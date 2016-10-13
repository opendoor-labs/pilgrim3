import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory, IndexRoute } from 'react-router'
import App from './pilgrim3/components/app'
import FileBrowser from './pilgrim3/components/fileBrowser'
import ServiceBrowser from './pilgrim3/components/serviceBrowser'
import MessageBrowser from './pilgrim3/components/messageBrowser'
import EnumBrowser from './pilgrim3/components/enumBrowser'
import fetchProtos from './pilgrim3/components/fetchProtos'

class Empty extends React.Component {
  render() {
    return (<div>Nothing found. Select an item on the left</div>);
  }
}

ReactDOM.render((
  <Router history={hashHistory}>
    <Route path="/" component={App} onEntry={fetchProtos}>
      <IndexRoute component={Empty}/>
      <Route path="/files/**/*" component={FileBrowser}/>
      <Route path="/services/:service_name" component={ServiceBrowser}/>
      <Route path="/messages/:message_name" component={MessageBrowser}/>
      <Route path="/enums/:enum_name" component={EnumBrowser}/>
    </Route>
  </Router>
), document.getElementById('app'))

