import cv2
import random
import sqlite3
from tkinter import *
from trainner import train
from datetime import datetime

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

'''--------------------------------------------------------------------------------datasetCreator starts here------------------------------------------------------------------ '''


def generateId():
    ID = random.sample(range(1, 500), 1)
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


def getName():
    global screen1
    global username
    global nameEntry
    screen1 = Toplevel(screen)
    screen1.geometry('600x500')
    screen1.title("Sign up")
    username = StringVar()

    Label(screen1, text='Sign up', bg='blue', width='300', height='2', font=("calibri", 13)).pack()
    Label(screen1, text="").pack()
    Label(screen1, text=' Enter Full Name Inside (" "),Eg."Naruto Ozumaki"', height='2', font=("calibri", 13)).pack()
    nameEntry = Entry(screen1, textvariable=username)
    nameEntry.pack()
    Label(screen1, text="").pack()
    Button(screen1, text='Register', width='10', height='2', command=collectData).pack()


def saveName(ID, Name):
    conn = sqlite3.connect("facebase.db")
    cmd = " insert into Users(ID,Name) values(" + str(ID) + "," + str(Name) + ")"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def signupSuccess():
    Label(screen1, text="").pack()
    Label(screen1, text="Preparing Dataset...", height='4', width='300').pack()
    Label(screen1, text="Sign up Successful!!!", height='4', width='300').pack()


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

    Name = username.get()
    nameEntry.delete(0, END)
    ID = generateId()

    saveName(ID, Name)

    while True:
        ret, frame = cam.read()
        if ret:
            face = faceextractor(frame)
            if face is not None:
                count += 1
                cv2.imwrite('dataset/user.' + str(ID)+ '.' + str(count) + '.jpg', face)
                cv2.putText(frame, 'collec ting face samples ' + str(count) + '...', (50, 50), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 255, 0), 3)
                cv2.imshow('Face Sample', frame)
                if count >= 150 or cv2.waitKey(1) == 13:
                    break
            else:
                print("Please hold still your face and look at the Camera!!!")
                pass
        else:
            Label(screen1, text="camera facing trouble while capturing frame...", bg='red').pack()
            pass

    cam.release()
    cv2.destroyAllWindows()
    train()
    Label(screen1, text="your ID:"+str(ID), width='30', height='2').pack()
    signupSuccess()


'''-----------------------------------------------------------datasetCreator ends here-------------------------------------------------------------'''
'''-----------------------------------------------------------surveillance starts here------------------------------------------------------------------'''


def workplace():
    global profile
    global screen
    global screen3
    screen3 = Toplevel(screen)
    screen3.title('Workplace')
    screen3.geometry('1400x800')
    Label(screen3,text="").pack()
    Label(screen3,text=('Workplace for '+str(profile[1])+'('+str(profile[0])+')'),bg='green',height='3',width='70').pack()
    Label(screen3,text="").pack()
    Button(screen3,text='Start Work',height='2',width='12',command=surveillence).pack()
    Label(screen3, text="").pack()
    Label(screen3, text="").pack()
    Label(screen3, text="To take a break press 'Q'",height='2').pack()
    Label(screen3, text="").pack()
    Label(screen3, text="").pack()
    Label(screen3, text="").pack()
    Button(screen3, text='Sign Out', height='2', width='10', command=destroy).pack()



def insertPresent(dt):
    global profile
    conn = sqlite3.connect("facebase.db")
    cmd = "insert into WorkTime (ID,User_Present) values("+str(profile[0])+",'" + dt + "')"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def insertMovedAway(dt):
    global profile
    conn = sqlite3.connect("facebase.db")
    cmd = "insert into WorkTime (ID,User_Moved_Away) values("+str(profile[0])+",'" + dt + "')"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def surveillence():
    statusList = [None, None]
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cam.read()
        status = 0
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            facequardinates = classifier.detectMultiScale(gray, 1.3, 6)
            if facequardinates is not ():
                for x, y, w, h in facequardinates:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                status=1
            statusList.append(status)

            statusList1 = statusList[-2:]

            if statusList1[-1] == 1 and statusList1[-2] == 0:
                up=str(datetime.now())
                print('user is there at:' + up)
                insertPresent(up)
            if statusList1[-1] == 0 and statusList1[-2] == 1:
                ua=str(datetime.now())
                print('user moved away at:' + ua)
                insertMovedAway(ua)


            cv2.imshow('frame', frame)
            cv2.waitKey(500)
            if cv2.waitKey(500) == ord('q'):
                break
        else:
            print('preparing camera:')
            pass

    cam.release()
    cv2.destroyAllWindows()
'''------------------------------------------------------------surveillance ends here---------------------------------------------------------------------'''
'''------------------------------------------------------------Recognizer starts here-----------------------------------------------------------------------------'''


def loginSuccess():
    global screen
    global screen2
    screen2 = Toplevel(screen)
    screen2.geometry('300x250')
    Label(screen2, text="").pack()
    Label(screen2, text="Login Successful!!!", height='4', width='300').pack()
    Label(screen2, text="").pack()
    Button(screen2, text="Go to Workplace", width='30',height='4',command=workplace).pack()




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
    flag = 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    facequardinates = classifier.detectMultiScale(gray, 1.3, 6)
    if facequardinates is ():
        return None, flag
    for x, y, w, h in facequardinates:
        cropped = gray[y:y + w, x:x + h]
        img = cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0), 1)
        ID, loss = recognizer.predict(cropped)
        #print(loss)
        if loss < 57:
            global profile
            profile = getProfile(ID)
            if profile is not None:
                cv2.putText(img, "User Id: " + (str(profile[0]) + "- " + str(profile[1])), (x, y + h + 30),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                flag = 1
        else:
            cv2.putText(img, "not valid user!!!", (x, y + h + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

    return img, flag


def recognize():
    recognizer.read('trainningDataset/trainningdata.yml')
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0
    while True:
        ret, frame = cam.read()
        if ret:
            img, flag = faceExtractor(frame)
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
    if flag == 1:
        loginSuccess()


'''-------------------------------------------------------recognizer ends here-----------------------------------------------------------------'''


def destroy():
    global screen2
    global screen3
    screen2.destroy()
    screen3.destroy()


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("1366x768")
    screen.title("SignIn or SignUp ")
    Label(text="Sign in or Sign up", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="User Login", height="2", width="30", command=recognize).pack()
    Label(text="").pack()
    Button(text="Sign up for new user", height="2", width="30", command=getName).pack()

    screen.mainloop()


main_screen()



