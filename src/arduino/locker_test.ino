#include <Stepper.h>

const int DE = 500;
String LOCKER_KEY = "Hello, World!";
bool isOpen = false;

// pin number may change.
int echoPin = 12;
int trigPin = 13;
//IN1,2,3,4 = 8-11pin
Stepper stepper(DE, 11, 9, 10, 8);

void setup() {
    // put your setup code here, to run once:
    stepper.setSpeed(21);
    Serial.begin(9600);

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

void loop() {
    unsigned long duration;
    float distance;

    // trig핀에 10us만큼 신호가 들어가게 되면 그 다음에 8번의 초음파 발사된다.
    // 초음파를 쏘기 위한 사전 신호!
    digitalWrite(trigPin, HIGH);
    delay(10);
    digitalWrite(trigPin, LOW);

    // echoPin이 HIGH를 유지한 시간을 저장 한다.
    duration = pulseIn(echoPin, HIGH);

    // HIGH 였을 때 시간(초음파가 보냈다가 다시 들어온 시간)을 가지고 거리를 계산 한다.
    distance = duration / 29.0 / 2.0;

    delay(500);

    /* step moter part */
    // 초음파 센서 거리 구분
    if (distance < 10) {
        // 문 여는 시도가 있을 경우
        if (Serial.available() > 0 && Serial.readStringUntil('\n').equals(LOCKER_KEY)) {
            if (!isOpen) {
                stepper.step(DE);
                isOpen = true;
                delay(10000);
            }
        } else {
            if (isOpen) {
                stepper.step(-DE);
                isOpen = false;
                delay(1000);
            }
        }
    }
}
