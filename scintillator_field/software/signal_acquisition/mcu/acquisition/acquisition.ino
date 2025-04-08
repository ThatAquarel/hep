// serial communications
// #define DEBUG
#define START_FLAG 0x7E
#define END_FLAG 0x7D

// hardware interrupt
#define TRIGGER 2
volatile bool triggered = false;
#define MANUAL_RESET 3
volatile bool resetted = false;
#define RESET 4

// FPGA data shifting
#define CS 10
#define MISO 12
#define CLK 13

void setup() {
  // Serial communication w/ computer and software
  Serial.begin(115200);

  // hardware interrupt for trigger
  pinMode(TRIGGER, INPUT);
  attachInterrupt(digitalPinToInterrupt(TRIGGER), trigger, RISING);

  // auto reset
  pinMode(MANUAL_RESET, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(MANUAL_RESET), reset, FALLING);

  pinMode(RESET, OUTPUT);
  digitalWrite(RESET, HIGH);

  // FPGA data shifting
  pinMode(CS, OUTPUT);
  digitalWrite(CS, HIGH);

  pinMode(MISO, INPUT);
  pinMode(CLK, OUTPUT);
  digitalWrite(CLK, LOW);
}

void loop() {
  if (triggered) {
    delayMicroseconds(30);
    // Start SPI transaction
    digitalWrite(CS, LOW); // Select FPGA

    uint32_t value = 0;
    for (int i = 0; i < 24; i++) {
      digitalWrite(CLK, HIGH);
      digitalWrite(CLK, LOW);

      value <<= 1;
      value |= digitalRead(MISO);
    }
    
    digitalWrite(CS, HIGH); // Deselect FPGA

#ifdef DEBUG
    Serial.print("TRIGGERED: 0x");
    Serial.println(value, HEX);
#endif
#ifndef DEBUG
    Serial.write(0x00);
    Serial.write(0x00);
    Serial.write(START_FLAG);
    Serial.write((uint8_t*)&value, 4);
    Serial.write(END_FLAG);
    Serial.write(0x00);
    Serial.write(0x00);
#endif

    triggered = false;

    reset();
  }

  if (resetted) {
    digitalWrite(RESET, LOW);
    digitalWrite(RESET, HIGH);
  }
}

void trigger() {
  triggered = true;
}

void reset() {
  resetted = true;
}
