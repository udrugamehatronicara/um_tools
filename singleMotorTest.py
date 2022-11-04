import can
import time

with can.interface.Bus(bustype='socketcan', channel='can0', bitrate='250000') as bus:
    bus.flush_tx_buffer()
    addr=0x00003C

    for i in range(0, 65535, 1000):

        b = i.to_bytes(4, 'big')
        msg = can.Message( arbitration_id=addr, data=b, is_extended_id=True) 
        bus.send(msg)
        time.sleep(0.1)
        print(i)

    time.sleep(1)
        
        
    for i in range(0, 65535, 1000):

        speed = 4294967295 - i
        b = speed.to_bytes(4, 'big')
        msg = can.Message( arbitration_id=addr, data=b, is_extended_id=True) 
        bus.send(msg)
        time.sleep(0.1)
        print(speed)

    speed = 0
    b = speed.to_bytes(4, 'big')
    msg = can.Message( arbitration_id=addr, data=b, is_extended_id=True) 
    bus.send(msg)
