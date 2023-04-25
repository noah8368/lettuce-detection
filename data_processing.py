# -*- coding: utf-8 -*-
"""DataPreProcessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NFUrELjdKueMVFzFSRmX10ZlpcHo77N0
"""

import os

from glob import glob
from google.colab import drive

drive.mount('/content/drive')                                                   

def convert_file(ground_truth_file_path, output_folder):
  # Open ground truth file and set parameter to read (r)
  groundTruthFile = open(ground_truth_file_path, 'r') 

  Lines = groundTruthFile.readlines()

  perImageAnnotation = ''
  currentFrameID = None
  imageWidth = 810
  imageHeight = 1080
  # line variable defined is each list of strings
  for line in Lines:
    bounding_box_parameters = line.strip().split(",")
    frameID, classID, x, y, w, h =  bounding_box_parameters[:-3]

    if currentFrameID is None:
      currentFrameID = frameID
    elif frameID != currentFrameID:
      newImageGroundTruth = open(f"{output_folder}/{currentFrameID}.txt", "w")
      newImageGroundTruth.write(perImageAnnotation)
      newImageGroundTruth.close()
      perImageAnnotation = ''
      currentFrameID = frameID
  
    x = int(x)
    y = int(y)
    w = int(w)
    h = int(h)
    # convert from top left corner to center of image for bounding box
    # Normalize between 0 and 1 for YOLOv8 
    x += w/2
    y += h/2
    y = round(y/imageHeight, 2)
    h = round(h/imageHeight, 2)
    x = round(x/imageWidth, 2)
    w = round(w/imageWidth, 2) 
    perImageAnnotation += f"{classID} {x} {y} {w} {h}\n"
    

  if len(perImageAnnotation) != 0:
    newImageGroundTruth = open(f"{output_folder}/{currentFrameID}.txt", "w")
    newImageGroundTruth.writelines(perImageAnnotation)
    newImageGroundTruth.close()

if __name__ == "__main__":
  # TODO: Change the `DATASET_ROOT_DIR` variable to reflect where your dataset
  # is.
  DATASET_ROOT_DIR = "/content/drive/MyDrive/BRAE_428_Colab/LettuceMOT"
  data_subsets = glob(f"{DATASET_ROOT_DIR}/*")
  
  for subset_path in data_subsets:
    ground_truth_file_path = subset_path + "/gt/gt.txt"
    output_folder = subset_path + "/yolo_gt"
    
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)
    
    convert_file(ground_truth_file_path, output_folder)