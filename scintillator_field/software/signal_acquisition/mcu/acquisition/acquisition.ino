#include <SPI.h>

// hardware interrupt
#define TRIGGER 2
volatile bool triggered = false;

// FPGA data shifting
#define CS 10

void setup() {
  // Serial communication w/ computer and software
  Serial.begin(115200);

  // hardware interrupt for trigger
  pinMode(TRIGGER, INPUT);
  attachInterrupt(digitalPinToInterrupt(TRIGGER), trigger, FALLING);

  // FPGA data shifting
  SPI.begin();
  pinMode(CS, OUTPUT);
  digitalWrite(CS, HIGH);

  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
}

void loop() {
  if (triggered) {
    // Start SPI transaction
    digitalWrite(CS, LOW); // Select FPGA
    
    // Read 3 bytes (24 bits)
    uint8_t byte1 = SPI.transfer(0x00);
    uint8_t byte2 = SPI.transfer(0x00);
    uint8_t byte3 = SPI.transfer(0x00);

    digitalWrite(CS, HIGH); // Deselect FPGA

    // Combine bytes into a 24-bit value
    uint32_t data = ((uint32_t)byte1 << 16) | ((uint32_t)byte2 << 8) | byte3;

    Serial.print("Received 24-bit data: 0x");
    Serial.println(data, HEX);

    triggered = false;
  }
}

void trigger() {
  triggered = true;
}
