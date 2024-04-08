#define CLK1 2 //encoder CLK input
#define CLK2 3 //encoder CLK input
#define DT1 4  //encoder DT input
#define DT2 5  //encoder DT input
#define SW1 A2 // A2/16 proximity switch to set encoder home.
#define SW2 A3 // proximity switch to set encoder home.
#define M1A 9//turn motor output 1
#define M1B 8//turn motor output 2
#define M2A 7//turn motor output 1
#define M2B 6//turn motor output 2

int switchAngle = -50;   // =angle of switch (5 DEG. PAST 0 ANGLE)
int angleAccuracy = 10;   // this is the accuracy needed for stearing =accuracy/360*encoderCount/2   
int setAngleLF = 900;      // INTEGER THAT IS 10 TIMES TRUE ANGLE
int counter1 = 10000; // for homing purposes set at 10000
int setAngleRF = setAngleLF;      // INTEGER THAT IS 10 TIMES TRUE ANGLE
int counter2 = counter1; // for homing purposes set at 10000
int joyBuff = 20;  // buffer to create dead space in joystick center
int angle = setAngleLF;
int setAngleLR = setAngleLF;
int setAngleRR = setAngleLF;
int thr = 0;  // throttle output
    
void setup() {

  Serial.begin(115200);           // start serial
          
  pinMode(CLK1,INPUT_PULLUP);
  pinMode(DT1,INPUT);  
  pinMode(M1A, OUTPUT);
  pinMode(M1B, OUTPUT);
  pinMode(CLK2,INPUT_PULLUP);
  pinMode(DT2,INPUT);  
  pinMode(M2A, OUTPUT);
  pinMode(M2B, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(CLK1), encoder1, RISING);
  attachInterrupt(digitalPinToInterrupt(CLK2), encoder2, RISING);

  digitalWrite(M1A, LOW);digitalWrite(M1B, LOW);
  digitalWrite(M2A, LOW);digitalWrite(M2B, LOW);
  
  Serial.println("*** HOMING **** STEARING POSITION");
  delay(2000);
} //END setup()



void encoder1() {
    if (digitalRead(DT1)) {counter1 ++;} else {counter1 --;}
} //END encoder1()

void encoder2() {  
    if (digitalRead(DT2)) {counter2 ++;} else {counter2 --;}
} //END encoder2()

void loop() {

// Set angle with read switch input
  if(analogRead(SW1) > 100) counter1 = switchAngle;
  if(analogRead(SW2) > 100) counter2 = switchAngle;
  
//turn to requested angle MOTOR1
if(counter1 > setAngleLR + angleAccuracy){
    digitalWrite(M1A, LOW);digitalWrite(M1B, HIGH);
}else{
    if(counter1 < setAngleLR - angleAccuracy){
        digitalWrite(M1A, HIGH); digitalWrite(M1B, LOW);
    }else{
        digitalWrite(M1A, LOW);digitalWrite(M1B, LOW);
    }
}//END turn to requested angle MOTOR1
  
//turn to requested angle MOTOR2
if(counter2 > setAngleRR + angleAccuracy){
    digitalWrite(M2A, LOW);digitalWrite(M2B, HIGH);
}else{
    if(counter2 < setAngleRR - angleAccuracy){
        digitalWrite(M2A, HIGH); digitalWrite(M2B, LOW);
    }else{
        digitalWrite(M2A, LOW);digitalWrite(M2B, LOW);
    }
}//END turn to requested angle MOTOR2      

// JOYSTICK **************
thr =map(analogRead(A7),0,1025,255,-255); // read turn input
if(thr > joyBuff)analogWrite(11, thr); else analogWrite(11, 0);

angle = map(analogRead(A6),0,1025,1700,100); // read turn input
if(angle < 901){
    setAngleLF = angle;
    if(setAngleLF < 0)setAngleLF = 0;    // over turn saftey
    if(setAngleLF > 1800)setAngleLF = 1800;// over turn saftey
    //if(analogRead(A5) < 150)setAngleLF = 900; // pushbutton set to 90.
    if(setAngleLF > 900-joyBuff && setAngleLF < 900+joyBuff){// use buffer to trim drive center
        setAngleLF = 900;
        setAngleRF = 900; 
    }else{
        setAngleRF = abs(atan(((tan((setAngleLF/10)*3.14159/180)*21.5)+40)/21.5)*180/3.14159)*10;
    }
}else{
    setAngleRF = angle;
    if(setAngleRF < 0)setAngleRF = 0;    // over turn saftey
    if(setAngleRF > 1800)setAngleRF = 1800;// over turn saftey
    //if(analogRead(A5) < 150)setAngleRF = 900; // pushbutton set to 90.
    if(setAngleRF > 900-joyBuff && setAngleRF < 900+joyBuff){// use buffer to trim drive center
        setAngleLF = 900;
        setAngleRF = 900; 
    }else{
        setAngleLF = map(abs(atan(((tan((setAngleRF/10)*3.14159/180)*21.5)+40)/21.5)*180/3.14159)*10,0,1800,1800,0);
    }  
}
setAngleLR = map(setAngleLF,0,1800,1800,0);
setAngleRR = map(setAngleRF,0,1800,1800,0);
Serial.print(setAngleLR);
Serial.print("  /  ");
Serial.println(setAngleRR);

}//END loop() ******
