import socket
import signal
import threading
import time
import os
from netifaces import interfaces, AF_INET, ifaddresses

class Proxy:
    def __init__(self):
        self.IP_Addr_init()
        self.Sockets_init()
        self.Tello_init()
        self.Thread_init()
    def IP_Addr_init(self):
        # Local IP Address
        self.video_local_ip = self.find_local_addr("192.168.0.x")
        self.tello_local_ip = self.find_local_addr("192.168.10.x")
        self.srs_local_ip = self.find_local_addr("172.16.0.x")
        # Transmit target IP Address
        self.srs_UE_IP = self.srs_Connection_Check()
        self.Tello_IP = "192.168.10.1"
        self.Video_ip = "192.168.0.2"
        self.srs_UE_Addr = (self.srs_UE_IP, 2000)
        self.Video_Addr = (self.Video_ip, 3000)
        self.Tello_Addr = (self.Tello_IP, 8889)
    def Sockets_init(self):
        #srslte Socket
        self.srs_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.srs_socket.bind((self.srs_local_ip,2000))
        #Video Socket(Ethernet)
        self.Video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Video_socket.bind((self.video_local_ip,3000))
        #Tello Sockets
        self.Tello_Command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Tello_Command_socket.bind((self.tello_local_ip,8889))
        self.Tello_Video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Tello_Video_socket.bind((self.tello_local_ip,11111))
    def Tello_init(self):
        self.Tello_Command_socket.sendto(b'command', self.Tello_Addr)
        self.Tello_Command_socket.sendto(b'streamon', self.Tello_Addr)
        #Tello_Command_socket
    def Thread_init(self):
        Transmit = threading.Thread(target = self.Command_Transmit_Thread)
        Transmit.start()
        Video_Transmit = threading.Thread(target = self.Video_Transmit_Thread)
        Video_Transmit.start()
    def find_local_addr(self, network_segment):
        retry_count = 0
        while True:
            process_network_segment = ""
            for i in range(0,len(network_segment)):
                if (i != len(network_segment)-1 and i != len(network_segment)-2):
                    process_network_segment += network_segment[i]
            for ifaceName in interfaces():
                try:
                    if process_network_segment in ifaddresses(ifaceName)[AF_INET][0]['addr']:
                        if (retry_count != 0):
                            print("")
                        print("Found local address [{0}]".format(ifaddresses(ifaceName)[AF_INET][0]['addr']))
                        return ifaddresses(ifaceName)[AF_INET][0]['addr']
                except:
                    retry_count += 1
                    print(".", end = "")
                    time.sleep(0.01)
    def srs_Connection_Check(self):
        TCP_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCP_Server.bind((self.srs_local_ip, 2000))
        TCP_Server.listen(5)
        print('Wait for connection...')
        conn, addr = TCP_Server.accept()
        print("Found UE at [{0}]".format(addr[0]))
        TCP_Server.close()
        return addr[0]
        
    def Command_Transmit_Thread(self):
        while True:
            try:
                data, addr = self.srs_socket.recvfrom(3000)
                self.Tello_Command_socket.sendto(data, self.Tello_Addr)
                data, addr = self.Tello_Command_socket.recvfrom(3000)
                self.srs_socket.sendto(data, self.srs_UE_Addr)
            except:
                pass
    def Video_Transmit_Thread(self):
        while True:
            try:
                data, addr = self.Tello_Video_socket.recvfrom(2048)
                #print(data)
                self.Video_socket.sendto(data, self.Video_Addr)
            except:
                pass

def handler(signum, frame):
    res = input("Do you really want to exit? y/n ")
    if (res == 'y'):
        print("Proxy Service Stopped!!")
        os._exit(0)
if (__name__ == "__main__"):
    ENB_Proxy = Proxy()
    while True:
        signal.signal(signal.SIGINT, handler)
