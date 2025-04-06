// #include <SPI.h>

// hardware interrupt
#define TRIGGER 2
volatile bool triggered = false;

// FPGA data shifting
#define CS 10
#define MISO 12
#define CLK 13

void setup() {
  // Serial communication w/ computer and software
  Serial.begin(115200);

  // hardware interrupt for trigger
  pinMode(TRIGGER, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(TRIGGER), trigger, FALLING);

  // FPGA data shifting
  // SPI.begin();
  pinMode(CS, OUTPUT);
  digitalWrite(CS, HIGH);

  pinMode(MISO, INPUT);
  pinMode(CLK, OUTPUT);
  digitalWrite(CLK, LOW);

  // SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
}

void loop() {
  if (triggered) {
    // Start SPI transaction
    digitalWrite(CS, LOW); // Select FPGA

    uint32_t value = 0;
    for (int i = 0; i < 24; i++) {
      digitalWrite(CLK, HIGH);
      digitalWrite(CLK, LOW);

      value <<= 1;
      value |= digitalRead(MISO);
    }
    
    // Read 3 bytes (24 bits)
    // uint8_t byte1 = SPI.transfer(0x00);
    // uint8_t byte2 = SPI.transfer(0x00);
    // uint8_t byte3 = SPI.transfer(0x00);

    digitalWrite(CS, HIGH); // Deselect FPGA

    // // Combine bytes into a 24-bit value
    // uint32_t data = ((uint32_t)byte1 << 16) | ((uint32_t)byte2 << 8) | byte3;

    // Serial.print("Received 24-bit data: 0x");
    // Serial.println(data, HEX);

    Serial.print("TRIGGERED: 0x");
    Serial.println(value, HEX);

    triggered = false;
  }
}

void trigger() {
  triggered = true;
}
