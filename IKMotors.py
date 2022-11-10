import can
import numpy as np
class IKMotors:
    def __init__(self, bus):
        self.bus = bus
        self.motor_addr = [0x00033C, 0x00033D, 0x00033E, 0x00033F]
        self.last_speeds = None
        R = 1

        add = -np.pi/2
        a1, a2, a3, a4 = np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4
        a1 += add
        a2 += add
        a3 += add
        a4 += add

        self.IK = np.array([
                [np.sin(a1), np.cos(a1), R],
                [np.sin(a2), np.cos(a2), R],
                [np.sin(a3), np.cos(a3), R],
                [np.sin(a4), np.cos(a4), R]
                ]) * (1/R)

    def set_speeds(self, speeds):

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

    def get_speeds(self, Vx, Vy, theta):
       speeds = self.IK @ np.array([Vx, Vy, theta]) 
       #print(Vx, Vy, theta, speeds)
       return speeds
