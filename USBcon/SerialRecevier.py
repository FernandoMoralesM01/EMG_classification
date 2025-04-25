from libemg.data_handler import OnlineDataHandler
import numpy as np
import serial
import threading
import time
from multiprocessing import Lock
from libemg.shared_memory_manager import SharedMemoryManager

### --- Receptor de datos desde Serial --- ###
class SensorReceiverSerial:
    def __init__(self, port='COM3', baudrate=115200, channel_list=list(range(8)), buffer_size=2000):
        self.port = port
        self.baudrate = baudrate
        self.channel_list = channel_list
        self.buffer_size = buffer_size
        self.signal = threading.Event()
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)

        self.shared_memory_items = []
        self.shared_memory_items.append(["emg",       (5000,8), np.double, Lock()])
        self.shared_memory_items.append(["emg_count", (1,1), np.int32, Lock()])
        self.emg_handlers = []

    def add_emg_handler(self, handler):
        self.emg_handlers.append(handler)

    def connect(self):
        print(f"Conectado al puerto SERIAL {self.port} con baudrate {self.baudrate}")

    def cleanup(self):
        self.ser.close()
        print("Puerto serial cerrado.")

    def run(self):
        self.smm = SharedMemoryManager()
        for item in self.shared_memory_items:
            self.smm.create_variable(*item)

        def write_emg(emg):
            self.smm.modify_variable("emg", lambda x: np.vstack((np.flip(emg, 0), x))[:x.shape[0], :])
            self.smm.modify_variable("emg_count", lambda x: x + emg.shape[0])

        self.add_emg_handler(write_emg)
        self.connect()

        while True:
            if self.ser.in_waiting:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    # Esperando líneas tipo: "0.12,0.23,0.01,0.34,..."
                    str_values = line.split(',')
                    if len(str_values) >= len(self.channel_list):
                        values = np.array([float(str_values[i]) for i in self.channel_list])
                        data = values[None, :]
                        for e in self.emg_handlers:
                            e(data)
                except Exception as e:
                    print(f"Error al leer datos seriales: {e}")

            if self.signal.is_set():
                self.cleanup()
                break

        print("LibEMG -> SensorReceiverSerial (proceso finalizado).")


if __name__ == "__main__":
    print("Iniciando Receptor Serial")
    receptor = SensorReceiverSerial()
    receptor_thread = threading.Thread(target=receptor.run)
    receptor_thread.start()

    time.sleep(2)  # Espera a que haya datos en memoria

    odh = OnlineDataHandler(shared_memory_items=receptor.shared_memory_items)
    odh.visualize()

    receptor.signal.set()
    receptor_thread.join()
