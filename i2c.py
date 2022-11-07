import smbus2 as smbus
import time
bus = smbus.SMBus(1)
address = 0x04


while True:
        #roll = bus.read_word_data(address, 2)
        yaw = bus.read_i2c_block_data(address, 3, 4)
        #pitch = bus.read_word_data(address, 4)
        #print(roll, yaw, pitch)
        print(yaw[0] + (yaw[1]*255), yaw)
        time.sleep(0.01)
