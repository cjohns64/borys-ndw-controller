/*
 * Program for rotating the stepper motor in a direction and amount given my ScopeFoundry
 */
#include <Stepper.h>
int stepsPerRevolution = 400;
int motorSpeed = 10;
String StepString = "step";
// initialize the stepper library on pins 8 through 11:
Stepper motor(stepsPerRevolution, 8, 9, 10, 11);

// the string used for serial input
String inputString = "";
char intoRotate = 'i';
char outofRotate = 'o';
boolean inputDone = 0;

boolean DEBUG = false;
int LED1 = 2;  // led for being in the inputDone section
int LED2 = 3;  // led for being in the serialEvent section
int LED3 = 4;  // led for useing stepper motor
int LED4 = 5;  // led for reading input

void setup() {
  if (DEBUG){
    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);
    pinMode(LED3, OUTPUT);
    pinMode(LED4, OUTPUT);
  }
  // set the stepper motor speed
  motor.setSpeed(motorSpeed); // value 0-100
  
  // start the serial port, 
  // initialize to the byte-rate of 57600 -- must be the same as the Python controller
  Serial.begin(57600);
  // wait until serial port is available
  //while (Serial.available() == 0){ }
}

void loop() {
  serial_read();
}

void move_stepper(){
//  inputDone = true;
//  inputString = "o10";
  
  if (inputDone) {
    if (DEBUG){digitalWrite(LED1, HIGH); delay(100);}
    
    if (motorSpeed > 0) {
      // get index of the command identifiers
      // the index will be -1 if the string does not exist in the input
      int intoIndex = inputString.indexOf(intoRotate);
      int outofIndex = inputString.indexOf(outofRotate);
      int steps = 0;
      String inputStepsStr = "0";
      Serial.print("in:"+inputString+";");

      // set steps value
      if (intoIndex >= 0){
        // get number of steps in the into direction
        inputStepsStr = inputString.substring(intoIndex + 1);
        steps = inputStepsStr.toInt();
        steps = -steps;  // fix the direction
      }
      else if (outofIndex >= 0) {
        // get number of steps in the outof direction
        inputStepsStr = inputString.substring(outofIndex + 1);
        steps = inputStepsStr.toInt();
      }
      else {
        Serial.println("no direction");
      }
      
      if (steps != 0){
        if (DEBUG) {digitalWrite(LED3, HIGH); delay(100);}
        
        // take the determined number of stepps
        // program will wait for the task to finish before proceding
        motor.step(steps);
        Serial.println("steping" + String(steps) + ";");
        if (DEBUG) {digitalWrite(LED3, LOW);}
      }
      else {
        Serial.println("not stepping");
      }
    }
    else {
      Serial.println("motor off");
    }
    // reset for next input
    inputDone = false;
    inputString = "";
  }
  if (DEBUG) {digitalWrite(LED1, LOW);}
}

void serial_read() {
  if (DEBUG) {digitalWrite(LED2, HIGH);}
  // read in the input stream
  inputString = Serial.readString();
  if (inputString.length() > 0) {
    if (DEBUG) {digitalWrite(LED4, HIGH); delay(100);}
    // line done
    inputDone = true;
    // cut out extra and check for valid start and end chars
    int start_input = inputString.indexOf('\t');
    // windows newline is \r\n but mac and linux is \n
    int end_input = inputString.indexOf('\r');
    if (end_input < 0){
      // no windows newline, check for linux
      end_input = inputString.indexOf('\n');
    }
    if (start_input >= 0){
      // we have both the start and end chars, so the input is valid
      inputString = inputString.substring(start_input, end_input);
      //Serial.println("Valid Input");
      // command stepper to move
      move_stepper();
    }
    else {
      // input is not valid
      //Serial.println("Invalid Input");
      inputString = "";
    }
  }
  if (DEBUG) {digitalWrite(LED2, LOW); digitalWrite(LED4, LOW);}
}

void serialEvent() {
  
}
