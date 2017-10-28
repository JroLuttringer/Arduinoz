#include <Servo.h>
#define DROITE 1
#define GAUCHE 2
Servo myServo;  // create a servo object 

int angle=0;   // variable to hold the angle for the servo motor 

void setup() {
  myServo.attach(3); // attaches the servo on pin 9 to the servo object 
  Serial.begin(9600); // open a serial connection to your computer
  angle = 90;
}

void serialEvent(){
  while(Serial.available()){
    char value = Serial.read();
    Serial.write(value);
    if(value == '1' ){
      angle = min(angle+1,179);
      Serial.write("DROITE");
    }
    else if (value == '2'){
      angle = max(1, angle-1); 
      Serial.write("GAUCHE");
    }
      myServo.write(angle);
  }

}

void loop(){}



