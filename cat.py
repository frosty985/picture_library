import cv2
import os
import copy
import random

"""
Main prgram for detecting objects
Currently only faces
"""
# todo Add more detection type


""" haarcasades """
# fixme check file exists, turn on/off below options if they don't

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
glasses_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')


def rnd_col(b=256, g=256, r=256):
    b = random.randint(0, int(b))
    g = random.randint(0, int(g))
    r = random.randint(0, int(r))
    color = (b, g, r)
    return color


"""
where a ROI has been found, save it to outdir ready to be used to train the facial recognistion
"""
def save_img(outdir, cat, imgname, img, debug=False):
    """
    Save ROI
    :param outdir: set in config.ini
    :param cat: determinned
    :param imgname: filename of current file
    :param img: store/working image
    :param debug: print debug to command line
    :return:
    """
    """ check for output dirs """
    if not (os.path.exists(str(outdir))):
        print("Output directory doesn't exist, trying to create")
        try:
            os.makedirs(str(outdir))
        except Exception as e:
            print("\nThere was an error creating directory:\t" + str(outdir))
            exit()

    if not (os.path.exists(outdir + "/" + str(cat))):
        try:
            os.makedirs(outdir + "/" + str(cat))
        except Exception as e:
            print("\nThere was an error creating directory:\t" + outdir + "/" + str(cat))
            exit()

    if debug:
        print("[Debug]\tSaving file '" + imgname + "' to '" + outdir + "/" + cat + "/" + imgname)
    try:
        cv2.imwrite(outdir + "/" + cat + "/" + imgname, img)
    except Exception as e:
        print ("[Error]\tUnable to save image : " + str(e))


""" look for a face in the current image"""
def is_face(inimg, outdir="/tmp/piclib", show=False, debug=False):
    imgname = os.path.splitext(os.path.basename(inimg))[0]

    # cat = "Uncategorised"
    cat = None
    roi_face = None
    roi_color = None
    roi_gray = None

    """ Check/create working dirs """
    if debug:
        print("[Debug]\tChecking working directories exist")


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
        if len(faces) is not 0:
            for (x, y, w, h,) in faces:
                counter += 1

                if debug:
                    print("[Debug]\tChecking for eyes")
                cat = "Possible Face"

                roi_gray = imgGray[y:y + h, x:x + w]
                roi_color = resized[y:y + h, x:x + w]
                roi_face = copy_resized[y:y + h, x:x + w]

                if show:
                    cv2.imshow("Face found: " + str(counter), roi_color)

                cv2.rectangle(resized, (x, y), (x + w, y + h), rnd_col(255, 255, 255), 2)

                eyes = eye_cascade.detectMultiScale(roi_gray)
                if debug:
                    print("[Debug] Eyes found: " + str(eyes))

                # check for eyes
                for (ex, ey, ew, eh) in eyes:

                    # cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
                    if debug:
                        print("[Debug]\tEyes found, must be a face")
                    cat = "Face"
                    """
                    face has been found, save to the right directory
                    """

                    counter += 1
                    # save_img(outdir, cat, imgname + "-" + str(counter) + ".jpg", roi_face, debug=debug)
                    # cv2.imwrite(outdir + "/" + cat + "/" + imgname + "-" + str(counter) + ".jpg", roi_face)

                # check for glasses
                if len(eyes) is not 0:

                    glasses = glasses_cascade.detectMultiScale(roi_gray)

                    if debug:
                        print("[Debug]\tGlasses found: " + str(glasses))

                    for (gx, gy, gw, gh) in glasses:
                        # cv2.rectangle(roi_color, (gx, gy), (gx + gw, gy + gh), (0, 0, 255), 2)
                        cat = "Face"
                        """
                        face has been found, save to the right directory
                        """
                        counter += 1
                        # save_img(outdir, cat, imgname + "-" + str(counter) + ".jpg", roi_face,
                        #         debug=debug)

                if len(eyes) == 0 and len(glasses) == 0:
                    """
                    a 'possible' face has been found, save to the right directory
                    """
                    cat = "Possible"
                    counter += 1

                save_img(outdir, cat, imgname + "-" + str(counter) + ".jpg", roi_face, debug=debug)

        if show:
            cv2.imshow("Filename: " + str(imgname), resized)

            cv2.waitKey(0)
        return(cat)

    except Exception as e:
        print("\nError loading image\t" + str(e))