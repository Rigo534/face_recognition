import cv2 
import face_recognition
import pickle
import numpy as np

camera = cv2.VideoCapture(0)
file = open("EncodeFile.pkl", 'rb')
face_encoded_with_names = pickle.load(file)
file.close()
face_encodings, face_names = face_encoded_with_names
face_locations = []

while True:
    ret, frame = camera.read()
    rgb_frame = cv2.resize(frame,(0,0),None,0.25,0.25)
    rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)       
    facelocationcamera = face_recognition.face_locations(rgb_frame)
    faceencodecamera = face_recognition.face_encodings(rgb_frame, facelocationcamera)
    
    for faceencoding, facelocation in zip(faceencodecamera, facelocationcamera):
        face_matching = face_recognition.compare_faces(face_encodings, faceencoding)
        face_distance = face_recognition.face_distance(face_encodings, faceencoding)
        print(face_distance)
        face_matching = np.argmin(face_distance)
        if face_distance[face_matching]< 0.5:
            name = face_names[face_matching].upper()
        else:
            name = 'Unknown'
        y1, x2, y2, x1 = facelocation
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)
