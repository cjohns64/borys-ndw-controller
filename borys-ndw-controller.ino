/*
 * Program for rotating the stepper motor in a direction and amount given my ScopeFoundry
 */
#include <Stepper.h>
int stepsPerRevolution = 400;
int motorSpeed = 1;
String StepString = "step";
// initialize the stepper library on pins 8 through 11:
Stepper motor(stepsPerRevolution, 8, 9, 10, 11);

// the string used for serial input
String inputString = "";
char intoRotate = 'i';
char outofRotate = 'o';

void setup() {
  // set the stepper motor speed
  motor.setSpeed(motorSpeed); // value 0-100
  
  // start the serial port, 
  // initialize to the byte-rate of 57600 -- must be the same as the Python controller
  Serial.begin(57600);
  // wait until serial port is available
  while (Serial.available() == 0){ }
}

void loop() {
  if (motorSpeed > 0) {
    // index of the command identifiers
    // the index will be -1 if the string does not exist in the input
    int intoIndex = inputString.indexOf(intoRotate);
    int outofIndex = inputString.indexOf(outofRotate);
    int steps = 0;
    String inputStepsStr = "0";
    
    if (intoIndex >= 0){
      // get number of steps in the into direction
      inputStepsStr = inputString.substring(intoIndex + 1);
      steps = inputStepsStr.toInt();
    }
    else if (outofIndex >= 0) {
      // get number of steps in the outof direction
      inputStepsStr = inputString.substring(outofIndex + 1);
      steps = inputStepsStr.toInt();
      steps = -steps;  // fix the direction
    }
    
    // take the determined number of stepps
    // program will wait for the task to finish before proceding
    motor.step(steps);
    Serial.println("steping" + steps);
  }
  else {
    Serial.println("no step");
  }
}

void serialEvent() {
  while (Serial.available()){
    // read in the input stream
    char inChar = (char)Serial.read();
    if (inChar != '\n'){
      // not done with the line
      inputString.concat(inChar);
    }
    else {
      // line done
      // cut out extra
      inputString = inputString.substring(inputString.indexOf('\t','\n'));
    }
  }
}
