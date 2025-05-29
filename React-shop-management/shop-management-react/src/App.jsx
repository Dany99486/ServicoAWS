import React from 'react';
import RepairList from './components/RepairList';

function App() {
  return (
    <div>
      <h1>Gestão da Loja – PrimeTech</h1>
      <RepairList filter="agendado" />
      <RepairList filter="diagnosticado" />
      <RepairList filter="entregue" />
    </div>
  );
}

export default App;


/*import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;*/
