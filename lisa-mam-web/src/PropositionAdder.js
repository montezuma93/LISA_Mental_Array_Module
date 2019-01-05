import React from 'react';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Proposition from './Proposition';

class PropositionAdder extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      	propositions: []
    };
  }

  static defaultProps = {
    relations: ['South', 'North', 'East', 'West', 'NorthWest', 'NorthEast', 'SouthWest', 'SouthEast'],
  }

  render() {
    const { relationName, objectName1, objectName2 } = this.state;
    let relationOptions = this.props.relations.map(relation => {
      return <option key={relation} value={relation}>{relation}</option>
    });
    return (
      <div>
        <div>
          {this.state.propositions.map(function(idx){
              return (<Proposition key={idx}/>)
          })}
          <Button onClick={this.addProposition} title="Add Proposition"  style={{marginTop: '4rem'}}>Add Proposition</Button>
          <Button onClick={this.startSimulation} title="Start Simulation"  style={{marginTop: '4rem'}}>Start Simulation</Button>
        </div>
      </div>
    );
  }

  startSimulation = (e) => {
    const { relationName, objectCategory1, objectName1, objectCategory2, objectName2 } = this.state;
    console.log("submit")
    return fetch('http://127.0.0.1:5000/save_knowledge_fragment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "relation": relationName,
        "objects": [
          {
            "name": objectName1,
            "type": objectCategory1
          },
          {
            "name": objectName2,
            "type": objectCategory2,
          }
        ]
      })
    });

  }

  addProposition = (e) => {
    this.setState({propositions:[...this.state.propositions, {"id": ++this.state.propositions.length}]});
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }
}

export default PropositionAdder;