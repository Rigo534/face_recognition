import face_recognition
import pickle
import os
import io
import numpy as np
from PIL import Image
import mysql.connector

face_encoding = []
face_images = []
path = "Images"
dir = os.listdir(path)

connect = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="coba_db"
)

cursor = connect.cursor()
Query = "SELECT image_name FROM TabelDataset"
execute = cursor.execute(Query)
result = cursor.fetchall()
face_names = [item for sublist in result for item in sublist]
print(face_names)


Query = "SELECT photo_id FROM TabelDataSet"

execute = cursor.execute(Query)
for img in cursor.fetchall():
    img_bytes = io.BytesIO(img[0])
    pil_image = Image.open(img_bytes)
    np_array = np.array(pil_image)
    encoding = face_recognition.face_encodings(np_array)
    face_encoding.extend(encoding)

face_encoded_with_names = [face_encoding, face_names]

print(face_encoded_with_names)
file = open("Encode", 'wb')
pickle.dump(face_encoded_with_names, file)
file.close()
print("File Saved")





