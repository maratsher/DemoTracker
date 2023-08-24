import os
import cv2
import argparse
import numpy as np
from tracker import tracker


def parse_args():
    """ benchmark test."""
    parser = argparse.ArgumentParser(description='make object tracking.')
    
    
    parser.add_argument('--video', default='1.mp4',
                        help='test video file')
    parser.add_argument('--save_predictions', action='store_true',
                        help='select object location manually')
    parser.add_argument('--save-dir', type=str, default='./predictions',
                        help='directory of saved results')
    
    opt = parser.parse_args()
    return opt


def inference(tracker, opt):
    """
    this function returns a dictionaries result. which has two keys. one is bbox,
    which represents the coordinates of the predicted frame,
    the other is best_score, which records everyframe best_score.
    Save output in current path
    """
    cv2.namedWindow("tracking", cv2.WINDOW_NORMAL)
    start_tracking = False
    key = -1
    if not os.path.exists(opt.save_dir):
        os.makedirs(opt.save_dir)
    cap = cv2.VideoCapture(opt.video)    
    ind = 0
    while(1):
        ret, frame = cap.read()
        if not ret:
            break
        
        if ind == 0 or key == 115: # s 
            cv2.namedWindow('select roi')
            gt_bbox = cv2.selectROI(
                'select roi',
                frame, fromCenter = False)
            cv2.destroyWindow('select roi')
            if all(gt_bbox):
                start_tracking = True
                # init tracker
                print("IMAGE SIZE INPUT", np.array(frame).shape)
                vini.select_obj(frame, gt_bbox)
                pred_bbox = gt_bbox
                score = 1
            else:
                start_tracking = False  
        elif start_tracking:
            score, pred_bbox = vini.search_obj(frame)
            pred_bbox = list(map(int, pred_bbox))
            cv2.rectangle(frame, (pred_bbox[0], pred_bbox[1]),
                (pred_bbox[0]+pred_bbox[2], pred_bbox[1]+pred_bbox[3]),
                (0, 255, 255), 3)
            #print(f"confidence bbox:{score:.3f}")
        if opt.save_predictions:
            cv2.imwrite(os.path.join(opt.save_dir, '%04d.jpg'%(ind+1)), frame)
        
        cv2.imshow('tracking', frame)
        key = cv2.waitKey(10)
        if (key == 27 or key == 113): # esc or q
            break
        ind +=1

if __name__ == '__main__':
    opt = parse_args()
    vini = tracker()
    inference(vini, opt)