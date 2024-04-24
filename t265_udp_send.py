import numpy as np
import socket
import pyrealsense2.pyrealsense2 as rs

UDP_IP = "10.43.0.1"
UDP_PORT = 5005
MESSAGE = [0]*6

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

pipe = rs.pipeline()

# Configure the pipeline
cfg = rs.config()

cfg.enable_stream(
    rs.stream.pose
)  

while True:
    try:
        pipe.start(cfg)
        break
    except Exception as e:
        print(e, "retrying..")


while True:

    frames = pipe.wait_for_frames()

    pose = frames.get_pose_frame()

    if pose:
        pose_data = pose.get_pose_data()
        MESSAGE = np.array([
                pose_data.translation.x,
                pose_data.translation.y,
                pose_data.translation.z,
                pose_data.rotation.x,
                pose_data.rotation.y,
                pose_data.rotation.z,
                pose_data.rotation.w,
        ]).tobytes()
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        #print("Position: ", pose_data.translation)
        #print("Rotation: ", pose_data.rotation)
#        print("Velocity: ", pose_data.velocity)


