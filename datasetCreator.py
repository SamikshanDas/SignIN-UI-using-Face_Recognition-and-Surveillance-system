import cv2
import sqlite3
from trainner import train
import random

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def generateId():
    ID = random.sample(range(1,500),1)
    conn = sqlite3.connect("facebase.db")
    cmd = "select * from Users where ID=" + str(ID[0])
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 0:
        conn.close()
        return ID[0]
    else:
        generateId()


def saveName(ID, Name):
    conn = sqlite3.connect("facebase.db")
    cmd = " insert into Users(ID,Name) values(" + str(ID) + "," + str(Name) + ")"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def faceextractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    facequardinates = classifier.detectMultiScale(gray, 1.3, 6)
    if facequardinates is ():
        return None
    for x, y, w, h in facequardinates:
        cropped = gray[y:y + h, x:x + w]
    return cropped


def collectData():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0

    ID = generateId()
    Name = input('Enter Your Name Inside double inverted comas("..."):')

    saveName(ID, Name)

    while True:
        ret, frame = cam.read()
        if ret:
            face = faceextractor(frame)
            if face is not None:
                count += 1
                cv2.imwrite('dataset/user.' + str(ID) + '.' + str(count) + '.jpg', face)
                cv2.putText(frame, 'collecting face samples ' + str(count) + '...', (50, 50), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 255, 0), 1)
                cv2.imshow('Face Sample', frame)
                if count >= 100 or cv2.waitKey(1) == 13:
                    break
            else:
                print("Please hold still your face and look at the Camera!!!")
                pass
        else:
            print("Preparing Camera...")
            pass

    cam.release()
    cv2.destroyAllWindows()
    print('Collecting Samples Is Now Complete...')
    train()
    print('your ID:'+str(ID))


collectData()



