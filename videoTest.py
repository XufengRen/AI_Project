from ctypes import *                                               # Import libraries
import math
import random
import os
import cv2
import numpy as np
import time
import darknet


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    # Colored labels dictionary
    color_dict = {
        'amazonCourier' : [0, 255, 255], 'fedexCourier': [238, 123, 158], 'ups_courier' : [24, 245, 217], 'uspsCourier' : [224, 119, 227]
    }
    
    for detection in detections:
        # print("detections[0]: " + str(detection[0]))
        # print("detections[1]: " + str(detection[1]))
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        name_tag = str(detection[0])#.decode())
        for name_key, color_val in color_dict.items():
            if name_key == name_tag:
                color = color_val 
                xmin, ymin, xmax, ymax = convertBack(
                float(x), float(y), float(w), float(h))
                pt1 = (xmin, ymin)
                pt2 = (xmax, ymax)
                cv2.rectangle(img, pt1, pt2, color, 1)
                cv2.putText(img,
                            detection[0] +
                            " [" + str(detection[1]) + "]",
                            (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            color, 2)
    return img

def YOLO():
   
    # global metaMain, netMain, altNames
    configPath = "./cfg/knockknock_cfg.cfg"                                 # Path to cfg
    weightPath = "./knockknock_cfg_best.weights"                                 # Path to weights
    metaPath = "./data/obj.data"                                    # Path to meta data
    if not os.path.exists(configPath):                              # Checks whether file exists otherwise return ValueError
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    network, class_names, class_colors = darknet.load_network(
            configPath,
            metaPath,
            weightPath,
            batch_size=1
        )
   
    
    #cap = cv2.VideoCapture(0)                                      # Uncomment to use Webcam
    cap = cv2.VideoCapture("ups02.avi")                             # Local Stored video detection - Set input video
    frame_width = int(cap.get(3))                                   # Returns the width and height of capture video
    frame_height = int(cap.get(4))
    # Set out for video writer
    out = cv2.VideoWriter(                                          # Set the Output path for video writer
        "./output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
        (frame_width, frame_height))

    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(frame_width, frame_height, 3) # Create image according darknet for compatibility of network
    x=float(0)
    while True:                                                      # Load the input frame and write output frame.
        prev_time = time.time()
        # print("line 107 pass")
        ret, frame_read = cap.read()                                 # Capture frame and return true if frame present
        # print("line 109 pass")
        # For Assertion Failed Error in OpenCV
        if not ret:                                                  # Check if frame present otherwise he break the while loop
            break

        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)      # Convert frame into RGB from BGR and resize accordingly
        #print("line 116 pass")
        frame_resized = cv2.resize(frame_rgb,
                                   (frame_width, frame_height),
                                   interpolation=cv2.INTER_LINEAR)
        #print("line 117 pass")
        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())                # Copy that frame bytes to darknet_image
        #print("line 121 pass")
        # detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.5)    # Detection occurs at this line and return detections, for customize we can change the threshold.                                                                                   
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.8)
        #print("line 124 pass")
        image = cvDrawBoxes(detections, frame_resized)               # Call the function cvDrawBoxes() for colored bounding box per class
        #print("line 126 pass")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # if detections:
        #   print(detections[0][1])

        if detections:
          if float(detections[0][1])>x:
            snap=image
            detection=detections
            x=float(detections[0][1])
            # x=x+1
        # print(detections)
        #print("line 128 pass")
        # print(1/(time.time()-prev_time))
        #print("line 130 pass")
        #cv2.imshow('Demo', image)                                    # Display Image window
        #print("line 132 pass")
        cv2.waitKey(3)
        out.write(image)                                             # Write that frame into output video
    # print("detections[0]: " + str(detections[0][0]))
    cv2.imwrite("snap.jpg",snap)
    cap.release()                                                    # For releasing cap and out. 
    out.release()

    print(detection[0][0])
    print(detection[0][1])
    print(":::Video Write Completed")

if __name__ == "__main__":  
    YOLO()                                                           # Calls the main function YOLO()
