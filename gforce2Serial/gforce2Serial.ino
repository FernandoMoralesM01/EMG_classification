#include <Arduino.h>
#include <gForceAdapter.h>  // Asegúrate de tener esta librería correctamente instalada

#define Timeout 1000
#define gforceSerial Serial2   // Cambia si tu hardware tiene otro puerto serial
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
unsigned long gTimestamp = 0;

void setup()
{
  Serial.begin(115200);         
  gforceSerial.begin(115200);   

  gforce.Init(); // Inicialización del adaptador
  Serial.println("Inicializado gForce. Esperando datos EMG...");
  gTimestamp = millis();
}

void loop()
{
  GF_Data gForceData;

  if (GF_RET_OK == gforce.GetGForceData(&gForceData, 10))
  {
    switch (gForceData.type)
    {
    case GF_Data_Type::GF_QUATERNION:
      if (millis() - gTimestamp > 50)
      {
        gTimestamp = millis();
    //    Serial.println("Recibiendo quaternion, comunicación normal.");
      }
    //break;

    case GF_Data_Type::GF_EMGRAW:
    {
      //Serial.println("CASO");
      GF_Emgraw emgrawData = gForceData.value.emgrawData;

      //Serial.print("EMGRAW: ");
      for (int i = 0; i < NUM_CHANNELS; i++)
      for( int i = 0; emgrawData.raw[i] != '\0', i++ )
      {
        Serial.print(emgrawData.raw[i]);
        if (i < NUM_CHANNELS - 1)
          Serial.print(", ");
      }
      Serial.println();
      break;
    }

    default:
      break;
    }
  }
}

