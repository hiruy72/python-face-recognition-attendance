import cv2
import face_recognition
import os

def load_and_encode_faces(path='images'):
    images = []
    names = []

    for file in os.listdir(path):
        img = cv2.imread(f'{path}/{file}')
        if img is None:
            continue
        images.append(img)
        names.append(os.path.splitext(file)[0])

    encodings = []
    for img in images:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(rgb_img)
        if encode:
            encodings.append(encode[0])

    print(f"[INFO] Encoded {len(encodings)} faces.")
    return encodings, names
