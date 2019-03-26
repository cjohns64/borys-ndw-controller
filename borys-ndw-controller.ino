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
  if (inputDone==1) {
    if (motorSpeed > 0) {
      // index of the command identifiers
      // the index will be -1 if the string does not exist in the input
      int intoIndex = inputString.indexOf(intoRotate);
      int outofIndex = inputString.indexOf(outofRotate);
      int steps = 0;
      String inputStepsStr = "0";
//      Serial.println("in:"+inputString+";");
//      delay(10);
      
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
      else {
//        Serial.println("no direction");
//        delay(10);
      }
      
      if (steps != 0){
        // take the determined number of stepps
        // program will wait for the task to finish before proceding
        motor.step(steps);
        Serial.println("steping" + steps);
        delay(100);
      }
      else {
//        Serial.println("not stepping");
//        delay(10);
      }
    }
    else {
//      Serial.println("motor off");
//      delay(10);
    }
    // reset for next input
    inputDone = 0;
    inputString = "";
  }
  delay(10);
}

void serialEvent() {
  while (Serial.available()){
    // read in the input stream
    char inChar = (char)Serial.read();
    if (inChar != '\n' || inChar != '\r'){
      // not done with the line
      inputString.concat(inChar);
//      Serial.print(inChar + "xx");
    }
    else if (inputString.length() > 0) {
        // line done
        inputDone = 1;
        int startIndex = inputString.indexOf('\t');
//        Serial.print("start index: " + startIndex);
//        delay(10);
        
        // cut out extra and check for valid start and end chars
        int start_input = inputString.indexOf('\t');
        // windows newline is \r\n but mac and linux is \n
        int end_input = inputString.indexOf('\r');
        if (end_input < 0){
          // no windows newline, check for linux
          end_input = inputString.indexOf('\n');
        }
        if (start_input >= 0 && end_input >= 0){
          // we have both the start and end chars, so the input is valid
          inputString = inputString.substring(start_input, end_input);
        }
        else {
          // input is not valid
//          Serial.print("!!Invalid Input!!");
//          delay(10);
          inputString = "";
        }
     }
  }
}
