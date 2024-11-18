#include <Servo.h>

Servo servoX, servoY;
int posX = 90, posY = 90;

// PID değişkenleri
float kp = 1.2, ki = 0.02, kd = 0.6;
float prevErrorX = 0, prevErrorY = 0;
float integralX = 0, integralY = 0;

void setup() {
  servoX.attach(13); // X ekseni servo
  servoY.attach(12); // Y ekseni servo
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    int targetX = data.substring(0, commaIndex).toInt();
    int targetY = data.substring(commaIndex + 1).toInt();

    // Hata hesaplama
    float errorX = targetX - 320; // Kamera merkezi: 320x240
    float errorY = targetY - 240;

    // PID hesaplama
    integralX += errorX;
    integralY += errorY;
    float derivativeX = errorX - prevErrorX;
    float derivativeY = errorY - prevErrorY;

    posX += kp * errorX + ki * integralX + kd * derivativeX;
    posY += kp * errorY + ki * integralY + kd * derivativeY;

    posX = constrain(posX, 0, 180);
    posY = constrain(posY, 0, 180);

    servoX.write(posX);
    servoY.write(posY);

    prevErrorX = errorX;
    prevErrorY = errorY;
  }
}
