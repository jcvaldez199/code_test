import re
from flask import (
    Flask,  g, redirect, request, url_for, jsonify, session, send_file, current_app
)
from sqlalchemy import (
    create_engine, Column, Integer, String, select, asc
)
from sqlalchemy.orm import registry, Session, declarative_base
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Base = declarative_base()
engine = create_engine("postgresql://wang:codetest@localhost/codetest", echo=True, future=True)

# start of util class/funcs

class User(Base):

    __tablename__ = 'user'
    
    userid = Column(Integer, primary_key=True)
    name = Column(String)
    mail = Column(String)
    
    def __init__(self, *args, **kwargs):
        self.name = None
        self.mail = None
        self.userid = None
        self.mode = None
        self.setvals(*args, **kwargs)

    def setvals(self, *args, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'mail' in kwargs:
            self.mail = kwargs['mail']
        if 'userid' in kwargs:
            self.userid = kwargs['userid']
        if 'mode' in kwargs:
            self.mode = kwargs['mode']

    @property
    def serialize(self):
        return {'name': self.name, 'mail': self.mail, 'userid': self.userid}

class Param():
    def __init__(self, *args, **kwargs):
        self.name = None
        self.type = None
        self.verifier = lambda x: True
        self.setvals(*args, **kwargs)

    def setvals(self, *args, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'verifier' in kwargs:
            self.verifier = kwargs['verifier']

def verify_fields(reqs, *params, **kwargs):
    """
        Checks type and format validity of request form parameters
    """
    ret_dict = {}
    for param in params:
        if param.name in reqs:
            if type(reqs[param.name]) != param.type:
                ret_dict[param.name] = f"{param.name} has wrong type {type(reqs[param.name])}, expected {param.type}"
            elif not param.verifier(reqs[param.name]):
                ret_dict[param.name] = f"{param.name} has the wrong value format"
    if not ret_dict:
        return
    return {"error" : ret_dict}

def check_missing(userObj, *fields, **kwargs):
    """
        checks for missing required fields
    """
    ret_dict = {}
    userDict = vars(userObj)
    for field in fields:
        if not userDict[field]:
            ret_dict[field] = f"missing field : {field}"
    if not ret_dict:
        return
    return {"error" : ret_dict}

def gen_query_orm(userObj, *args, **kwargs):
    """
        generate and execute query
        it is assumed at this stage that values are verified
    """
    error = None
    mode = userObj.mode

    if mode == 'add':
        error = check_missing(userObj, 'name', 'mail')
        if not error:
            with Session(engine) as session:
                existing = session.scalars(select(User).where(User.mail == userObj.mail)).first()
                if existing:
                    error = {"error" : f"Mail {userObj.mail} already exists"}
                else:
                    session.add(userObj)
                    session.commit()
    elif mode == 'del':
        error = check_missing(userObj, 'userid')
        if not error:
            with Session(engine) as session:
                existing = session.scalars(select(User).where(User.userid == userObj.userid)).first()
                if not existing:
                    error = {"error" : f"Userid {userObj.userid} does not exist"}
                else:
                    session.delete(existing)
                    session.commit()
    elif mode == 'edit':
        error = check_missing(userObj, 'userid', 'name')
        if not error:
            with Session(engine) as session:
                existing = session.scalars(select(User).where(User.userid == userObj.userid)).first()
                if not existing:
                    error = {"error" : f"Userid {userObj.userid} does not exist"}
                else:
                    existing.name = userObj.name
                    session.commit()
    else:
        error = {"error" : "Invalid CRUD mode"}

    return error

def mail_regex(mail):
    # RFC 5322 standard email regex http://emailregex.com/
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return pattern.match(mail)

# end of util class/funcs

@app.route('/users', methods=('POST', 'GET'))
@cross_origin()
def user_crud():
    
    if (request.method == 'POST') and (not request.data):
        error = {"error":"No JSON Body."}
        return jsonify(error), 500

    if request.method == 'POST':

        req_form = request.get_json()
        ID_par   = Param(name='userid', type=int)
        Mode_par = Param(name='mode', type=str)
        Name_par = Param(name='name', type=str)
        Mail_par = Param(name='mail', type=str, verifier=mail_regex)
        error = verify_fields(
            req_form, ID_par, Mode_par, Name_par, Mail_par
        )

        if error:
            return jsonify(error), 500

        userObj  = User(**req_form)
        error = gen_query_orm(userObj)

        if error:
            return jsonify(error), 500

        return jsonify({'stat':'success'})

    elif request.method == 'GET':
        ret_list = None
        with Session(engine) as session:
            stmt = select(User)
            ret_list = [x.serialize for x in session.scalars(select(User).order_by(asc(User.userid))).all()]
        return jsonify(json_list=ret_list)

    return jsonify({"error":"Invalid HTTP method."}), 500
