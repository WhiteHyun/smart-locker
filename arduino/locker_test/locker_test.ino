#include <Stepper.h>

const int DE = 500;
rotate = 0;
//IN1,2,3,4 = 8-11pin

Stepper stepper(DE, 11, 9, 10, 8);

void setup() {
    // put your setup code here, to run once:
    stepper.setSpeed(21);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char buffer = Serial.read();
        if (buffer == 'T') {
            if (rotate) {
                stepper.step(DE);
                rotate = 0;
                delay(1000);
            } else {
                stepper.step(-DE);
                rotate = 1;
                delay(1000);
            }
        } else {
            Serial.print("read: ");
            Serial.println(buffer);
        }
    }
}
