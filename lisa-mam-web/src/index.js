import React from 'react';
import ReactDOM from 'react-dom';
import LisaMAM from './LisaMAM';
import './index.css';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(
    <LisaMAM />,
    document.getElementById('root')
  );

serviceWorker.register();
