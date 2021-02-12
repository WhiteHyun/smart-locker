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
    String url;
    const float distance = getDistanceForMicroSonic();
    delay(500);

    if (Serial.available() > 0)
        url = Serial.readStringUntil('\n');

    interactLocker(distance, url);
}

/*
 * 초음파 센서를 이용하여 거리 계산하고 그 값을 반환합니다.
 */
float getDistanceForMicroSonic() {
    unsigned long duration;

    // trig핀에 10us만큼 신호가 들어가게 되면 그 다음에 8번의 초음파 발사된다.
    // 초음파를 쏘기 위한 사전 신호!
    digitalWrite(trigPin, HIGH);
    delay(10);
    digitalWrite(trigPin, LOW);

    // echoPin이 HIGH를 유지한 시간을 저장 한다.
    duration = pulseIn(echoPin, HIGH);

    // HIGH 였을 때 시간(초음파가 보냈다가 다시 들어온 시간)을 가지고 거리를 계산 한다.
    return duration / 29.0 / 2.0;
}

/*
 * 문과 상호작용하는 함수.
 * 
 * 
 * Attributes:
 *      distance (float): 문과 센서와의 거리
 *      url (String): 함과 상호동작시키기 위해 라즈베리파이에서 받아온 값
 * 
 * Return:
 *      bool: 성공적으로 수행되거나 실패했을 경우 리턴됨
 */
bool interactLocker(const float distance, const String url) {
    if (distance < 10) {
        if (Serial.available() > 0 && url.equals(LOCKER_KEY)) {
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
    } else {
        if (!isOpen) {
            /* 절대 들어오면 안되는 루프 */
            Serial.println("******************DANGEROUS******************");
        }
    }
}