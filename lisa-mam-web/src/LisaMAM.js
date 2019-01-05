import React from 'react';
import ReactDOM from 'react-dom';
import PropositionAdder from './PropositionAdder';
import SpatialArray from './SpatialArray';

class LisaMAM extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <div className="class">
            <h1>UI for LISA Mental Array Module Simulation</h1>
            <PropositionAdder/>
            <SpatialArray/>
            </div>
        );
    }



}

export default LisaMAM;