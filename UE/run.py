import tello
import threading
from tello_control_ui import TelloUI
from UE_Addon import UE

def main():
    UE_init = UE()
    drone = tello.Tello(UE_init.srs_local_ip,2000)
    vplayer = TelloUI(drone,"./img/","./Yolov5_Test.pt")
    vplayer.root.mainloop()

if __name__ == "__main__":
    main=threading.Thread(target=main,args=())
    main.daemon=True
    main.start()
    main.join()
