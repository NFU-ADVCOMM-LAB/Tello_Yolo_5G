class UE:
    def __init__(self):
        import socket
        self.srs_local_ip = self.find_local_addr("172.16.0.x")        
        self.srs_ENB_Addr = ("172.16.0.1", 2000)
        self.srs_Connection_Check()
  
    def find_local_addr(self, network_segment):
        from netifaces import interfaces, AF_INET, ifaddresses
        self.retry_count = 0
        while True:
            process_network_segment = ""
            
            for i in range(0,len(network_segment)):
                if (i != len(network_segment)-1 and i != len(network_segment)-2):
                    process_network_segment += network_segment[i]
            if process_network_segment in ifaddresses("tun_srsue")[AF_INET][0]['addr']:
                if (self.retry_count != 0):
                    print("")
                print("Found local address [{0}]".format(ifaddresses("tun_srsue")[AF_INET][0]['addr']))
                return ifaddresses("tun_srsue")[AF_INET][0]['addr']
            '''
            except:
                self.retry_count += 1
                print(".", end = "")
            '''
    def srs_Connection_Check(self):
        import socket
        TCP_Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            TCP_Client.connect(self.srs_ENB_Addr)
        except:
            pass
        TCP_Client.close()
