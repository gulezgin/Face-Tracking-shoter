#include <Servo.h> 

// Servo kontrol nesnesi
Servo servo;

// Kullanıcıdan gelen veri için değişkenler
const int START_BYTE = 255;  // Veri paketinin başlangıç baytı
int userInput[2];            // Gelen veri paketinin 2 baytlık kısmı
int servoAngle = 90;         // Servo motorun başlangıç açısı (orta pozisyon)

// Servo pals aralığı (mikrosaniye)
const int MIN_PULSE = 600;   // Minimum servo pals genişliği
const int MAX_PULSE = 2400;  // Maksimum servo pals genişliği

// Seri bağlantı hızı
const int BAUD_RATE = 9600;  // Seri bağlantı hızı (bps)

void setup() 
{   
    // Servo motoru 9. pine bağla ve pals genişliğini ayarla
    servo.attach(9, MIN_PULSE, MAX_PULSE);
    // Seri iletişimi başlat
    Serial.begin(BAUD_RATE); 
} 

void loop() 
{ 
    // Seri portta en az 3 baytlık veri varsa işleme başla
    if (Serial.available() >= 3) 
    {
        // Veri paketinin başlangıç baytını oku
        int startByte = Serial.read();

        // Başlangıç baytı doğruysa devam et
        if (startByte == START_BYTE) 
        {
            // Kullanıcıdan gelen 2 baytlık veriyi oku
            userInput[0] = Serial.read(); // Servo numarası (tek servo olduğu için kullanılmıyor)
            userInput[1] = Serial.read(); // Hedef pozisyon komutu
            
            // Pozisyon komutunu işle
            handlePositionCommand(userInput[1]);
        }
    }
}

// Pozisyon komutlarını işleyen yardımcı fonksiyon
void handlePositionCommand(int positionCommand)
{
    if (positionCommand == 1) 
    {
        // Açıyı 3 derece artır ve sınırları aşmamasını sağla
        servoAngle = constrain(servoAngle + 3, 0, 180);
        servo.write(servoAngle);
    } 
    else if (positionCommand == 2) 
    {
        // Açıyı 3 derece azalt ve sınırları aşmamasını sağla
        servoAngle = constrain(servoAngle - 3, 0, 180);
        servo.write(servoAngle);
    }
}
