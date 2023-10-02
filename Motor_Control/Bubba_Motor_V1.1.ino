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
int WDog = 50000;         // Amount of time to run without input before stopping drive motors. (Milliseconds) range 500 - 15000
int DTime = 500;         // Amount of time required at stop before changing direction of a drive motor. (Milliseconds)
int MotorMin = 35;       // Minimuim soutput for motors to avoid stalling / High amp draw.
int LowBatt = 235;       // Minimum allowed battery voltage

char inChar;            // incoming data
String target;          // data target
int inputNumber = 0;    //to hold incoming data

unsigned long WDMillis = millis() + WDog;  // data timmer
unsigned long DirectionMillis = 0;  // data timmer

int i = 0;

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
    WDMillis = millis() + WDog;
    // get the new byte:
    inChar = (char)Serial.read();
    // determan what the input is for
    if (inChar == 'L') { target = "LeftMotor"; inputNumber = 0;}
    if (inChar == 'R') { target = "RightMotor"; inputNumber = 0;}
    if (inChar == 'W') { target = "WatchDog"; inputNumber = 0;}
    if (inChar == 'V') Serial.println(voltage);
    if (inChar == 'P') Serial.println("Position");
    if (int(inChar) >= 48){ // int(char(48)) = 0
      if (int(inChar) <= 57){ // int(char(57)) = 9
        // add it to the inputNumber
        inputNumber = (inputNumber * 10) + (int(inChar) - 48);
      }
    }

    // if the incoming character is a newline, do something about it:
    if (inChar == 'n') {
       if (target == "LeftMotor"){
          if (LRun < 201){ // Motor Direction change delay
             if (inputNumber > 200) DirectionMillis = millis() + DTime;
          }
          if (LRun > 199){ // Motor Direction change delay
             if (inputNumber < 200) DirectionMillis = millis() + DTime;
          }
          LRun = inputNumber;
       }
       if (target == "RightMotor"){
          if (RRun < 201){ // Motor Direction change delay
             if (inputNumber > 200) DirectionMillis = millis() + DTime;
          }
          if (RRun > 199){ // Motor Direction change delay
             if (inputNumber < 200) DirectionMillis = millis() + DTime;
          }
          RRun = inputNumber;
       }
       
       if (target == "WatchDog"){
          if (inputNumber > 500){ // minimum of 1/2 second for Watch Dog timmer.
             if (inputNumber < 15000) WDog = inputNumber; // maximum of 15 seconds for watchdog timmer
             else Serial.println("error WatchDog");
          }
          else Serial.println("error WatchDog");
       }
       // clear the string:
       inputNumber = 0;
       target = "";
    }
  }
} // end serialEvent()

void loop() {

  // record battery voltage
  voltage = map(analogRead(A0),275,830,100,300);
/*  if (voltage < LowBatt) { // Send error message and stop bot if battery is low.
      Serial.println("error LowBatt");
      LRun = 200;
      RRun = 200;
  }
*/
  if (DirectionMillis > millis()){ // controller switching safty with delayed direction change
      digitalWrite(LFoff, HIGH);
      digitalWrite(LRoff, HIGH);
      digitalWrite(LFPWM, LOW);
      digitalWrite(LRPWM, LOW);
      digitalWrite(RFoff, HIGH);
      digitalWrite(RRoff, HIGH);
      digitalWrite(RFPWM, LOW);
      digitalWrite(RRPWM, LOW);
  } else{
    // Left motor control
    if (LRun == 200) { // stop left motor
    digitalWrite(LFoff, HIGH);
    digitalWrite(LRoff, HIGH);
    digitalWrite(LFPWM, LOW);
    digitalWrite(LRPWM, LOW);
    } else {
      if(LRun < 200){
        digitalWrite(LFoff, HIGH);
        digitalWrite(LRoff, LOW);
        digitalWrite(LRPWM, LOW);
        analogWrite(LFPWM, map(LRun,199,1,MotorMin,255));
      }
      if(LRun > 200){
        digitalWrite(LRoff, HIGH);
        digitalWrite(LFoff, LOW);
        digitalWrite(LFPWM, LOW);
        analogWrite(LRPWM, map(LRun,201,400,MotorMin,255));
      }
    }
    // Right motor control
    if (RRun == 200) { // stop Right motor
    digitalWrite(RFoff, HIGH);
    digitalWrite(RRoff, HIGH);
    digitalWrite(RFPWM, LOW);
    digitalWrite(RRPWM, LOW);
    } else {
      if(RRun < 200){
        digitalWrite(RFoff, HIGH);
        digitalWrite(RRoff, LOW);
        digitalWrite(RRPWM, LOW);
        analogWrite(RFPWM, map(RRun,199,1,MotorMin,255));
      }
      if(RRun > 200){
        digitalWrite(RRoff, HIGH);
        digitalWrite(RFoff, LOW);
        digitalWrite(RFPWM, LOW);
        analogWrite(RRPWM, map(RRun,201,400,MotorMin,255));
      }
    }
  } //  end controller switching safty with delayed direction change
  // Stop if there has been no input for the set amount of time.
  if (WDMillis < millis()){
    LRun = 200;
    RRun = 200;    
  }

} // end loop()
