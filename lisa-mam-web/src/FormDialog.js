import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

export default class FormDialog extends React.Component {
  state = {
    open: false,
    size: 9,
    unmarkedDistance: 2,
    markedDistance: 1,
    standardDeviation: 0.5,
    amountOfFiringEvents: 10
  };

  render() {
    return (
      <div>
        <Button variant="outlined" color="primary" onClick={this.handleClickOpen}>
          Adjust settings and start simulation
        </Button>
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Subscribe</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Please set the settings for the simulation. 
              If you don't want to change something, just use the default values.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              value={this.state.size}
              onChange={this.onChange}
              id="name"
              name="size"
              ref="size"
              label="Size"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              value={this.state.unmarkedDistance}
              id="name"
              name="unmarkedDistance"
              ref="unmarkedDistance"
              onChange={this.onChange}
              label="Unmarked distance between agent and referent"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              name="markedDistance"
              ref="markedDistance"
              value={this.state.markedDistance}
              id="name"
              onChange={this.onChange}
              label="Marked distance between agent and referent"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              name="standardDeviation"
              ref="standardDeviation"
              value={this.state.standardDeviation}
              id="name"
              onChange={this.onChange}
              label="StandardDeviation, for the gaussian distribution"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              name="amountOfFiringEvents"
              ref="amountOfFiringEvents"
              value={this.state.amountOfFiringEvents}
              id="name"
              onChange={this.onChange}
              label="Amount of firing events, how often gaussian distribution will chose"
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleClose} color="primary">
              Start Simulation
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
  
  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
    return fetch('http://127.0.0.1:5000/start_simulation', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "propositions": this.props.propositions,
        "size": this.state.size,
        "unmarkedDistance": this.state.unmarkedDistance,
        "markedDistance": this.state.markedDistance,
        "standardDeviation": this.state.standardDeviation,
        "amountOfFiringEvents": this.state.amountOfFiringEvents
      })
    })
    .then((response) => response.json())
    .then((data) => this.props.setSpatialArray(data));
  };

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
    
  }
}