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
    const { relation, objectName1, objectName2 } = this.state;
    let relationOptions = this.props.relations.map(relation => {
      return <option key={relation} value={relation}>{relation}</option>
    });
    return (
      <div>
        <div>
          {this.state.propositions.map(function(item){
              return (<Proposition key={item.id} id={item.id} data={item} onChangeValue={this.handleChangeValue} relation/>)
          }, this)}
          <Button onClick={this.addProposition} title="Add Proposition"  style={{marginTop: '4rem'}}>Add Proposition</Button>
          <Button onClick={this.startSimulation} title="Start Simulation"  style={{marginTop: '4rem'}}>Start Simulation</Button>
        </div>
      </div>
    );
  }

  handleChangeValue = (e, id) => {
    var new_propositions = this.state.propositions
    var new_proposition = this.state.propositions[id -1]
    if (e.target.name == "objectName1") {
      new_proposition.objectName1 = e.target.value
    } else if(e.target.name == "objectName2") {
      new_proposition.objectName2 = e.target.value
    }
    else {
      new_proposition.relationName = e.target.value
    }
    new_propositions[e.id -1 ] = new_proposition
    this.setState({propositions: new_propositions

    })
  }

  startSimulation = (e) => {
    const { propositions } = this.state;
    console.log("submit")
    return fetch('http://127.0.0.1:5000/start_simulation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "propositions": propositions
      })
    });

  }

  addProposition = (e) => {
    this.setState({propositions:[...this.state.propositions, {"id": ++this.state.propositions.length, "relationName":"", "objectName1": "", "objectName2": ""}]});
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }
}

export default PropositionAdder;