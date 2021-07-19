import pyrealsense2 as rs
import numpy as np
import argparse
import time
import os

def parser_args():
    parser = argparse.ArgumentParser(description='test the accel data in t265')
    parser.add_argument('--save_dir', default='./data/t265_accel', help='dir to save the data')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parser_args()
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    
    # init the pipeline
    pipeline = rs.pipeline()
    conf = rs.config()
    conf.enable_stream(rs.stream.pose)
    profile = pipeline.start(conf)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            pose = frames.get_pose_frame()
            if pose and pose.frame_number%100 == 0:
                data = pose.get_pose_data()
                pos = data.translation
                accel = data.acceleration
                velocity = data.velocity
                fout = open('./pose.txt', 'a')
                accel_fout = open('./accel.txt', 'a')
                velocity_fout = open('./velocity.txt', 'a')
                fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), pos.x, pos.y, pos.z))
                accel_fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), accel.x, accel.y, accel.z))
                velocity_fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), velocity.x, velocity.y, velocity.z))
                print('the frame number is {}'.format(pose.frame_number))
                print('the translation is x:{:.4f}, y:{:.4f}, z:{:.4f}'.format(pos.x, pos.y, pos.z))
                fout.close()
    finally:
        pipeline.stop()

