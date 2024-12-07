import sqlite3
from PIL import Image
import face_recognition
import os




#Detect faces with images appearing



def detect_faces(image_name1, image_name2, db2):
    saved_image_paths = []

    with sqlite3.connect(db2) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable5 WHERE image_name = ?", (image_name1,))
        result = cursor.fetchone()

        if result:
            image_path = result[0]
            known_image_path = image_path
            known_image = face_recognition.load_image_file(known_image_path)

            face_locations = face_recognition.face_locations(known_image)

            if len(face_locations) == 0:
                print("No faces found in the reference image. Check if the image contains faces.")
                return

            input_directory, input_filename = os.path.split(known_image_path)

            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = known_image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

                face_filename = os.path.splitext(input_filename)[0] + f"_face_{i + 1}.jpg"
                face_filepath = os.path.join(input_directory, face_filename)

                pil_image.save(face_filepath)

                saved_image_paths.append(face_filepath)

    with sqlite3.connect(db2) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable5 WHERE image_name = ?", (image_name2,))
        result1 = cursor.fetchone()

        result2 = saved_image_paths

        if result1 and result2:
            image_path1 = result1[0]
            image_path2 = result2[0]

            known_image = face_recognition.load_image_file(image_path1)
            unknown_image1 = face_recognition.load_image_file(image_path2)

            biden_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding1 = face_recognition.face_encodings(unknown_image1)[0]

            results1 = face_recognition.compare_faces([biden_encoding], unknown_encoding1)

            if results1[0]:
                print(f"{image_name1} is in {image_name2}")
                print(f"Path of the matched face: {image_path2}")

                # Load and display the images
                reference_image = Image.open(image_path1)
                matching_face_image = Image.open(image_path2)

                reference_image.show()
                matching_face_image.show()

                return f"{image_name1} is in {image_name2}"
            else:
                print(f"Faces of {image_name1} and {image_name2} do not match")
                return f"{image_name1} is not in {image_name2}"
        else:
            return f"At least one of the images not found."


image_name1 = "t1"   # 1 individual
image_name2 = "team"   # individuals
db2 = r"C:\Users\admin\Desktop\t3.db"

detect_faces(image_name1, image_name2, db2)
