import time
import can
from JoyStick import JoyStick
from IKMotors import IKMotors

bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate='500000')
bus.flush_tx_buffer()
ik = IKMotors(bus)

period = 0.001
startTime = time.time()
speeds = [0]*4

cwAxis = 0
ccwAxis = 0
jX = 0
jY = 0
tdata = [jX, jY, cwAxis, ccwAxis]


tagetSpeeds = [0]*4
speeds = [0]*4
step = 5
js = JoyStick()
t, q = js.start()
maxspeed = 50000
maxrotspeed = 5000

while True:
    #evbuf = jsdev.read(8)
    if not q.empty():
        tdata = q.get()
        print(tdata)
        #print(tdata)
    try:
        if time.time() - startTime >= period:
            jX, jY, cwAxis, ccwAxis = tdata[0], tdata[1], tdata[2], tdata[3]
            startTime = time.time()

            rot = int((cwAxis-ccwAxis))

            jX = 0 if abs(jX) < 0.5 else jX
            jY = 0 if abs(jY) < 0.5 else jY

            targetSpeeds = ik.get_speeds(jX, jY, rot) * maxspeed

            for i in range(4):
                if targetSpeeds[i] > 0 and speeds[i] < targetSpeeds[i]:
                    speeds[i] += step
                elif targetSpeeds[i] < 0 and speeds[i] > targetSpeeds[i]:
                    speeds[i] -= step
                elif targetSpeeds[i] == 0:
                    if speeds[i] > targetSpeeds[i]:
                        speeds[i] -= step
                    elif speeds[i] < targetSpeeds[i]:
                        speeds[i] += step
            ik.set_speeds(speeds)

            
    except KeyboardInterrupt:
        js.stop()
        break
