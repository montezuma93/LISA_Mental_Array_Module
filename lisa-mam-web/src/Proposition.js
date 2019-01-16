import React from 'react';
import Select from '@material-ui/core/Select';
import TextField from '@material-ui/core/TextField';

class Proposition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      relationName: props.data.relationName,
      objectName1: props.data.objectName1,
      objectName2: props.data.objectName2,
    };
  }

  static defaultProps = {
    relations: ['South', 'North', 'East', 'West', 'NorthWest', 'NorthEast', 'SouthWest', 'SouthEast', 'Left', 'Right'],
  }

  render() {
    const { relationName, objectName1, objectName2} = this.state;
    let relationOptions = this.props.relations.map(relation => {
      return <option key={relation} value={relation}>{relation}</option>
    });
    return (
      <div>
        <div style={{display: 'inline-block'}}>
            <Select ref="relationName" value={relationName} onChange={this.onChange} name="relationName" style={{marginLeft: '4rem', width:'7rem'}}>
              {relationOptions}
            </Select>
            <TextField type="text" ref="objectName1" value={objectName1} onChange={this.onChange} name='objectName1' style={{marginLeft: '4rem'}}/>
            <TextField type="text" ref="objectName2" value={objectName2} onChange={this.onChange} name='objectName2' style={{marginLeft: '4rem'}}/>
        </div>
      </div>
    );
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value }, this.props.onChangeValue(e, this.state.id));  
  }
}

export default Proposition;