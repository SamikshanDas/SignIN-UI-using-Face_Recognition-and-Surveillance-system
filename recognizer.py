import sqlite3
import cv2

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()


def getProfile(ID):
    conn = sqlite3.connect('facebase.db')
    cmd = "select * from Users where ID=" + str(ID)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile



def faceExtractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    facequardinates = classifier.detectMultiScale(gray, 1.3, 6)
    if facequardinates is ():
        return None
    for x, y, w, h in facequardinates:
        cropped = gray[y:y + w, x:x + h]
        img = cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0), 1)
        ID, loss = recognizer.predict(cropped)
        print(loss)
        if loss < 55:
            profile = getProfile(ID)
            if profile is not None:
                cv2.putText(img, "User Id: " + (str(profile[0]) + "- " + str(profile[1])), (x, y + h + 30),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        else:
            cv2.putText(img, "not valid user!!!", (x, y + h + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

    return img


def recognize():
    recognizer.read('trainningDataset/trainningdata.yml')
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0
    while True:
        ret, frame = cam.read()
        if ret:
            img = faceExtractor(frame)
            if img is not None:
                cv2.imshow('Detecting...', img)
                count += 1
                if count > 9:
                    cv2.waitKey(8000)
                    break
            else:
                cv2.putText(frame, "Detecting face, please wait...", (200, 300), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                            2)
                cv2.imshow('Detecting...', frame)
            if cv2.waitKey(1) == 13:
                break
        else:
            print("preparing camera")
            pass

    cam.release()
    cv2.destroyAllWindows()

recognize()
