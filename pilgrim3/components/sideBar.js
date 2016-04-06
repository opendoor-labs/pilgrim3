import React from 'react';
import state from './state';
import { keys, map, filter, includes } from 'lodash';
import NavLink from './navLink';

const FILES = 'files';
const MESSAGES = 'messages';
const ENUMS = 'enums';
const SERVICES = 'services';
const ACTIVE = 'active';

class SelectionButton extends React.Component {
  render() {
    let isActive = this.props.activeSelection === this.props.value;
    let classNames;
    if (isActive) {
      classNames = 'btn btn-primary'
    } else {
      classNames = 'btn btn-default'
    }

    return (
      <button
        type="button"
        value={this.props.value}
        className={classNames}
        onClick={this.props.onClick}>{this.props.children}</button>
    )
  }
}

export default React.createClass({
  getInitialState: function() {
    return {
      query: undefined,
      kind: this.selectorKind() || FILES,
    }
  },

  items: function(kind) {
    let foundKeys = keys(this.itemObjects(kind));
    return this.filterItems(foundKeys).sort();
  },

  itemObjects(kind) {
    switch (kind) {
    case SERVICES:
      return state.byService;
      break;
    case FILES:
      return state.byFile;
      break;
    case MESSAGES:
      return state.byMessage;
      break;
    case ENUMS:
      return state.byEnum;
      break;
    }
  },

  filterItems: function(items) {
    let query = this.state.query
    if (!query) return items;

    let lowerQuery = query.toString().toLowerCase();

    return filter(items, (i) => {
      return includes(i.toLowerCase(), lowerQuery);
    }).sort();
  },

  handleQueryChange: function(e) {
    let newState = this.state;
    newState.query = this.refs.queryInput.value
    this.setState(newState);
  },

  setActiveType: function(e) {
    let state = this.state;
    state.kind = e.target.value;
    this.setState(state);
  },

  selectorKind: function() {
    if (this.props.params.splat) {
      return FILES
    } else if (this.props.params.service_name) {
      return SERVICES
    } else if (this.props.params.message_name) {
      return MESSAGES
    } else if (this.props.params.enum_name) {
      return ENUMS
    }
  },

  render: function() {
    let kind = this.state.kind;
    let route;
    if (this.props.params.splat) {
      let fileName = this.props.params.splat.join('/')
      route = (name) => {  return (fileName == name ? ACTIVE : ''); }
    } else if (this.props.params.service_name) {
      route = (name) => {  return (this.props.params.service_name == name ? ACTIVE : ''); }
    } else if (this.props.params.message_name) {
      route = (name) => {  return (this.props.params.message_name == name ? ACTIVE : ''); }
    } else if (this.props.params.enum_name) {
      route = (name) => {  return (this.props.params.enum_name == name ? ACTIVE : '') }
    } else {
      route = () => { return ''; }
    }

    let objects = this.itemObjects(kind);

    let items = map(this.items(kind), (item) => {
      let obj = objects[item];
      let pkg;
      if (obj.fileDescriptor) {
        pkg = (<small className='pull-left'>{obj.fileDescriptor.package}</small>)
      }

      return (
        <li key={`${kind}-${item}`} className={route(item)}>
          <NavLink to={`/${kind}/${item}`}>
            {pkg}
            <div className='text-right'>{obj.name}</div>
          </NavLink>
        </li>
      );
    });

    return (
      <div>
        <div className='btn-group' role='group'>
          <SelectionButton value={FILES} activeSelection={this.state.kind} onClick={this.setActiveType}>Files</SelectionButton>
          <SelectionButton value={SERVICES}  activeSelection={this.state.kind} onClick={this.setActiveType}>Services</SelectionButton>
          <SelectionButton value={MESSAGES} activeSelection={this.state.kind} onClick={this.setActiveType}>Messages</SelectionButton>
          <SelectionButton value={ENUMS} activeSelection={this.state.kind} onClick={this.setActiveType}>Enums</SelectionButton>
        </div>
        <input type='search' ref='queryInput' className='form-control' onChange={this.handleQueryChange} />
        <ul id='nav-docs' className='nav nav-pills nav-stacked list list-unstyled pad40-top'>
          {items}
        </ul>
      </div>
    );
  }
});
