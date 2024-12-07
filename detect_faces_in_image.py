import os
from PIL import Image
import face_recognition
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)





@app.route('/detect-faces', methods=['POST'])
def process_text():
    data = request.json
    image_name2 = data.get('text3')
    image_name = data.get('text4')
    print(image_name2)
    print(image_name)
    return open_image_by_name(image_name, image_name2)


def open_image_by_name(image_name1, image_name2):
    saved_image_paths = []
    # image_name = "test2"

    with sqlite3.connect(r"C:\Users\admin\Desktop\t3.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable5 WHERE image_name = ?", (image_name1,))
        result = cursor.fetchone()

        if result:
            image_path = result[0]

            known_image_path = image_path
            image = face_recognition.load_image_file(known_image_path)

            face_locations = face_recognition.face_locations(image)

            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            if len(face_locations) == 0:
                print("No faces found. Check if the image contains faces.")

            input_directory, input_filename = os.path.split(known_image_path)

            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

                face_filename = os.path.splitext(input_filename)[0] + f"_face_{i + 1}.jpg"
                face_filepath = os.path.join(input_directory, face_filename)

                pil_image.save(face_filepath)

                saved_image_paths.append(face_filepath)  # Append the path to the list

                print(f"Saved face {i + 1} as {face_filename}")

                # pil_image.show()

    print(saved_image_paths)

    with sqlite3.connect(r"C:\Users\admin\Desktop\t3.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable5 WHERE image_name = ?", (image_name2,))
        result1 = cursor.fetchone()
        print(result1)

        # cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name2,))
        result2 = saved_image_paths

        if result1 and result2:
            image_path1 = result1[0]
            image_path2 = result2[0]

            # Load the image files
            known_image = face_recognition.load_image_file(image_path1)
            unknown_image1 = face_recognition.load_image_file(image_path2)
            unknown_image2 = face_recognition.load_image_file(image_path2)

            # Encode the faces
            biden_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding1 = face_recognition.face_encodings(unknown_image1)[0]
            unknown_encoding2 = face_recognition.face_encodings(unknown_image2)[0]

            # Compare faces
            results1 = face_recognition.compare_faces([biden_encoding], unknown_encoding1)
            results2 = face_recognition.compare_faces([biden_encoding], unknown_encoding2)

            if results1[0]:
                print(f"{image_name2} is  in {image_name1}")
                return f"{image_name2} is in {image_name1}"
            elif results2[0]:
                print(f"{image_name2} is in {image_name1}")
                return f"{image_name2} is in {image_name1}"
            else:
                print(f"Faces of {image_name2} and {image_name1} do not match")
                return f"{image_name2} is not in {image_name1}"
        else:
            return f"At least one of the images not found."


if __name__ == '__main__':
    app.run(debug=True, port=8000)
