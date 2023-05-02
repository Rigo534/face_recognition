import cv2
import face_recognition
import pickle
import os

face_encoding = []
face_images = []
face_names = []
path = "Images"
dir = os.listdir(path)

for file_images in dir:
    current_img = cv2.imread(f'{path}/{file_images}')
    face_images.append(current_img)
    face_names.append(os.path.splitext(file_images)[0])
print(face_names)

for img in face_images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(img)[0]
    face_encoding.append(img_encoding)
print(face_encoding)
face_encoded_with_names = [face_encoding, face_names]

file = open("EncodeFile.pkl", 'wb')
pickle.dump(face_encoded_with_names, file)
file.close()
print("File Saved")


