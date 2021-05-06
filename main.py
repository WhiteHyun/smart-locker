if __name__ == "__main__":
    import time
    import json
    from multiprocessing import *
    from src import ui
    from src.utils import sensor_listener

    LCKMngKey = ""

    procs = []

    a = ui.App()

    proc1 = Process(target=a.mainloop, args=())
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

    sListener = sensor_listener.SensorListener(0, "/dev/ttyACM0", LCKMngKey)
    proc2 = Process(target=sListener.listen, args=())
    procs.append(proc2)
    proc2.start()

    # for p in procs:
    #     p.start()

    for p in procs:
        p.join()
