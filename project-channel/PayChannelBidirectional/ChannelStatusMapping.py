def get_status(status):
    switcher = {
        0: "Init",
        1: "Open",
        2: "InConflict",
        3: "Settled",
        4: "WaitingToClose",
        5: "ReadyToClose",
    }
    return switcher.get(int(status), "nothing")
