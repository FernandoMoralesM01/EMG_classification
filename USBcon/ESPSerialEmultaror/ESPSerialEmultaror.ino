#define NUM_CHANNELS 8        // Número de canales EMG
#define SAMPLING_RATE 1000   // Frecuencia de muestreo en Hz

void setup() {
  Serial.begin(115200);
}

void loop() {
  for (int i = 0; i < NUM_CHANNELS; i++) {
    float emg_value = random(-1000, 1000) / 1000.0;  // Simula señal entre -1.0 y 1.0
    Serial.print(emg_value, 4);  // 4 cifras decimales
    if (i < NUM_CHANNELS - 1) {
      Serial.print(",");  // Separador entre canales
    } else {
      Serial.println();   // Fin de línea al final del vector
    }
  }

  delayMicroseconds(1000000 / SAMPLING_RATE);  // Espera para mantener frecuencia
}
