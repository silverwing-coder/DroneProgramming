'''
Edited by Sangmork Park, Aug-2024
    -   This c-code is created to demonstrate serial communication between a micro controller and Raspberry Pi.
    -   RPi sends a message -> "Micro controller echo the message" -> RPi receive the message back and print.
'''

String tx_data;

void setup() {
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
  
  // Serial.println("ESP8662 Tx Test");
}


void loop() {

  // send_data_simple();
  receive_data();

}

void send_data_simple() {

  Serial.print("esp_start");
  Serial.print("Tx from ESP6220 ....");
  Serial.println("esp_end");

  delay(10);

}

void receive_data() {

  if (Serial.available() > 0) {
    tx_data = Serial.readStringUntil('\n');
    Serial.print("esp_start");
    Serial.print(tx_data);
    Serial.print(" received and returned ...");
    Serial.print("esp_end");
  }
  delay(10);

}