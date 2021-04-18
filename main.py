# if __name__ == "__main__":
#     from src import ui
#     ui.App().mainloop()



if __name__ == "__main__":
    from src import  ui,sensorListener

    
     
    sListener = sensorListener.sensorListener(0,"/dev/ttyACM0","H001234")
    
    from multiprocessing import *

    procs = []

    a= ui.App()
    
    proc1 = Process(target= a.mainloop,args=())
    #proc2 = Process(target=sensorListener.sensorListener(0,"/dev/ttyACM0","H001234").startListen,args=())
    proc2 = Process(target=sListener.startListen,args=())
    procs.append(proc1)
    procs.append(proc2)

    for p in procs:
        p.start()

    for p in procs:
        p.join()
    