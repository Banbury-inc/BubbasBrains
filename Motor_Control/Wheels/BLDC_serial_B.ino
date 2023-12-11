/*
  BubbaBot Motor control
*/
int LPWM = 3;         // Left motor PWM pin
int RPWM = 9;         // Right motor PWM pin
int minPWM = 100;     // minimum pwm signal
int maxPWM = 150;     // max pwm signal
int Ldir = 11;        // Left motor diection pin
int Rdir = 12;        // Right motor direction pin
int rangeLow = 1;     // input range for drive always starts at 1
int rangeStop = 5;    // stop position for inputs
int rangeHigh = (rangeStop - rangeLow) + rangeStop; // calculate the input range for the drive
int LRun = rangeStop; // how fast the left motor runs ******** SET THIS VARIABLE TO THE STOP NUMBER TO USE **************
int RRun = rangeStop; // how fast the left motor runs and it what direction (1-4 reverse / 5 stop / 6-9 forward)
int DTime = 500;      // Amount of time required at stop before changing direction of a drive motor. (Milliseconds)
unsigned long DirectionMillis = 0;  // data timmer
char inChar;          // incoming data
char target = 'N';    // data target
int inputNumber = 0;  //to hold incoming data

void setup() {
  // initialize serial:
  Serial.begin(115200); 
 
  digitalWrite(Ldir, LOW);
  digitalWrite(Rdir, LOW);
  analogWrite(LPWM, minPWM);  
  analogWrite(RPWM, minPWM);
  delay(2000);
} // end setup()


void loop() {
// serial input  *************************************************************************    
 while (Serial.available()) {
  inChar = (char)Serial.read();
    if (target == 'N') { target = inChar;
    } else {
      if (target == 'L') {
        inputNumber = int(inChar) - 48;
        if (LRun < rangeStop + 1) if (inputNumber > rangeStop) DirectionMillis = millis() + DTime;
        if (LRun > rangeStop - 1) if (inputNumber < rangeStop) DirectionMillis = millis() + DTime;
        LRun = inputNumber;      
      }
      if (target == 'R') {
        inputNumber = int(inChar) - 48;
        if (RRun < rangeStop + 1) if (inputNumber > rangeStop) DirectionMillis = millis() + DTime;
        if (RRun > rangeStop - 1) if (inputNumber < rangeStop) DirectionMillis = millis() + DTime;
        RRun = inputNumber;      
      }
      target = 'N';
    }
 }  
// END serial input *************************************************************************   
if (DirectionMillis > millis()){ // controller switching safty with delayed direction change
    analogWrite(LPWM, minPWM);  
    analogWrite(RPWM, minPWM);
    if(LRun < rangeStop) digitalWrite(Ldir, HIGH); else digitalWrite(Ldir, LOW);
    if(RRun < rangeStop) digitalWrite(Rdir, HIGH); else digitalWrite(Rdir, LOW);
  } else{ // When not changing direction run motors at set speed 
    // Left motor control
    if (LRun == rangeStop) analogWrite(LPWM, minPWM);  
    if (LRun < rangeStop) analogWrite(LPWM, map(LRun,rangeStop,rangeLow,minPWM,maxPWM));
    if (LRun > rangeStop) analogWrite(LPWM, map(LRun,rangeStop,rangeHigh,minPWM,maxPWM));
   // Right motor control
    if (RRun == rangeStop) analogWrite(RPWM, minPWM);  
    if (RRun < rangeStop) analogWrite(RPWM, map(RRun,rangeStop,rangeLow,minPWM,maxPWM));
    if (RRun > rangeStop) analogWrite(RPWM, map(RRun,rangeStop,rangeHigh,minPWM,maxPWM));
  }
} // end loop()
