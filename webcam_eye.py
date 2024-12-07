import os
import json
import sqlite3

import cv2
import face_recognition
from flask import Flask

app = Flask(__name__)

@app.route('/eye')
def webcam():
    with sqlite3.connect(r"C:\Users\admin\Desktop\t.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path, image_name FROM ImageTable2")
        db_image_data = cursor.fetchall()

    reference_data = []

    for data in db_image_data:
        image_path = data[0]
        name = data[1]

        reference_image = face_recognition.load_image_file(image_path)
        reference_encodings = face_recognition.face_encodings(reference_image)

        if len(reference_encodings) > 0:
            reference_encoding = reference_encodings[0]
            reference_data.append({"encoding": reference_encoding, "name": name})
        else:
            print(f"No face found in {image_path}")

    eye_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, faces)

        for (top, right, bottom, left), face_encoding in zip(faces, face_encodings):
            name = "Unknown"

            for reference in reference_data:
                match = face_recognition.compare_faces([reference["encoding"]], face_encoding)[0]
                if match:
                    name = reference["name"]
                    break

            cv2.rectangle(frame, (left, top), (right, bottom), (252, 186, 3), 2)
            font = cv2.FONT_HERSHEY_DUPLEX

            face_roi = gray_frame[top:bottom, left:right]
            eyes = eye_detector.detectMultiScale(face_roi)

            for (eye_x, eye_y, eye_w, eye_h) in eyes:
                eye_x_absolute = left + eye_x
                eye_y_absolute = top + eye_y
                cv2.rectangle(frame, (eye_x_absolute, eye_y_absolute),
                              (eye_x_absolute + eye_w, eye_y_absolute + eye_h), (0, 255, 0), 2)

            cv2.putText(frame, name, (left + 6, bottom + 18), font, 0.5, (69, 82, 73), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return "webcam opened"


if __name__ == '__main__':
    app.run(debug=False, port=5400)
