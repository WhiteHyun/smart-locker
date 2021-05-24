if __name__ == "__main__":
    from time import sleep
    import json
    from multiprocessing import *
    from src import ui
    from src.utils import sensor_listener, locker_state

    LCKMngKey = ""

    procs = []

    app = ui.App()

    proc1 = Process(target=app.mainloop, args=())
    procs.append(proc1)
    proc1.start()

    while not LCKMngKey:
        try:
            with open("data/information.json") as f:
                file_read = f.readlines()
                if not file_read:
                    sleep(1)
                else:
                    json_object = json.loads("".join(file_read))
                    LCKMngKey = json_object["LCKMngKey"]
        except FileNotFoundError as e:
            pass

    sListener = sensor_listener.SensorListener(LCKMngKey)

    proc2 = Process(target=sListener.listen, args=())
    procs.append(proc2)
    proc2.start()

    sBehavior = locker_state.LockerState()

    proc3 = Process(target=sBehavior.check_door, args=())
    procs.append(proc3)
    proc3.start()

    # for p in procs:
    #     p.start()

    for p in procs:
        p.join()
