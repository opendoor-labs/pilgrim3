import React from 'react'
import ReactDOM from 'react-dom'
import { Link } from 'react-router'
import { Navbar } from 'react-bootstrap'

export default class NavBar extends React.Component {
  render() {
    return (
      <Navbar>
         <Navbar.Header>
           <Navbar.Brand>
             <Link to='/'>Pilgrim</Link>
           </Navbar.Brand>
           <Navbar.Toggle />
         </Navbar.Header>
       </Navbar>
    );
  }
}
