import cv2
import sqlite3
import face_recognition

def recognize_faces():
    with sqlite3.connect(r"C:\Users\admin\Desktop\face_recognition.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path, image_name FROM ImageTable")
        db_image_data = cursor.fetchall()

    reference_data = []

    for data in db_image_data:
        image_path = data[0]
        name = data[1]

        reference_image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(reference_image)

        if len(face_encodings) > 0:
            reference_encoding = face_encodings[0]
            reference_data.append({"encoding": reference_encoding, "image_name": name})
        else:
            print(f"No face found in {image_path}")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"

            for reference in reference_data:
                match = face_recognition.compare_faces([reference["encoding"]], face_encoding)[0]
                if match:
                    name = reference["image_name"]
                    break

            top, right, bottom, left = face_location
            rectangle_color = (252, 186, 3)
            cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (69, 82, 73), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

recognize_faces()
