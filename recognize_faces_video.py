import os
import sqlite3

import cv2
import face_recognition
from flask import Flask, request

app = Flask(__name__)


def load_reference_data_from_database():
    reference_data = []
    with sqlite3.connect(r"C:\Users\admin\Desktop\t3.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT image_path, image_name FROM ImageTable2")
        db_image_data = cursor.fetchall()

        for row in db_image_data:
            image_path, image_name = row
            reference_data.append({"path": image_path, "name": image_name.replace(" ", "_")})

    return reference_data


@app.route('/data', methods=['POST'])
def process_video():
    data = request.get_json()
    text_data = data['text']

    with sqlite3.connect(r"C:\Users\admin\Desktop\t.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT video_path FROM VideoTable WHERE video_name = ?", (text_data,))
        result1 = cursor.fetchone()

        if result1:
            # Check if result1 is not None
            cleaned_string = result1[0].replace("(", "").replace("'", "").replace(")", "").replace(",", "")
            print(cleaned_string)
        else:
            print("No matching record found.")

    print(f"Received data in Python: {text_data}")

    reference_data = load_reference_data_from_database()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    input_video_path = cleaned_string
    cap = cv2.VideoCapture(input_video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_video_path = "output_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    known_face_encodings = []
    known_face_names = []
    for item in reference_data:
        image_path = item["path"]
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            encoding = face_encodings[0]
            known_face_encodings.append(encoding)
            known_face_names.append(item["name"])
        else:
            print(f"No face detected in {image_path}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (x, y, w, h), face_encoding in zip(faces, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if any(matches):
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (66, 135, 245), 2)

        out.write(frame)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True, port=5800)
