import pyrealsense2 as rs
import numpy as np
import argparse
import time
import os

def parser_args():
    parser = argparse.ArgumentParser(description='test the accel data in t265')
    parser.add_argument('--save_dir_accel', default='./data/t265_accel.txt', help='dir to save the accel data')
    parser.add_argument('--save_dir_velocity', default='./data/t265_velocity.txt', help='dir to save the velocity data')
    parser.add_argument('--save_dir_pose', default='./data/t265_pose.txt', help='dir to save the pose data')
    args = parser.parse_args()
    return args

def write_data(filename, data):
    fout = open(filename, 'a')
    fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), data.x, data.y, data.z))
    fout.close()
    

if __name__ == "__main__":
    args = parser_args()
    # if not os.path.exists(args.save_dir):
    #     os.makedirs(args.save_dir)
    
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
                pose_fout = open(args.save_dir_pose, 'a')
                accel_fout = open(args.save_dir_accel, 'a')
                velocity_fout = open(args.save_dir_velocity, 'a')
                pose_fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), pos.x, pos.y, pos.z))
                accel_fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), accel.x, accel.y, accel.z))
                velocity_fout.write('{:.2f}\tx\t{:.4f}\ty\t{:.4f}\tz\t{:.4f}\n'.format(time.time(), velocity.x, velocity.y, velocity.z))
                print('the frame number is {}'.format(pose.frame_number))
                print('the translation is x:{:.4f}, y:{:.4f}, z:{:.4f}'.format(pos.x, pos.y, pos.z))
                pose_fout.close()
                accel_fout.close()
                velocity_fout.close()
    finally:
        pipeline.stop()

