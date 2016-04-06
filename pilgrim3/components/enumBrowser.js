import React from 'react'
import state from './state'
import { Link } from 'react-router'
import { map } from 'lodash'
import { relativeName } from './utils'
import ProtoInfo from './protoInfo'
import DocBlock from './docBlock'
import OptionsPopover from './optionsPopover'

export default class EnumBrowser extends React.Component {
  renderEnum(theEnum) {
    let docs;

    return (
      <div>
        <h1>{theEnum.name}<OptionsPopover placement='right' obj={theEnum} /></h1>
        <DocBlock docs={theEnum.documentation} />
        <ProtoInfo infoObject={theEnum}/>
        {this.renderValues(theEnum)}
      </div>
    );
  }

  renderValues(theEnum) {
    let valueRows = this.renderValueRows(theEnum.value, theEnum);

    return (
      <div className='panel panel-default'>
        <div className='panel-heading'>Values</div>
        <table className='table table-hover'>
          <thead>
            <tr>
              <th/> 
              <th>ID</th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            {valueRows}
          </tbody>
        </table>
      </div>
    )
  }

  renderValueRows(values, theEnum) {
    return map(values, (value) => {
      return (
        <tr key={`enum-value-row-${theEnum.fullName}-${value.number}`}>
          <td><OptionsPopover placement='left' obj={theEnum}/></td>
          <td>{value.number}</td>
          <td>{value.name}</td>
        </tr>
      );
    });
  }

  render() {
    if (!state.byEnum) {
      return (<div className='alert alert-info'>Loading</div>);
    }

    let theEnum = state.byEnum[this.props.params.enum_name];

    if (!theEnum) {
      return (<div className='alert alert-danger'>Enum Not Found</div>);
    } else {
      return this.renderEnum(theEnum);
    }
  }
}
