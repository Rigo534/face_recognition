import cv2
import mediapipe as mp
import os
import pickle
import face_recognition

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

camera = cv2.VideoCapture(0)
file = open("EncodeFile.pkl", 'rb')
face_encoded_with_names = pickle.load(file)
file.close()
face_encodings, face_names = face_encoded_with_names
face_images = []
path = 'Images'
dir = os.listdir(path)
# Menbaca semua gambar di file Images
# for file_images in dir:
#     current_img = cv2.imread(f'{path}/{file_images}')
#     face_images.append(current_img)
#     face_names.append(os.path.splitext(file_images)[0])
#     print(face_names)
    
# for img in face_images:
#     img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#     img_encoding = face_recognition.face_encodings(img)[0]
#     face_encodings.append(img_encoding)

video_capture = cv2.VideoCapture(0) 
while True:
    ret, frame = video_capture.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)
    
    face_locations = []
    for detection in results.detections:
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = frame.shape
        x, y, w, h = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
        face_locations.append((y, x+w, y+h, x))
    
    face_images = [frame[top:bottom, left:right] for (top, right, bottom, left) in face_locations]
    for face_image, (top, right, bottom, left) in zip(face_images, face_locations):
        face_encoding = face_recognition.face_encodings(face_image)
        # print(face_encoding)
        if len(face_encoding) > 0:
            matches = face_recognition.compare_faces(face_encodings, face_encoding[0], tolerance=0.5)
            name = "Unknown"
            if True in matches:
                distance = face_recognition.face_distance(face_encodings, face_encoding[0])
                print(distance)
                first_match_index = matches.index(True)
                name = face_names[first_match_index]
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # Tekan tombol 'q' untuk keluar dari program
        break
        
video_capture.release()
cv2.destroyAllWindows()