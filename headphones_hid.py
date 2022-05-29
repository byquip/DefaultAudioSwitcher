import hid  # TODO : LIBS IN system32 add
            # TODO: ADD Always powered flag and use:

class Headphones:
    powered: bool = False
    res_cur = None
    res_prev = None
    res_prev_prev = None
    stop = False

    def __init__(self, VID: int, PID: int) -> None:
        self.hp = hid.Device(VID, PID)

    def listen(self) -> None:
        while not self.stop:
            self.res_cur = self.hp.read(1, 500)
            self.check_states()
            self.res_prev_prev = self.res_prev
            self.res_prev = self.res_cur

    def check_states(self) -> None:
        if self.res_prev != b'' and self.res_cur != b'':  # if volume buttons was touched
            self.powered = True
        if self.res_cur == b'' and self.res_prev == b'\x01' and self.res_prev_prev == b'':  # if power was switched off
            self.powered = False

    def stop_loop(self):
        self.stop = True

