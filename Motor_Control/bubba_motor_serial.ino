/*
  BubbaBot Motor control
*/
int LRPWM = 10;           //Left Reverse PWM pin
int LRoff = 8;           //Left Reverse GND for forward pin
int LFPWM = 11;           //Left Forward PWM pin 
int LFoff = 12;           //Left Forward GND for reverse pin
int voltage = 0;          // battery voltage
int RRPWM = 3;           //Right Reverse PWM pin
int RRoff = 2;           //Right Reverse GND for forward pin
int RFPWM = 9;           //Right Forward PWM pin 
int RFoff = 7;           //Right Forward GND for reverse pin
int LRun = 200;          // how fast the left motor runs and it what direction (1-199 reverse / 200 stop / 201-400 forward)
int RRun = 200;          // how fast the left motor runs and it what direction (1-199 reverse / 200 stop / 201-400 forward)

char inChar;            // incoming data
String target;          // data target
int inputNumber = 0;    //to hold incoming data

unsigned long previousMillis = 0;  // data timmer

void setup() {
  // initialize serial:
  Serial.begin(9600);
    
  // declare pins to be an output:
    // left motor
  pinMode(LFPWM, OUTPUT);
  pinMode(LFoff, OUTPUT);
  pinMode(LRPWM, OUTPUT);
  pinMode(LRoff, OUTPUT);
    // set initial state of left motor pins
  digitalWrite(LFoff, HIGH);
  digitalWrite(LRoff, HIGH);
  digitalWrite(LFPWM, LOW);
  digitalWrite(LRPWM, LOW);
   // Right motor
  pinMode(RFPWM, OUTPUT);
  pinMode(RFoff, OUTPUT);
  pinMode(RRPWM, OUTPUT);
  pinMode(RRoff, OUTPUT);
    // set initial state of Right motor pins
  digitalWrite(RFoff, HIGH);
  digitalWrite(RRoff, HIGH);
  digitalWrite(RFPWM, LOW);
  digitalWrite(RRPWM, LOW);
} // end setup()

// function that executes whenever data is requested


// function that executes whenever data is received
void serialEvent() {
  while (Serial.available()) {
    previousMillis = millis();
    // get the new byte:
    inChar = (char)Serial.read();
    // determan what the input is for
    if (inChar == 'L') { target = "LeftMotor"; inputNumber = 0;}
    if (inChar == 'R') { target = "RightMotor"; inputNumber = 0;}
    if (inChar == 'V') Serial.println(voltage);
    if (inChar == 'P') Serial.println("Position");
    if (int(inChar) >= 48){ // int(char(48)) = 0
      if (int(inChar) <= 57){ // int(char(57)) = 9
        // add it to the inputNumber
        inputNumber = (inputNumber * 10) + (int(inChar) - 48);
      }
    }
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == 'n') {
       if (target == "LeftMotor") LRun = inputNumber;
       if (target == "RightMotor") RRun = inputNumber;
       // clear the string:
       delay(20);
       inputNumber = 0;
       target = "";
    }
  }
}

void loop() {

  // record battery voltage
  voltage = map(analogRead(A0),275,830,10,30);

  // Left motor control
  if (LRun == 200) { // stop left motor
  digitalWrite(LFoff, HIGH);
  digitalWrite(LRoff, HIGH);
  digitalWrite(LFPWM, LOW);
  digitalWrite(LRPWM, LOW);
  delay(600);
  } else {
    if(LRun < 200){
      digitalWrite(LFoff, HIGH);
      analogWrite(LFPWM, map(LRun,199,1,20,255));
      digitalWrite(LRoff, LOW);
      digitalWrite(LRPWM, LOW);
    }
    if(LRun > 200){
      digitalWrite(LRoff, HIGH);
      analogWrite(LRPWM, map(LRun,201,400,20,255));
      digitalWrite(LFoff, LOW);
      digitalWrite(LFPWM, LOW);
    }
  }
  // Right motor control
  if (RRun == 200) { // stop Right motor
  digitalWrite(RFoff, HIGH);
  digitalWrite(RRoff, HIGH);
  digitalWrite(RFPWM, LOW);
  digitalWrite(RRPWM, LOW);
  delay(600);
  } else {
    if(RRun < 200){
      digitalWrite(RFoff, HIGH);
      analogWrite(RFPWM, map(RRun,199,1,20,255));
      digitalWrite(RRoff, LOW);
      digitalWrite(RRPWM, LOW);
    }
    if(RRun > 200){
      digitalWrite(RRoff, HIGH);
      analogWrite(RRPWM, map(RRun,201,400,20,255));
      digitalWrite(RFoff, LOW);
      digitalWrite(RFPWM, LOW);
    }
  }
  delay(50);

  // Stop if there has been no input for more than one minute.
  if (previousMillis + 60000 < millis()){
    LRun = 200;
    RRun = 200;
    Serial.println("error");
    
  }
  
   
} // end loop()
