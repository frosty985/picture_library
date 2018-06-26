import cv2
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('faceTrain.yml')


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, im = cap.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2, 6)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x - 50, y - 50), (x + w + 50, y + h + 50), (225, 0, 0), 2)
        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        #print(conf)
        if conf>50:
            if Id == 1:
                name = "Gary"
            elif Id == 2:
                name = "Sian"
            elif Id == 3:
                name = "Chloe"
            else:
                name = "Unknown"
            cv2.putText(im, str(name) + " " + str(round(conf)) + "%", (x, y + h), font, 2, (255,255,0))
    cv2.imshow('im', im)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()