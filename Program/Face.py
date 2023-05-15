import cv2 
import face_recognition
import pickle
import numpy as np
import mysql.connector 

# def detecting_face_movement(face_landmarks):
#     left_eye_top = face_landmarks['left_eye'][1]
#     right_eye_top = face_landmarks['right_eye'][1]
#     mouth_top = face_landmarks['top_lip'][0]

#     eye_movement_x = abs(left_eye_top[0] - right_eye_top[0])
#     eye_movement_y = abs(left_eye_top[1] - right_eye_top[1])
#     mouth_movement_x = abs(left_eye_top[0] - mouth_top[0])
#     mouth_movement_y = abs(left_eye_top[1] - mouth_top[1])
    
#     total_movement = eye_movement_x + eye_movement_y + mouth_movement_x + mouth_movement_y
#     return total_movement

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="coba_db"
)

cursor = db.cursor()
from subprocess import call

call(['python', "Program/EncodingProcess.py"])
camera = cv2.VideoCapture(0)
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
    print(facelocationcamera)
    faceencodecamera = face_recognition.face_encodings(rgb_frame, facelocationcamera)
    
    for faceencoding, facelocation in zip(faceencodecamera, facelocationcamera):
        face_landmarks = face_recognition.face_landmarks(rgb_frame, facelocationcamera)[0]
        
        print(face_landmarks)
        if (facelocationcamera[0][1] - facelocationcamera[0][3]) > 50:
            print(facelocationcamera[0][1] - facelocationcamera[0][3])
            face_matching = face_recognition.compare_faces(face_encodings, faceencoding)
            print(face_matching)
            face_distance = face_recognition.face_distance(face_encodings, faceencoding)
            print(face_distance)
            face_matching = np.argmin(face_distance)
            if face_distance[face_matching]< 0.5:
                id = face_id[face_matching]
                name = "SELECT image_name FROM tabeldataset WHERE id = %(id)s";    
                val = {'id': id}
                cursor.execute(name, val)
                name = cursor.fetchone()
                name = str(name[0])
            else:
                id = 'Unknown'
                name = 'Unknown'
        else:
            print(facelocationcamera[0][1] - facelocationcamera[0][3])
            name = 'unknown'
        
        y1, x2, y2, x1 = facelocation
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(frame, name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX, 0.75,(255,255,255),2)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)
