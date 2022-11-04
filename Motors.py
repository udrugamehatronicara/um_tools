import can
class Motors:
    def __init__(self, bus):
        self.bus = bus
        self.motor_addr = [0x00033C, 0x00033D, 0x00033E, 0x00033F]
        self.last_speeds = None

    def set_speeds(self, speeds):
        self.last_speeds = speeds

        msgs = []
        for s, addr in zip(speeds, self.motor_addr):
            if s < 0:
                speed = (4294967295 + s).to_bytes(4, 'big')
            else:
                speed = s.to_bytes(4, 'big')

            #print(speed)

            msg = can.Message(arbitration_id=addr, data=speed, is_extended_id=True)
            msgs.append(msg)

        for msg in msgs:
            try:
                self.bus.send(msg)
            except can.CanError:
                print("ERROR message not sent", m)