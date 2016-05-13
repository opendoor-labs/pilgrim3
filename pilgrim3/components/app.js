import React from 'react';
import { Col } from 'react-bootstrap';

import fetchProtos from './fetchProtos';
import state from './state';
import NavBar from './navbar';
import SideBar from './sideBar';

export default React.createClass({
  getInitialState: function() {
    return { loaded: false, errors: false };
  },

  componentDidMount: function() {
    fetchProtos(state).then(
      () => {
        this.setState({loaded: true, errors: false});
      },
      (errs) => {
        let theErrors = errs;
        this.setState({loaded: false, errors: errs});
      }
    );
  },

  render: function() {
    if (!this.state.loaded) {
      if (this.state.errors) {
        return (
          <div>
            <NavBar/>
            <div className='alert alert-danger'>
              {"Could not fetch your proto bundle. Have you compiled it?"}
            </div>
          </div>
        );
      } else {
        return (<div><NavBar/></div>);
      }
    }

    return (<div>
      <NavBar/>
      <Col id='left' md={3}>
        <SideBar params={this.props.params}/>
      </Col>
      <Col id='right' md={9}>
        {this.props.children}
      </Col>
    </div>);
  }
});

