import './App.css';

import React, { useState } from 'react'
import axios from 'axios'
import { Form, Stack, Container, Col, Button, Card, Alert, Table } from 'react-bootstrap'
import { BaseUrl } from './config'

function App() {
  
  const [variant, setVariant] = useState('success');
  const [userList, setUserList] = useState([]);
  const [userDel, setUserDel] = useState();
  const [userMod, setUserMod] = useState();
  const [alertmsg, setAlertmsg] = useState(() => (<div></div>));
  const [alertstatus, setAlertstatus] = useState(200);
  const [alertenabled, setAlertEnabled] = useState(false);

  function SuccessRoutine(response) {
     setAlertmsg(() => (
     	<div>
     	  <p>Request succeeded with status code 200</p>
     	</div>
     ));
     setVariant('success');
     setAlertEnabled(true);
     setAlertstatus(200);
     window.scrollTo(0, 0);
  }

  function FailureRoutine(error) {
     setAlertmsg(() => (
     	<div>
     	  <p>Request failed with status code 500</p>
     	  <p>Server responded with the following error message:</p>
     	  <p>{JSON.stringify(error.response.data.error)}</p>
     	</div>
     ));
     setVariant('danger');
     setAlertEnabled(true);
     setAlertstatus(500);
     window.scrollTo(0, 0);
  }

  function Adder() {
  
    function postCred(event) {
      event.preventDefault()
      axios.post(BaseUrl, 
      {
        name: event.target.elements.formName.value,
        mail: event.target.elements.formEmail.value,
        mode: "add"
      })
      .then(SuccessRoutine)
      .catch(FailureRoutine);
    }
  
    return (
     <form onSubmit={postCred}>
        <Card>
          <Card.Header as="h5">Add User</Card.Header>
          <Card.Body>
	    <Stack gap={2}>
  	      <div className="form-group" >
  	          <input type="name" name="formName" className="form-control" placeholder="Enter your name" />
  	      </div>
  	      <div className="form-group">
  	          <input type="email"  name="formEmail" className="form-control" placeholder="Enter your email" />
  	      </div>
  	      <Button size="lg" type="submit" variant="primary">addUser</Button>
	    </Stack>
          </Card.Body>
        </Card>
    </form>
    );
  }

  function Getter() {
  
    function getUsers(event) {
      event.preventDefault()
      axios.get(BaseUrl)
      .then((response) => {
	SuccessRoutine(response);
	setUserList(response.data.json_list);
	console.log(response.data.json_list);
	if (response.data.json_list && response.data.json_list.length) {
	    setUserMod(response.data.json_list[0].userid);
	    setUserDel(response.data.json_list[0].userid);
        }
	   
      })
      .catch(FailureRoutine);
    }
    
    return (
       <Card>
         <Card.Header as="h5">Get Users</Card.Header>
         <Card.Body>
	   <Stack gap={2}>
              <Table variant='dark' striped bordered>
                <tbody>
                  <tr>
                    <td>#</td>
                    <td>id</td>
                    <td>name</td>
                    <td>mail</td>
                  </tr>
                  {userList.map((userObj, index) => (
		      <tr>
		        <td>{index}</td>
		        <td>{userObj.userid}</td>
		        <td>{userObj.name}</td>
		        <td>{userObj.mail}</td>
		      </tr>
                  ))}
                </tbody>
              </Table>
             <Button onClick={getUsers} size="lg" type="submit" variant="info">getUser</Button>
	   </Stack>
         </Card.Body>
       </Card>
    );
  }

  function Modder() {
  
    function postCred(event) {
      event.preventDefault()
      axios.post(BaseUrl, 
      {
        name: event.target.elements.formName.value,
	userid: Number(userMod),
        mode: "edit"
      })
      .then(SuccessRoutine)
      .catch(FailureRoutine);
    }
  
    return (
     <form onSubmit={postCred}>
        <Card>
          <Card.Header as="h5">Mod User Name</Card.Header>
          <Card.Body>
	    <Stack gap={2}>
	      <Form.Select 
                value={userMod}
                onChange={(event) => setUserMod(event.target.value)}
	        aria-label="Default select example"
	      >
                {userList.map((userObj, index) => (
		    <option value={userObj.userid}>{userObj.userid}</option>
                ))}
              </Form.Select>
  	      <div className="form-group" >
  	          <input type="name" name="formName" className="form-control" placeholder="Enter new name" />
  	      </div>
  	      <Button size="lg" type="submit" variant="warning">modUser</Button>
	    </Stack>
          </Card.Body>
        </Card>
    </form>
    );
  }

  function Deleter() {
  
    function postCred(event) {
      event.preventDefault()
      axios.post(BaseUrl, 
      {
	userid: Number(userDel),
        mode: "del"
      })
      .then(SuccessRoutine)
      .catch(FailureRoutine);
    }
  
    return (
     <form onSubmit={postCred}>
        <Card>
          <Card.Header as="h5">Delete User</Card.Header>
          <Card.Body>
	    <Stack gap={2}>
	      <Form.Select 
                value={userDel}
                onChange={(event) => setUserDel(event.target.value)}
	        aria-label="Default select example"
	      >
                {userList.map((userObj, index) => (
		    <option value={userObj.userid}>{userObj.userid}</option>
                ))}
              </Form.Select>
  	      <Button size="lg" type="submit" variant="danger">delUser</Button>
	    </Stack>
          </Card.Body>
        </Card>
    </form>
    );
  }

  return (
    <div className="App">
	  <Container>
	     <Col className="col-md-5 mx-auto minBreakpoint-xs">
	         <Stack gap={2}>
	           <h1>Home</h1>
	           <Alert key={variant} variant={variant} show={alertenabled} onClose={() => setAlertEnabled(false)} dismissible>
	                 <Alert.Heading>{alertstatus}</Alert.Heading>
	  	         {alertmsg}
	           </Alert>
	             <div><Adder /></div>
	             <div><Getter /></div>
	             <div><Modder /></div>
	             <div><Deleter /></div>
	         </Stack>
             </Col>
          </Container>
    </div>
  );
}

export default App;
