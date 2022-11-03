import can
import time

with can.interface.Bus(bustype='socketcan', channel='can0', bitrate='250000') as bus:

    for i in range(0, 65535, 1000):

        b = i.to_bytes(4, 'big')
        msg = can.Message( arbitration_id=0x00003D, data=b, is_extended_id=True) 
        bus.send(msg)
        time.sleep(0.1)
        
        
    for i in range(0, 65535, 1000):

        speed = 4294967295 - i
        b = speed.to_bytes(4, 'big')
        msg = can.Message( arbitration_id=0x00003D, data=b, is_extended_id=True) 
        bus.send(msg)
        time.sleep(0.1)
