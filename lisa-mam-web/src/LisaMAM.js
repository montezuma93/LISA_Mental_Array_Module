import React from 'react';
import PropositionAdder from './PropositionAdder';

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
            </div>
        );
    }
}

export default LisaMAM;