import socket
import pickle
import time
import numpy as np
import multiprocessing

def delsys_emulator(emg=True, emg_port=50043, aux_port=50044, channel_list=list(range(8)), time_ = None, fs = 1000):
    emg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if emg:
        print("Stream activo")
        if time_  == None:
            while True:
                    emg_data = np.random.randn(len(channel_list)).astype(np.float64)
                    emg_packet = pickle.dumps(emg_data)
                    emg_sock.sendto(emg_packet, ('localhost', emg_port))
                    time.sleep(1/fs)

        else:
            for i in range (time_ * fs):    
                emg_data = np.random.randn(len(channel_list)).astype(np.float64)
                emg_packet = pickle.dumps(emg_data)
                emg_sock.sendto(emg_packet, ('localhost', emg_port))
                time.sleep(1/fs)


delsys_emulator()