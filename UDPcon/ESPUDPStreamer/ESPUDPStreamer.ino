#include <WiFi.h>
#include <WiFiUdp.h>

// Configuración Wi-Fi
const char* ssid = "INFINITUM9A90";
const char* password = "DJag9JyC6c";

// Configuración UDP
WiFiUDP udp;
const char* udpAddress = "192.168.1.74"; // IP del receptor (cambia a la IP de tu PC)
const int udpPort = 50043;

// Configuración de señal
const int num_channels = 8;
double emg_data[num_channels];  // double = float64
const int fs = 1000;            // Frecuencia de muestreo en Hz
unsigned long lastSendTime = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado. Dirección IP: " + WiFi.localIP().toString());
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastSendTime >= 1000 / fs) {
    lastSendTime = currentTime;

    // Generar datos aleatorios entre -1.0 y 1.0
    for (int i = 0; i < num_channels; i++) {
      emg_data[i] = ((double)random(-1000, 1000)) / 1000.0;
    }

    // Enviar datos como binario
    udp.beginPacket(udpAddress, udpPort);
    udp.write((uint8_t*)emg_data, sizeof(emg_data));
    udp.endPacket();
  }
}
