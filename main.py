if __name__ == "__main__":
    import time
    import json
    from multiprocessing import *
    from src import ui
    from src.utils import sensor_listener, discriminate

    LCKMngKey = ""

    procs = []

    a = ui.App()

    proc1 = Process(target=a.mainloop, args=())
    procs.append(proc1)
    proc1.start()

    while True:
        with open("data/information.json") as f:
            file_read = f.readlines()
            if not file_read:
                time.sleep(1)
                continue
            else:
                json_object = json.loads("".join(file_read))
                LCKMngKey = json_object["LCKMngKey"]
                break

    sListener = sensor_listener.SensorListener(0, "/dev/ttyARDMR")

    proc2 = Process(target=sListener.listen, args=())
    procs.append(proc2)
    proc2.start()

    sBehavior = discriminate.Discriminate()

    proc3 = Process(target=sBehavior.check_door, args=())
    procs.append(proc3)
    proc3.start()

    # for p in procs:
    #     p.start()

    for p in procs:
        p.join()
