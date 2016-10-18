import { map, compact } from 'lodash';
import { Link } from 'react-router';
import React from 'react'

export default class LinkBlock extends React.Component{
  render() {
    if (!this.props.things || !this.props.urlBase) {
      return (<div/>);
    } else {
      let things = this.props.things;
      let prefix = this.props.urlBase;
      let arrayThings = compact(things)
      let links = map(arrayThings, (thing) => {
        return (
            <li key={`thing-link-${prefix}-${thing.fullName}`}>
              <Link to={`${prefix}/${thing.fullName}`}>{thing.name}</Link>
            </li>
        );
      });


      return (
          <ul className='list list-unstyled'>
            {links}
          </ul>
      );
    }
  }
}
