const int FIRST_LED = 23;
const int SECOND_LED = 22;
const int THIRD_LED = 21;
const int FOURTH_LED = 19;
const int FIFTH_LED = 18;

// LED ORDER
const int LEDS[] = {FIRST_LED, SECOND_LED, THIRD_LED, FOURTH_LED, FIFTH_LED};

char c;
char str[6]; // Holds all the on/off values + null terminator
uint8_t idx = 0;

void setup() {
  Serial.begin(115200); // General ESP32 baudrate
  pinMode(FIRST_LED, OUTPUT);
  pinMode(SECOND_LED, OUTPUT);
  pinMode(THIRD_LED, OUTPUT);
  pinMode(FOURTH_LED, OUTPUT);
  pinMode(FIFTH_LED, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    c = Serial.read(); // Reads one character at a time

    // Add each character to the string
    if (c != '\n') {
      str[idx++] = c;
    } else { // When all characters are read, end the string and reset idx
      str[idx] = '\0';
      idx = 0;

      for (int i = 0; i < 5; i++) {
        digitalWrite(LEDS[i], str[i] - '0'); // Turn char into int and turn on/off the corresponding leds
      }
    }
  }
}
