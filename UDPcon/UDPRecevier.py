from libemg.data_handler import OnlineDataHandler
import numpy as np
import socket
import pickle
import threading
from multiprocessing import Lock
from libemg.shared_memory_manager import SharedMemoryManager
import time

### --- Receptor de datos --- ###
class SensorReceiver:
    def __init__(self, emg_port=50043, channel_list=list(range(8)), buffer_size=2000):
        self.emg_port = emg_port
        self.channel_list = channel_list
        self.emg = True
        self._min_recv_size = 1024
        self._data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._data_socket.bind(('192.168.1.74', emg_port))
        self.signal = threading.Event()
        
        self.shared_memory_items = []
        self.shared_memory_items.append(["emg",       (5000,8), np.double, Lock()])
        self.shared_memory_items.append(["emg_count", (1,1), np.int32, Lock()])
        self.emg_handlers = []

    def add_emg_handler(self, handler):
        self.emg_handlers.append(handler)

    def connect(self):
        print(f"Conectado al puerto UDP {self.emg_port}")

    def cleanup(self):
        self._data_socket.close()
        print("Socket cerrado.")

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
            if self.emg:
                packet, _ = self._data_socket.recvfrom(self._min_recv_size)
                
                #!!!! Si se esta ocupando en localhost
                #data = pickle.loads(packet)

                #!!!! SI es que se está leyendo desde otro dispositivo
                data = np.frombuffer(packet, dtype=np.float64)
                data = data[self.channel_list]
                if len(data.shape) == 1:
                    data = data[None, :]
                for e in self.emg_handlers:
                    e(data)

            if self.signal.is_set():
                self.cleanup()
                break

        print("LibEMG -> DelsysReceiver (proceso finalizado).")


if __name__ == "__main__":
    print("Iniciando Receptor UDP")
    receptor = SensorReceiver()
    receptor_thread = threading.Thread(target=receptor.run)
    receptor_thread.start()

    # Espera a que llegue algo de datos antes de visualizar
    time.sleep(2)

    odh = OnlineDataHandler(shared_memory_items=receptor.shared_memory_items)
    odh.visualize()
    #odh.visualize_heatmap() 

    # Después de cerrar la visualización, detenemos el receptor
    receptor.signal.set()
    receptor_thread.join()
