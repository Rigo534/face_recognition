import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate('Program/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://facerecognitionattendanc-ff2b5-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket' : "facerecognitionattendanc-ff2b5.appspot.com"
})

face_encoding = []
face_images = []
face_id = []
path = "Images"
dir = os.listdir(path)
bucket = storage.bucket()

for file_images in dir:
    current_img = cv2.imread(f'{path}/{file_images}')
    face_images.append(current_img)
    face_id.append(os.path.splitext(file_images)[0])
    uploadfile = f'{path}/{file_images}'
    blob = bucket.blob(uploadfile)
    blob.upload_from_filename(uploadfile)
print(face_id)

for img in face_images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(img)[0]
    face_encoding.append(img_encoding)
print(face_encoding)
face_encoded_with_id = [face_encoding, face_id]

file = open("Encode", 'wb')
pickle.dump(face_encoded_with_id, file)
file.close()
print("File Saved")



