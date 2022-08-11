import numpy as np
import cv2
import time

def get_clip(input_filename, output_filename,  start_sec, end_sec):
    # input and output videos are probably mp4
    vidcap = cv2.VideoCapture(input_filename)
    
    # math to find starting and ending frame number
    fps = find_frames_per_second(vidcap)
    start_frame = int(start_sec*fps)
    end_frame = int(end_sec*fps)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES,start_frame)
    
    # open video writer
    vidwrite = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'MP4V'), fps, get_frame_size(vidcap))
    
    success, image = vidcap.read()
    frame_count = start_frame
    while success and (frame_count < end_frame):
        vidwrite.write(image)  # write frame into video
        success, image = vidcap.read()  # read frame from video
        frame_count+=1
    vidwrite.release()