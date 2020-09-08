from datetime import datetime
import cv2
import sqlite3



def insertPresent(dt):
    conn = sqlite3.connect("facebase.db")
    cmd = "insert into WORKHOUR (User_Present) values('"+ dt + "')"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def insertMovedAway(dt):
    conn = sqlite3.connect("facebase.db")
    cmd = "insert into WORKHOUR (User_Moved_Away) values('" + dt + "')"
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
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if firstFrame is None:
                firstFrame = gray
                continue

            deltaFrame = cv2.absdiff(firstFrame, gray)
            threshDelta = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
            threshDelta = cv2.dilate(threshDelta, None, iterations=0)
            (cnts, _) = cv2.findContours(threshDelta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in cnts:
                if 8000< cv2.contourArea(contour)< 15000:
                    status=1
                    (x,y,w,h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            statusList.append(status)

            statusList1 = statusList[-2:]

            if statusList1[-1] == 1 and statusList1[-2] == 0:
                up=str(datetime.now())
                #print('user is there at:' + up)
                insertPresent(up)
            if statusList1[-1] == 0 and statusList1[-2] == 1:
                ua=str(datetime.now())
                #print('user moved away at:' + ua)
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
    print(statusList)


surveillence()
