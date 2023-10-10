import React from 'react';
import 'website3/src/styles/main.css';
function Home() {
  return (
    <section>

           <h1>Manual Control</h1>

                            <img id="videoStream" src="http://localhost:4000/od-videostream" alt="Video Stream"></img>
                <div class="row">
                        <div class="container">
                            <h4>Camera</h4>
                                <div class="remotecontrol-buttons">
                                    <button id="btnOk1" class="remotebtn btn-secondary" onclick="changeVideo('http://localhost:4000/od-videostream')">Normal</button>
                                    <button id="btnOk1" class="remotebtn btn-secondary" onclick="changeVideo('http://localhost:4000/od-videostream')">Object Detection</button>
                                    <button id="btnOk1" class="remotebtn btn-secondary" onclick="changeVideo('http://127.0.0.1:5000/od-videostream')">Depth Perception</button>
                                    <button id="btnDown1" class="remotebtn btn-secondary">Capture Image</button>
                                    <button id="btnDown1" class="remotebtn btn-secondary">Capture Video</button>
                                </div>
                        </div>
                </div>
                         <div class="container">
                        <h4>Wheel Speed</h4>
                        <div class="row">
                            <div class="col">
                            <label for="frontleft-wheel-speed">Front Left Wheel Speed:</label>
                            </div>
                            <div class="col">
                            <label for="frontright-wheel-speed">Front Right Wheel Speed:</label>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                            <label for="backleft-wheel-speed">Back Left Wheel Speed:</label>
                            </div>
                            <div class="col">
                            <label for="backright-wheel-speed">Back Right Wheel Speed:</label>
                            </div>
                        </div>
                        </div>
                                   <button id="btnUpLeft" class="remotebtn btn-secondary">Up/Left</button>
                                    <button id="btnUp" class="remotebtn btn-secondary">Up</button>
                                    <button id="btnUpRight" class="remotebtn btn-secondary">Up/Right</button>
                                    <button id="btnLeft" class="remotebtn btn-secondary">Left</button>
                                    <button id="btnStop" class="remotebtn btn-secondary">Stop</button>
                                    <button id="btnRight" class="remotebtn btn-secondary">Right</button>
                                    <button id="btnDownLeft" class="remotebtn btn-secondary">Down/Left</button>
                                    <button id="btnDown" class="remotebtn btn-secondary">Down</button>
                                    <button id="btnDownRight" class="remotebtn btn-secondary">Down/Right</button>
 

    </section>
  );
}

export default Home;
