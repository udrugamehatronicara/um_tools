import time
import queue
import can
import numpy as np
from Motors import Motors
import os, struct, array
from fcntl import ioctl
from threading import Thread, Event

# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'throttle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# Get the device name.
#buf = bytearray(63)
buf = array.array('B', [0] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

print('%d axes found: %s' % (num_axes, ', '.join(axis_map)))
print('%d buttons found: %s' % (num_buttons, ', '.join(button_map)))

# Main event loop
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def getMotorSpeeds(mag, angle, cw, ccw):
    maxspeed = 6000
    maxrotspeed = 5000
    speeds = [0]*4
    speeds[0] = speeds[2] = int(maxspeed*np.sin(angle)*mag)
    speeds[1] = speeds[3] = int(maxspeed*np.cos(angle)*mag)

    rot = int((cw-ccw) * maxrotspeed)

    speeds[0] += rot
    speeds[1] -= rot
    speeds[2] -= rot
    speeds[3] += rot
    return speeds

event = Event()
q = queue.Queue()
def readJoy():
    jX = jY = cwAxis = ccwAxis = 0
    while True:
        evbuf = jsdev.read(8)
        if event.is_set():
            break
        if evbuf:
            _, value, type, number = struct.unpack('IhBB', evbuf)

            if type & 0x80:
                print("(initial)", end="")

            if type & 0x01:
                button = button_map[number]
                if button:
                    button_states[button] = value
                    if value:
                        print("%s pressed" % (button))
                    else:
                        print("%s released" % (button))

            if type & 0x02:
                axis = axis_map[number]
                if axis:
                    fvalue = value / 32767.0
                    axis_states[axis] = fvalue
                    #print("%s: %.3f" % (axis, fvalue))
                    if axis == "x":
                        jX = fvalue
                    elif axis == "y":
                        jY = -fvalue
                    elif axis == "gas":
                        cwAxis = (fvalue+1)/2
                    elif axis == "brake":
                        ccwAxis = (fvalue+1)/2
            tdata = [jX, jY, cwAxis, ccwAxis]
            q.put(tdata)


bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate='500000')
bus.flush_tx_buffer()
motors = Motors(bus)

period = 0.001
startTime = time.time()
speeds = [0]*4

cwAxis = 0
ccwAxis = 0
jX = 0
jY = 0
tdata = [jX, jY, cwAxis, ccwAxis]


t = Thread(target=readJoy, daemon=True)
t.start()
tagetSpeeds = [0]*4
speeds = [0]*4
step = 20
while True:
    #evbuf = jsdev.read(8)
    if not q.empty():
        tdata = q.get()
        #print(tdata)
    try:
        if time.time() - startTime >= period:
            jX, jY, cwAxis, ccwAxis = tdata[0], tdata[1], tdata[2], tdata[3]
            motors.set_speeds(speeds)
            startTime = time.time()
            magnitude, angle  = cart2pol(jX, jY)
            angle = angle + 5*np.pi/4
            angle = round(angle, 1)
            magnitude = 0 if magnitude < 0.7 else magnitude
            targetSpeeds = getMotorSpeeds(magnitude, angle, cwAxis, ccwAxis)
            

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


            print(magnitude, angle, speeds)
    except KeyboardInterrupt:
        event.set()
        break
t.join()
