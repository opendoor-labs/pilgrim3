import React from 'react'
import { map } from 'lodash'

export default class OptionsTable extends React.Component {
  optionRow(value, key) {
    return (
      <tr key={`${key}-${value}`}>
        <th>{key}</th>
        <td>{value.toString()}</td>
      </tr>
    );
  }

  render() {
    if (!this.props.object) {
      return (<span/>);
    } else {
      return (
        <table className='table table-hover'>
          <tbody>
            {map(this.props.object.options, this.optionRow)}
          </tbody>
        </table>
      );
    }
  }
}
