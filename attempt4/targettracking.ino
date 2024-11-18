#include <Servo.h>

Servo servoX, servoY;
int posX = 90, posY = 90;

// PID parametreleri
float kp = 0.5, ki = 0.01, kd = 0.1;
float prev_errorX = 0, prev_errorY = 0;
float integralX = 0, integralY = 0;

void setup() {
  servoX.attach(9);
  servoY.attach(10);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      int targetX = data.substring(0, commaIndex).toInt();
      int targetY = data.substring(commaIndex + 1).toInt();

      // Hata hesaplama
      float errorX = targetX - 320; // 320, ekranın yatay merkezi
      float errorY = targetY - 240; // 240, ekranın dikey merkezi

      // PID hesaplama
      integralX += errorX;
      integralY += errorY;
      float derivativeX = errorX - prev_errorX;
      float derivativeY = errorY - prev_errorY;

      posX += kp * errorX + ki * integralX + kd * derivativeX;
      posY += kp * errorY + ki * integralY + kd * derivativeY;

      // Servo sınırlarını kontrol et
      posX = constrain(posX, 0, 180);
      posY = constrain(posY, 0, 180);

      servoX.write(posX);
      servoY.write(posY);

      prev_errorX = errorX;
      prev_errorY = errorY;
    }
  }
}
