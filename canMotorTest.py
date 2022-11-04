import can
import time

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

            print(speed)

            msg = can.Message(arbitration_id=addr, data=speed, is_extended_id=True)
            msgs.append(msg)

        for msg in msgs:
            try:
                self.bus.send(msg)
            except can.CanError:
                print("ERROR message not sent", m)
if __name__ == "__main__":
    DO_SINGLE = False
    bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate='500000')
    motors = Motors(bus)
    sleepTime = 0.05
    step = 2000
    maxspeed = 50000
    
    if DO_SINGLE:
        print("Single motor test starting ...")
        for mIndex in range(4):

            print(f"Motor {mIndex} direction 1")
            speeds = [0,0,0,0]
            for i in range(0, maxspeed, step):
                speeds[mIndex] = i
                motors.set_speeds(speeds)
                time.sleep(sleepTime)
                print(f"Motor {mIndex} direction 1 speed: {speeds}")

            speeds = [0,0,0,0]
            for i in range(maxspeed, 0, -step):
                speeds[mIndex] = i
                motors.set_speeds(speeds)
                time.sleep(sleepTime)
                print(f"Motor {mIndex} direction 1 speed: {speeds}")

            print(f"Motor {mIndex} direction 0")
            speeds = [0,0,0,0]
            for i in range(0, maxspeed, step):
                speeds[mIndex] = -i
                motors.set_speeds(speeds)
                time.sleep(sleepTime)
                print(f"Motor {mIndex} direction 0 speed: {speeds}")

            speeds = [0,0,0,0]
            for i in range(maxspeed, 0, -step):
                speeds[mIndex] = -i
                motors.set_speeds(speeds)
                time.sleep(sleepTime)
                print(f"Motor {mIndex} direction 0 speed: {speeds}")

    print("All 4 motors test starting...")

    print(f"direction 1")
    for i in range(0, maxspeed, step):
        speeds = [i]*4
        motors.set_speeds(speeds)
        time.sleep(sleepTime)
        print(f"All motors direction 1 speed: {speeds}")

    for i in range(maxspeed, 0, -step):
        speeds = [i]*4
        motors.set_speeds(speeds)
        time.sleep(sleepTime)
        print(f"All motors direction 1 speed: {speeds}")

    speeds = [0]*4
    motors.set_speeds(speeds)

    time.sleep(3)
    print(f"direction 0")
    for i in range(0, maxspeed, step):
        speeds = [-i]*4
        motors.set_speeds(speeds)
        time.sleep(sleepTime)
        print(f"All motors direction 0 speed: {speeds}")

    for i in range(maxspeed, 0, -step):
        speeds = [-i]*4
        motors.set_speeds(speeds)
        time.sleep(sleepTime)
        print(f"All motors direction 0 speed: {speeds}")

    speeds = [0]*4
    motors.set_speeds(speeds)
