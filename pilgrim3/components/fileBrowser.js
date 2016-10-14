import React from 'react';
import state from './state';
import { map, compact } from 'lodash';
import { Link } from 'react-router';
import OptionsTable from './optionsTable'
import DocBlock from './docBlock'

export default class FileBrowser extends React.Component {
  dependencyItems(items) {
    return map(items, (item) => {
      return (
        <li key={`file-browser-item-link-${item}`}>
          <Link to={`/files/${item}`}>{item}</Link>
        </li>
      );
    });
  }

  fileTable(file) {
    return (
      <table className='table table-hover'>
        <tbody>
          <tr>
            <th className='col-md-2'>Syntax</th>
            <td>{file.syntax || 'proto2'}</td>
          </tr>
          <tr>
            <th>Package</th>
            <td>{file.package}</td>
          </tr>
          <tr>
            <th>Dependencies</th>
            <td>
              <ul className='list-unstyled'>
                {this.dependencyItems(file.dependency)}
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
    );
  }

  linkThings(things, prefix) {
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

  render() {
    let key = this.props.params.splat.join('/');

    if (!state.byFile || !state.byFile[key]) {
      return (
        <h3>Not Found</h3>
      );
    }

    let file = state.byFile[key];

    // TODO(daicoden) replace test-done with template mechanism, tests will use it to inject this data, others can use it to styleize page
    return (
      <div className='panel panel-default'>
        <div className='panel-heading'>
          <h4>{file.name}</h4>
        </div>
        <DocBlock docs={file.documentation} />

        <div className='row'>
          <div className='col-sm-6'>
            <div className='panel panel-default'>
              <div className='panel-heading'>
                <h5>Info</h5>
              </div>
              {this.fileTable(file)}
            </div>
          </div>

          <div className='col-sm-6'>
            <div className='panel panel-default'>
              <div className='panel-heading'>
                <h5>Options</h5>
              </div>
              <OptionsTable object={file}/>
            </div>
          </div>
        </div>

        <div className='row'>
          <div className='col-sm-4'>
            <div className='panel panel-default'>
              <div className='panel-heading'>
                <h4>Enums ({compact(file.enumType).length})</h4>
              </div>
              <div className='panel-body'>
                {this.linkThings(file.enumType, '/enums')}
              </div>
            </div>
          </div>

          <div className='col-sm-4'>
            <div className='panel panel-default'>
              <div className='panel-heading'>
                <h4>Services ({compact(file.service).length})</h4>
              </div>
              <div className='panel-body'>
                {this.linkThings(file.service, '/services')}
              </div>
            </div>
          </div>

          <div className='col-sm-4'>
            <div className='panel panel-default'>
              <div className='panel-heading'>
                <h4>Messages ({compact(file.messageType).length})</h4>
              </div>
              <div className='panel-body'>
                {this.linkThings(file.messageType, '/messages')}
              </div>
            </div>
          </div>
        </div>
        <div id="test-done"></div>
      </div>
    );
  }
}
