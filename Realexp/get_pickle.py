import cv2
import pickle
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="./data/exp/2021-06-18-15-08-18/000150.jpg", help="the original image")
    parser.add_argument("--out_dir", default="./data/exp/2021-06-18-15-08-18", help="the saved path")
    opt = parser.parse_args()

    
    with open(os.path.join(opt.out_dir, "000150.pickle"), 'wb') as fout:
        pickle.dump(opt.image, fout)
