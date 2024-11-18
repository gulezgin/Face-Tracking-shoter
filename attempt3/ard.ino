#include <Servo.h>

Servo servoX;
Servo servoY;

int posX = 90; // Başlangıç pozisyonu
int posY = 90;

void setup() {
  servoX.attach(9);
  servoY.attach(10);
  Serial.begin(9600);
  servoX.write(posX);
  servoY.write(posY);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      int x = data.substring(0, commaIndex).toInt();
      int y = data.substring(commaIndex + 1).toInt();

      // Basit bir servo hareket mantığı
      posX = map(x, 0, 640, 0, 180); // 640, kamera genişliği
      posY = map(y, 0, 480, 0, 180); // 480, kamera yüksekliği
      servoX.write(posX);
      servoY.write(posY);
    }
  }
}
