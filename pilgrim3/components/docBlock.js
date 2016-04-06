import React from 'react'
import ReactMarkdown from 'react-markdown'

export default class DocBlock extends React.Component{

  render() {
    if (!this.props.docs) {
      return (<div/>);
    } else {
      return (
        <div className='col-sm-12'>
          <ReactMarkdown className='documentation' source={this.props.docs} />
        </div>
      )
    }
  }
}
