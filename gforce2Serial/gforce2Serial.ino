#include <Arduino.h>
#include <gForceAdapter.h>  // Asegúrate de tener esta librería correctamente instalada

#define Timeout 1000
#define gforceSerial Serial2 
#define NUM_CHANNELS 8

// Función para obtener un carácter desde el puerto serial
int SYS_GetChar(unsigned char *data)
{
  int ret = gforceSerial.read();
  if (ret == -1)
    return 0;
  *data = (unsigned char)ret;
  return 1;
}

// Función para obtener el tiempo del sistema
unsigned long SYS_GetTick(void)
{
  return millis();
}

// Instancia del adaptador gForce
GForceAdapter gforce(SYS_GetChar, SYS_GetTick);
//unsigned long gTimestamp = 0;

void setup()
{
  Serial.begin(250000);         
  gforceSerial.begin(115200);   

  gforce.Init(); // Inicialización del adaptador
  //Serial.println("Inicializado gForce. Esperando datos EMG...");
  //gTimestamp = millis();
}

void loop()
{
  GF_Data gForceData;

  if (GF_RET_OK == gforce.GetGForceData(&gForceData, 10))
  {
    GF_Emgraw emgrawData = gForceData.value.emgrawData;
    for( int i = 0; i < NUM_CHANNELS ;i++ )
      {
        Serial.print(emgrawData.raw[i]);
        if (i < NUM_CHANNELS - 1)
          Serial.print(",");
      }
    Serial.println();

  }
}

