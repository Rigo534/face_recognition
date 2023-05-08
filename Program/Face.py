import cv2 
import face_recognition
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from subprocess import call

cred = credentials.Certificate('Program/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://facerecognitionattendanc-ff2b5-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket' : "facerecognitionattendanc-ff2b5.appspot.com"
})


call(['python', "Program/EncodingProcess.py"])
camera = cv2.VideoCapture(0)
ref = db.reference('Employee')
data = ref.get()
print(data)
# camera.set(3, 640)
# camera.set(4, 480)

file = open("Encode", 'rb')
face_encoded_with_id = pickle.load(file)
file.close()
face_encodings, face_id = face_encoded_with_id
face_locations = []

while True:
    ret, frame = camera.read()
    rgb_frame = cv2.resize(frame,(0,0),None,0.25,0.25)
    rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)       
    facelocationcamera = face_recognition.face_locations(rgb_frame)
    faceencodecamera = face_recognition.face_encodings(rgb_frame, facelocationcamera)
    
    for faceencoding, facelocation in zip(faceencodecamera, facelocationcamera):
        face_matching = face_recognition.compare_faces(face_encodings, faceencoding)
        print(face_matching)
        face_distance = face_recognition.face_distance(face_encodings, faceencoding)
        print(face_distance)
        face_matching = np.argmin(face_distance)
        if face_distance[face_matching]< 0.5:
            id = face_id[face_matching]
            name = data[id]["Nama"].upper()
        else:
            name = 'Unknown'
        y1, x2, y2, x1 = facelocation
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(frame, name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX, 0.75,(255,255,255),2)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)
