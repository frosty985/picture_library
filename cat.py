import cv2
import os
import copy
import sys
from datetime import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
glasses_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
exec_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

""" look for a face in the current image"""
def save_img(outdir, cat, imgname, img, debug=False):
    if debug:
        print("[Debug]\tSaving file '" + imgname + "' to '" + outdir + "/" + cat + "/" + imgname)
    try:
        cv2.imwrite(outdir + "/" + cat + "/" + imgname, img)
    except Exception as e:
        print ("[Error]\tUnable to save image : " + str(e))


def is_face(inimg, outdir="/tmp/piclib", show=False, debug=False):
    imgname = os.path.splitext(os.path.basename(inimg))[0]

    cat = "Uncategorised"
    roi_face = None
    roi_color = None
    roi_gray = None

    """ Check/create working dirs """
    if debug:
        print("[Debug]\tChecking working directories exist")

    if not (os.path.exists(outdir)):
        print("Directory doesn't exist, trying to create")
        try:
            os.makedirs(outdir)
        except Exception as e:
            print ("\nThere was an error creating directory:\t" + outdir)
            exit()
    if not (os.path.exists(outdir + "/Face")):
        try:
            os.makedirs(outdir + "/Face")
        except Exception as e:
            print("\nThere was an error creating directory:\t" + outdir + "/Face")
            exit()
    if not (os.path.exists(outdir + "/Possible")):
        try:
            os.makedirs(outdir + "/Possible")
        except Exception as e:
            print ("\nThere was an error creating directory:\t" + outdir + "/Possible")
            exit()


    """ Check image exists """
    if debug:
        print("[Debug]\tChecking image exists")
    if (os.path.exists(inimg) == False):
        print("\nFile " + inimg + " does not exist")
        exit()

    """
    load image twice, original in colour
    then convert to grayscale for analising
    create a copy to use later for saving
    """
    if debug:
        print("[Debug]\tLoading image to work with: '" + inimg + "'")
    try:
        img = cv2.imread(inimg)
        # resize image
        r = 1000.00 / img.shape[1]
        dim = (1000, int(img.shape[0] * r))

        resized  = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        copy_resized = copy.copy(resized)
        imgGray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        #faces = face_cascade.detectMultiScale(imgGray, 1.3, 5)
        faces = face_cascade.detectMultiScale(imgGray, 1.3, 6)

        if debug:
            print("[Debug] Possible faces found: " + str(faces))
        counter = 0
        for (x, y, w, h,) in faces:
            if debug:
                print("[Debug]\tChecking for eyes")
            cat = "Possible Face"

            roi_gray = imgGray[y:y + h, x:x + w]
            roi_color = resized[y:y + h, x:x + w]

            roi_face = copy_resized[y:y + h, x:x + w]

            cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

            eyes = eye_cascade.detectMultiScale(roi_gray)
            print("[Debug] Eyes found: " + str(eyes))

            #check for eyes
            for (ex, ey, ew, eh) in eyes:

                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
                if debug:
                    print("[Debug]\tEyes found, must be a face")
                cat = "Face"
                """
                face has been found, save to the right directory
                """

                counter += 1
                save_img(outdir, cat, imgname + "-" + str(counter) + ".jpg", roi_face, debug=debug)
                #cv2.imwrite(outdir + "/" + cat + "/" + imgname + "-" + str(counter) + ".jpg", roi_face)
            # check for glasses
            if len(eyes) >= 0:

                glasses = glasses_cascade.detectMultiScale(roi_gray)

                if debug:
                    print("[Debug]\tGlasses found: " + str(glasses))

                for (gx, gy, gw, gh) in glasses:
                    cv2.rectangle(roi_color, (gx, gy), (gx + gw, gy + gh), (0, 0, 255), 2)
                    cat = "Face"
                    """
                    face has been found, save to the right directory
                    """
                    counter += 1
                    save_img(outdir, cat, imgname + "-" + str(counter) + ".jpg", roi_face,
                             debug=debug)

            if len(eyes) == 0:
                """
                a 'possible' face has been found, save to the right directory
                """
                cat = "Possible"
                counter += 1
                save_img(outdir, cat, imgname + "-" + str(counter) + ".jpg", roi_face,
                         debug=debug)

        if show:
            cv2.imshow("Faces", resized)
            cv2.imshow("Faces1", roi_color)
            cv2.waitKey(0)
        return(cat)

    except Exception as e:
        print("\nError loading image\t" + str(e))