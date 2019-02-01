import React from 'react';

class SpatialArray extends React.Component {

  render() {
    return (
      <div >
        <table style={{align:"center", marginTop:"4rem"}}>{this.createTable()}</table>
      </div>
    );
  }
    
  createTable = () => {
    let table = []
    for (let i = 0; i < this.props.spatialArray.length; i++) {
      let children = []
      for (let j = 0; j < this.props.spatialArray[i].length; j++) {
        if (this.props.spatialArray[i][j] == null){
          children.push(<td style={{"borderStyle":'solid', "borderWidth":0.5, width:'3rem', height:'3rem'}}></td>)
        } else {
          children.push(<td style={{"borderStyle":'solid', "borderWidth":0.5, width:'3rem', height:'3rem', "text-align": 'center', "vertical-align": 'middle'}}>{this.props.spatialArray[i][j]}</td>)
        }
      }
      table.push(<tr style={{"borderStyle":'solid', "borderWidth":0.5}}>{children}</tr>)
    }
    return table
  }
}

export default SpatialArray;