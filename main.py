# if __name__ == "__main__":
#     from src import ui
#     ui.App().mainloop()



if __name__ == "__main__":
    from src import  ui,sensorListener
    import json
    import time

    LCKMngKey =''
     
    
    from multiprocessing import *

    procs = []

    a= ui.App()
    
    proc1 = Process(target= a.mainloop,args=())
    procs.append(proc1)
    proc1.start()

    while True:
        with open("data/information.json") as f:
            file_read = f.readlines()
            if len(file_read) == 0:
                time.sleep(1)
                continue
            else:
                json_object = json.loads("".join(file_read))
                LCKMngKey = json_object["LCKMngKey"]    
                break

    sListener = sensorListener.sensorListener(0,"/dev/ttyACM0",LCKMngKey)
    #proc2 = Process(target=sensorListener.sensorListener(0,"/dev/ttyACM0","H001234").startListen,args=())
    proc2 = Process(target=sListener.startListen,args=())
    procs.append(proc2)
    proc2.start()

    # for p in procs:
    #     p.start()

    for p in procs:
        p.join()
    