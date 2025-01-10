#include <Arduino.h>
#include <EEPROM.h>

const int eepromSize = 4096; // Rozmiar pamięci EEPROM w bajtach
int eepromIndex = 0;

void printEEPROM();

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    // Serial.print(c); // Wyświetlanie odczytanych znaków na monitorze szeregowym

    // Zapis do pamięci EEPROM
    if (eepromIndex < eepromSize - 1) {
      EEPROM.write(eepromIndex++, c);
    } else {
      Serial.println("Pamięć EEPROM pełna!");
    }
    if(c == '#')
      printEEPROM();
  }
  delay(100);
}

void printEEPROM() {
  Serial.println("Zawartość pamięci EEPROM:");
  for (int i = 0; i < eepromSize/4; i++) {
    char c = EEPROM.read(i);
    Serial.print(c);
  }
  Serial.println();
}
