import argparse
import configparser
import numpy as np
import os
import cv2
from argparse import RawTextHelpFormatter
from PIL import Image

""" Set program arguments """
parser = argparse.ArgumentParser("Train facerconginser from samples taken", formatter_class=RawTextHelpFormatter)
parser.add_argument("src_dir", type=str)
parser.add_argument("-o", "--output", type=str, default="/tmp/piclib", help="Output directory")
parser.add_argument("-c", "--config", type=str, default="config.ini", help="Location of config file")

args = parser.parse_args()
configfilename = args.config

""" Set Golbal varibles """
config = None
con_database = None
con_debug = None
mysqlCur = None


""" Load config file """
if (os.path.exists(configfilename) == False):
    print("\nSorry, the config file " + configfilename + " does not exist\nPlease check the command line, or create a config file")
    exit()
try:
    config = configparser.ConfigParser()
    config.read(configfilename)
    if(len(config.sections()) == 0):
        raise Exception("File", "Empty")
    con_database = config["database"]
    con_debug = config["debug"]

except:
    print("\nError reading config file.\nPlease check it is valid, and try again\n")
    exit()

""" Set varibles """
recognizer = cv2.face.LBPHFaceRecognizer_create()
decetor = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faceSamples = []
ids = []

"""
check src_dir exists
  for each dir, enter
loop through each .jpg 
"""
def getImagesAndLabels(workingDir):
    counter = 0
    if con_debug.getboolean("message"):
        print("[Debug]\tEntering working dir: \t" + workingDir)
    for dirList in sorted(os.listdir(workingDir)):

        dirname = os.fsdecode(str(dirList))

        if con_debug.getboolean("message"):
            print("[Debug]\tChecking '" + dirname + "' is a directory")
        if os.path.isdir(workingDir + "/" + str(dirname)):
            counter += 1
            if con_debug.getboolean("message"):
                print("[Debug]\t" + str(counter) + " '" + dirname + "' as ID")
                print("[Debug]\tLooping through file list and train")
            for fileList in os.listdir(workingDir + "/" + dirname):

                filename = os.fsdecode(fileList)
                if con_debug.getboolean("message"):
                    print("[Debug]\tLooping through files: \t" + filename)

                if con_debug.getboolean("message"):
                    print("[Debug]\tChecking file is a jpg")
                if filename.endswith(".jpg"):
                    if con_debug.getboolean("message"):
                        print("[Debug]\tOpening image: \t" + filename)
                    pilImage = Image.open(workingDir + "/" + dirname + "/" + filename).convert("L")

                    if con_debug.getboolean("message"):
                        print("[Debug]\tConverting to numpy: \t" + filename)
                    imageNp = np.array(pilImage, 'uint8')

                    if con_debug.getboolean("message"):
                        print("[Debug]\tDetecting faces: \t" + filename)
                    faces=decetor.detectMultiScale(imageNp)
                    for (x, y, w, h) in faces:

                        if con_debug.getboolean("message"):
                             print("[Debug]\tFace found at: \t {}, {}, {}, {}".format(x, y, w, h))
                        faceSamples.append(imageNp[y:y+h, x:x+w])
                        ids.append(int(counter))
    return faceSamples,ids

if (os.path.exists(str(args.src_dir))):
    faces,ids = getImagesAndLabels(str(args.src_dir))
    recognizer.train(faces, np.array(ids))
    #recognizer.save(os.path.basename(os.path.normpath(str(args.src_dir))) + ".yml")
    recognizer.save("faceTrain.yml")
else:
    print("\nThe directory: '" + str(args.src_dir) + "' does not exist\n")
    exit()
