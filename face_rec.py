import pymysql
import mysql_actions
import numpy as np
import cv2
import copy

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('faceTrain.yml')

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def get_face_ids(cur, debug=False):
    sql = ("SELECT id, frid, who FROM who")
    cur.execute(sql)
    return cur


def face_rec(img, cur, debug=False, show=False, resize=750, min_conf=49):
    print(str(img))

    sql = "SELECT id FROM pictures WHERE filename = '{}'".format(img)
    cur.execute(sql)
    pid = cur._rows[0]["id"]

    """ Get face ids, using a copy of cur, else cant be reused later """
    fids = get_face_ids(copy.copy(cur))

    im = cv2.imread(img)

    """ make image 'resize' px tall"""
    r = float(resize) / im.shape[1]
    dim = (resize, int(im.shape[0] * r))
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    if debug:
        print("[Debug]\tChecking faces")
    faces = faceCascade.detectMultiScale(gray, 1.2, 6)
    for (x, y, w, h) in faces:
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])

        if conf > 0:
            if debug:
                print("Found a face")
                print(str(id))
                print("\t" + fids._rows[id - 1]["who"] + " - " + str(round(conf, 2)) + "%")

            """ for visual debugging (only used if show is set in config.ini """
            cv2.rectangle(resized, (x, y), (x + h, y + w), (0, 255, 00), 4)
            cv2.putText(resized, fids._rows[id - 1]["who"] + " " + str(round(conf, 2)) + "%", (x - 20, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            """ if confident enough, add to database """
            if conf > min_conf:
                sql = "SELECT id FROM pic_who WHERE pid = '{}' AND wid = '{}'".format(pid, fids._rows[id - 1]["id"])
                cur.execute(sql)
                if cur.rowcount == 0:
                    sql = "INSERT INTO pic_who (id, pid, wid) VALUES (REPLACE(UUID(), '-', ''), '{}', '{}')".format(
                        str(pid), str(fids._rows[id - 1]["id"]))
                    cur.execute(sql)
    if show:
        cv2.imshow("Faces", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
