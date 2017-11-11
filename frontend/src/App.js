import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  constructor(props){
      super(props);
  }


  fetchData(){
    fetch('http://127.0.0.1:5000/content', {method: "GET"}).then((res) => {
      return res.json()
    }).then((j) => {
      alert(JSON.stringify(j));
    }).catch(e => {
      alert("Failed: ", e);
    });
  }


  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <input type="button" onClick={this.fetchData} value="Test Server Connection"/>
      </div>
    );
  }
}

export default App;
