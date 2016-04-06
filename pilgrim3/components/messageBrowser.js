import React from 'react'
import state from './state'
import { Link } from 'react-router'
import { map, forEach, isNumber, find } from 'lodash'
import { relativeName } from './utils'
import ProtoInfo from './protoInfo'
import DocBlock from './docBlock'
import OptionsPopover from './optionsPopover'

const COLORS = [
  '#CEF6CE',
  '#CEECF5',
  '#F5F6CE',
  '#F8E0E6',
  '#F2E0F7',
];

export default class MessageBrowser extends React.Component {
  componentWillMount() {
    this.currentColorIdx = -1;
  }

  componentWillReceiveProps() {
    this.currentColorIdx = -1;
  }

  nextColor() {
    this.currentColorIdx++;
    if (this.currentColorIdx === COLORS.length) this.currentColorIdx = 0;
    return COLORS[this.currentColorIdx];
  }

  renderMessage(msg) {
    return (
      <div>
        <h1>{msg.name}<OptionsPopover placement='right' obj={msg} /></h1>
        <DocBlock docs={msg.documentation}/>
        <ProtoInfo infoObject={msg}/>
        {this.renderFields(msg)}
      </div>
    );
  }

  renderFields(msg) {
    let fieldRows = this.renderFieldRows(msg.field, msg);

    return (
      <div className='panel panel-default'>
        <div className='panel-heading'>Fields</div>
        <table className='table table-hover'>
          <thead>
            <tr>
              <th/>
              <th>Id</th>
              <th>Kind</th>
              <th>Name</th>
              <th>JSON Name</th>
              <th>Type</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {fieldRows}
          </tbody>
        </table>
      </div>
    )
  }

  renderFieldRows(fields, msg) {
    let currentOneOfIdx;
    let rows = [];
    let style = {};
    let color;

    forEach(fields, (field) => {
      if(isNumber(field.oneofIndex)) {
        if (currentOneOfIdx !== field.oneofIndex) {
          currentOneOfIdx = field.oneofIndex;
          color = this.nextColor();
          style = { backgroundColor: color };

          rows.push(
            <tr className='oneof-header' key={`one-of-${msg.fullName}-${currentOneOfIdx}`} style={style}>
              <th colSpan={7}><h5>{msg.oneofDecl[currentOneOfIdx].name}</h5></th>
            </tr>
          );
        }

        rows.push(
          <tr style={style} className='oneof-row' key={`on-of-${currentOneOfIdx}-field-row-${msg.fullName}-${field.number}-${field.name}`}>
            <td><OptionsPopover obj={field}/></td>
            <td>{field.number}</td>
            <td>{this.renderFieldType(field, msg)}</td>
            <td>{field.name}</td>
            <td>{field.jsonName}</td>
            <td>{this.renderFieldLabel(field)}</td>
            <td><DocBlock docs={field.documentation}/></td>
          </tr>
        )
      } else {
        rows.push(
          <tr key={`field-row-${msg.fullName}-${field.number}-${field.name}`}>
            <td><OptionsPopover obj={field}/></td>
            <td>{field.number}</td>
            <td>{this.renderFieldType(field, msg)}</td>
            <td>{field.name}</td>
            <td>{field.jsonName}</td>
            <td>{this.renderFieldLabel(field)}</td>
            <td><DocBlock docs={field.documentation}/></td>
          </tr>
        );
      }
    });

    return rows;
  }

  renderFieldLabel(field) {
    if (field.typeName) {
      let msg = state.byMessage[field.typeName]
      if (msg && msg.options && msg.options.mapEntry) {
        return 'MAP';
      }
    }

    let label = field.label.replace(/^LABEL_/, '')
    if (label !== 'OPTIONAL') return label;
  }

  renderFieldType(field, msg) {
    let type = field.type.replace(/^TYPE_/, '');

    switch(type) {
      case 'MESSAGE':
        let msgName = field.typeName
        let msgType = state.byMessage[field.typeName];
        if (msgType.options && msgType.options.mapEntry) {
          let keyField = find(msgType.field, {name: 'key'});
          let valueField = find(msgType.field, {name: 'value'});
          return (
            <span className='proto-map'>
              <Link to={`/messages/${msgName}`}>map</Link>
              {`<${this.renderFieldType(keyField, msg)}, `}
              {this.renderFieldType(valueField, msg)}
              {'>'}
            </span>
          )

        } else {
          return (
            <Link to={`/messages/${msgName}`}>{relativeName(msgName, msg.fileDescriptor)}</Link>
          );
        }
        break;
      case 'ENUM':
        let enumName = field.typeName;
        return (
          <Link to={`/enums/${enumName}`}>{relativeName(enumName, msg.fileDescriptor)}</Link>
        );
        break;

      default:
        return type.toLowerCase();
    }
  }

  render() {
    if (!state.byMessage) {
      return (<div className='alert alert-info'>Loading</div>);
    }

    let msg = state.byMessage[this.props.params.message_name];

    if (!msg) {
      return (<div className='alert alert-danger'>Message Not Found</div>);
    } else {
      return this.renderMessage(msg);
    }
  }
}
