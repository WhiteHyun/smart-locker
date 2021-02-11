#include <Stepper.h>

const int DE = 500;
int rotate = 0;
//IN1,2,3,4 = 8-11pin
// pin number may change.
int echoPin = 12;
int trigPin = 13;

Stepper stepper(DE, 11, 9, 10, 8);

void setup() {
    // put your setup code here, to run once:
    stepper.setSpeed(21);
    Serial.begin(9600);

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

void loop() {
    // 초음파를 보낸다. 다 보내면 echo가 HIGH 상태로 대기하게 된다.
    digitalWrite(trig, LOW);
    digitalWrite(echo, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);

    // echoPin 이 HIGH를 유지한 시간을 저장 한다.
    unsigned long duration = pulseIn(echoPin, HIGH);
    // HIGH 였을 때 시간(초음파가 보냈다가 다시 들어온 시간)을 가지고 거리를 계산 한다.
    float distance = ((float)(340 * duration) / 10000) / 2;

    Serial.print(distance);
    Serial.println("cm");
    // 수정한 값을 출력
    delay(500);

    //
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
            // code for test
            Serial.print("read: ");
            Serial.println(buffer);
        }
    }
}
