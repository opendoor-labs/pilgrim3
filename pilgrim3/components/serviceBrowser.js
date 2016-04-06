import React from 'react';
import state from './state';
import { Link } from 'react-router';
import { map } from 'lodash';
import { relativeName } from './utils';
import ProtoInfo from './protoInfo';
import DocBlock from './docBlock';
import OptionsPopover from './optionsPopover';

export default class ServiceBrowser extends React.Component {
  renderService(service) {

    return (
      <div>
        <h1>{service.name}<OptionsPopover placement='right' obj={service} /></h1>
        <DocBlock docs={service.documentation} />
        <ProtoInfo infoObject={service}/>
        {this.renderMethods(service)}
      </div>
    );
  }

  renderMethods(service) {
    let methodRows = this.renderMethodRows(service.method, service);

    return (
      <div className='panel panel-default'>
        <div className='panel-heading'>Methods</div>
        <table className='table table-hover'>
          <thead>
            <tr>
              <th/>
              <th>Name</th>
              <th>Input</th>
              <th>Output</th>
            </tr>
          </thead>
          <tbody>
            {methodRows}
          </tbody>
        </table>
      </div>
    );
  }

  renderMethodRows(methods, service) {
    return map(methods, (meth) => {
      let deprecated = (meth.options && meth.options.deprecated) ? 'deprecated' : '';
      return (
        <tr key={`rpc-method-${service.fullName}-${meth.name}`} className={deprecated}>
          <td><OptionsPopover obj={meth}/></td>
          <td>{meth.name}</td>
          <td><Link to={`/messages/${meth.inputType}`}>{relativeName(meth.inputType, service.fileDescriptor)}</Link></td>
          <td><Link to={`/messages/${meth.outputType}`}>{relativeName(meth.outputType, service.fileDescriptor)}</Link></td>
        </tr>
      );
    });
  }

  render() {
    if (!state.byService) {
      return (<div className='alert alert-info'>Loading</div>);
    }

    let service = state.byService[this.props.params.service_name];

    if (!service) {
      return (<div className='alert alert-danger'>Service Not Found</div>);
    } else {
      return this.renderService(service);
    }
  }
}
