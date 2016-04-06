import React from 'react'
import { Link } from 'react-router'

export default class ProtoInfo extends React.Component {

  render() {
    if (!this.props.infoObject) {
      return (<div/>);
    } else {
      let thing = this.props.infoObject;

      return (
        <table className="table table-hover">
          <tbody>
            <tr>
              <th>File</th>
              <td><Link to={`/files/${thing.fileDescriptor.name}`}>{thing.fileDescriptor.name}</Link></td>
            </tr>
            <tr>
              <th>Package</th>
              <td>{thing.fileDescriptor.package}</td>
            </tr>
            <tr>
              <th>Full Name</th>
              <td>{thing.fullName}</td>
            </tr>
            <tr>
              <th>Name</th>
              <td>{thing.name}</td>
            </tr>
          </tbody>
        </table>
      );
    }
  }
}
