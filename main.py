import cv2
import numpy as np
import face_recognition
from encode_faces import load_and_encode_faces
from attendance_logger import mark_attendance, init_db

# Initialize database
init_db()

# Load known faces
known_encodings, known_names = load_and_encode_faces('images')

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces_current = face_recognition.face_locations(rgb_frame)
    encodes_current = face_recognition.face_encodings(rgb_frame, faces_current)

    for encode_face, face_loc in zip(encodes_current, faces_current):
        matches = face_recognition.compare_faces(known_encodings, encode_face)
        face_distance = face_recognition.face_distance(known_encodings, encode_face)
        match_index = np.argmin(face_distance)

        if matches[match_index]:
            name = known_names[match_index].upper()
            y1, x2, y2, x1 = face_loc
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, name, (x1, y2 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            mark_attendance(name)

    cv2.imshow('Face Attendance System', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
