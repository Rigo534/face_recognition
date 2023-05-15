import cv2
import face_recognition
import pickle
import os

face_encoding = []
face_images = []
face_id = []
path = "Images"
dir = os.listdir(path)


for file_images in dir:
    current_img = cv2.imread(f'{path}/{file_images}')
    face_images.append(current_img)
    face_id.append(os.path.splitext(file_images)[0])

print(face_id)

for img in face_images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(img)[0]
    face_encoding.append(img_encoding)
face_encoded_with_id = [face_encoding, face_id]

file = open("Encode", 'wb')
pickle.dump(face_encoded_with_id, file)
file.close()
print("File Saved")



