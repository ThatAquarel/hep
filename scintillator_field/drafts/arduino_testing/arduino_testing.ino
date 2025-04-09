#define START_FLAG 0x7E
#define END_FLAG 0x7D

void setup()
{
    Serial.begin(115200);
}

void send_packet(uint32_t value)
{
    Serial.write(0x00);
    Serial.write(0x00);
    Serial.write(START_FLAG);
    Serial.write((uint8_t*)&value, 4);
    Serial.write(END_FLAG);
    Serial.write(0x00);
    Serial.write(0x00);
}

uint32_t state_0 = 0b01010101010101010101010101010101;
uint32_t state_1 
{
    send_packet(state_0);
    delay(0.1);
    send_packet(state_1);
    delay(0.1);
    send_packet(state_2);
    delay(0.1);
    send_packet(state_3);
    delay(0.1);
}= 0b10101010101010101010101010101010;
uint32_t state_2 = 0b01010101010101011010101010101010;
uint32_t state_3 = 0b10101010101010100101010101010101;

void loop()
{
    send_packet(state_0);
    delay(0.1);
    send_packet(state_1);
    delay(0.1);
    send_packet(state_2);
    delay(0.1);
    send_packet(state_3);
    delay(0.1);
}
