import React from 'react'
import { OverlayTrigger, Popover, Glyphicon } from 'react-bootstrap'
import { isEmpty, forEach } from 'lodash'

export default class OptionsPopover extends React.Component {
  renderOptionRows(opts, id) {
    let rows = [];

    forEach(opts, (val, name) => {
      rows.push(
        <tr key={`${id}-${name}`}>
          <td>{name}</td>
          <td>{val.toString()}</td>
        </tr>
      )
    })
    return rows;
  }

  renderOptions(opts, id) {
    let rows = this.renderOptionRows(opts, id)
    return (
      <Popover id={id}>
        <table className='table table-hover'>
          <thead>
            <tr>
              <th>{'Name'}</th>
              <th>{'Value'}</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </Popover>
    )
  }

  render() {
    if (!this.props.obj || !this.props.obj.options || isEmpty(this.props.obj.options)) {
      return (<span/>);
    } else {
      let content = this.renderOptions(this.props.obj.options, `${this.props.obj.fullName}-options`);
      return (
        <OverlayTrigger
          trigger='click'
          placement={this.props.placement || 'left'}
          overlay={content}
          className='clickable'
        >
          <Glyphicon className='clickable' glyph='option-vertical'/>
        </OverlayTrigger>
      );
    }
  }
}
