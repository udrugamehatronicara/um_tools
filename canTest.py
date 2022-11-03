import can


def send_one():
    """Sends a single message."""

    # this uses the default configuration (for example from the config file)
    # see https://python-can.readthedocs.io/en/stable/configuration.html
    with can.interface.Bus(bustype='socketcan', channel='can0', bitrate='250000') as bus:

        # Using specific buses works similar:
        # bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
        # bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        # bus = can.interface.Bus(bustype='ixxat', channel=0, bitrate=250000)
        # bus = can.interface.Bus(bustype='vector', app_name='CANalyzer', channel=0, bitrate=250000)
        # ...

        msg1 = can.Message(
            arbitration_id=0x000088, data=[0x10, 0x7F, 0x00, 0, 0, 0, 0, 0], is_extended_id=True
        )
        msg2 = can.Message(
            arbitration_id=0x00033D, data=[0, 0, 0, 0, 0, 0, 0, 255], is_extended_id=True
        )
        msg = msg2
        print(msg)

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")


if __name__ == "__main__":
    send_one()
