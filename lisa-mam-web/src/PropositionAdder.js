import React from 'react';
import Button from '@material-ui/core/Button';
import Proposition from './Proposition';
import FormDialog from './FormDialog';
import SpatialArray from './SpatialArray';

class PropositionAdder extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        spatialArray: [],
      	propositions: []
    };
  }

  static defaultProps = {
    relations: ['South', 'North', 'East', 'West', 'NorthWest', 'NorthEast', 'SouthWest', 'SouthEast'],
  }

  render() {
    return (
      <div>
        <div  style={{marginLeft: '10rem'}} >
          {this.state.propositions.map(function(item){
              return (<Proposition key={item.id} id={item.id} data={item} onChangeValue={this.handleChangeValue} relation/>)
          }, this)}
          <Button onClick={this.addProposition} title="Add Proposition"  style={{marginTop: '4rem', marginBottom: '2rem', marginLeft: '14rem'}}>Add Proposition</Button >
          <FormDialog propositions={this.state.propositions} setSpatialArray={this.handleSpatialArray} style={{height: '1000rem'}}/>
          <SpatialArray spatialArray={this.state.spatialArray}/>
        </div>
      </div>
    );
  }

  handleChangeValue = (e, id) => {
    var new_propositions = this.state.propositions
    var new_proposition = this.state.propositions[id -1]
    if (e.target.name === "objectName1") {
      new_proposition.objectName1 = e.target.value
    } else if(e.target.name === "objectName2") {
      new_proposition.objectName2 = e.target.value
    }
    else {
      new_proposition.relationName = e.target.value
    }
    new_propositions[e.id -1 ] = new_proposition
    this.setState({propositions: new_propositions
    })
  }
    
  handleSpatialArray = (data) => {
    this.setState({spatialArray: data.spatial_array})
  }

  addProposition = (e) => {
    this.setState({propositions:[...this.state.propositions, {"id": ++this.state.propositions.length, "relationName":"", "objectName1": "", "objectName2": ""}]});
  }
}

export default PropositionAdder;
