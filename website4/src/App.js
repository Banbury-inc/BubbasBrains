import React, { Component } from "react";
import "./App.css";

import ReactNippleExample from "./ReactNippleExample";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
        </header>
        <div className="App-examples">
          <ReactNippleExample
            title="Joystick"
            width={450}
            height={350}
            options={{ mode: "dynamic", color: "red" }}
          />
       </div>
      </div>
    );
  }
}

export default App;
