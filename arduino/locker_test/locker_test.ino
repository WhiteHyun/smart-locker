#include <Stepper.h>

int DE = 700;

//IN1,2,3,4 = 8-11pin


Stepper stepper(DE,11,9,10,8);



void setup() {
  // put your setup code here, to run once:
  stepper.setSpeed(21);
}

void loop() {
  // put your main code here, to run repeatedly:
   stepper.step(DE);
   delay(1000);

   stepper.step(-DE);
   delay(1000);
   


}
