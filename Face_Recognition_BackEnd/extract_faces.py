import os
import sqlite3
import face_recognition
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)
text1 = None


@app.route('/extract', methods=['GET', 'POST'])
def process_text():
    data = request.get_json()
    text = data['text1']
    print(f"Received data in Python: {text}")
    return extract_images(text)


def extract_images(image_name):
    with sqlite3.connect(r"C:\Users\admin\Desktop\face_recognition.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name,))
        result = cursor.fetchone()
        print(result)

        if result:
            image_path = result[0]

            known_image_path = image_path
            image = face_recognition.load_image_file(known_image_path)

            face_locations = face_recognition.face_locations(image)

            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            if len(face_locations) == 0:
                print("No faces found. Check if the image contains faces.")
                return "tes"

            input_directory, input_filename = os.path.split(known_image_path)

            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

                face_filename = os.path.splitext(input_filename)[0] + f"_face_{i + 1}.jpg"
                face_filepath = os.path.join(input_directory, face_filename)

                pil_image.save(face_filepath)

                print(f"Saved face {i + 1} as {face_filename}")

                pil_image.show()


extract_images(image_name="dr2")

# if __name__ == '__main__':
#     app.run(debug=True, port=5300)
