import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
datapath = 'dataset'


def getFaceWithId(path):
    imagepaths = [os.path.join(datapath, f) for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath, f))]
    faces, Ids = [], []
    for imagepath in imagepaths:
        faceimg = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
        faces.append(np.asarray(faceimg, dtype=np.uint8))
        id = os.path.split(imagepath)[1].split('.')[1]
        Ids.append(id)
    return faces, Ids


def train():
    faces, Ids = getFaceWithId(datapath)
    recognizer.train(faces, np.asarray(Ids, dtype=np.int32))
    recognizer.save('trainningDataset/trainningdata.yml')
    print("Trainning complete!!!")
    cv2.destroyAllWindows()

#train()



