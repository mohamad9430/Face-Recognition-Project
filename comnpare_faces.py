import sqlite3
from flask import Flask, request, jsonify
import face_recognition
from PIL import Image

app = Flask(__name__)

# Path to the SQLite database
db2 = r"C:\Users\admin\Desktop\t3.db"

# Function to process image by image name
def open_image_by_name(image_name1):
    with sqlite3.connect(db2) as conn:
        cursor = conn.cursor()

        # Fetch the image path for the specified image name
        cursor.execute("SELECT image_path FROM ImageTable5 WHERE image_name = ?", (image_name1,))
        result1 = cursor.fetchone()

        if result1:
            image_path1 = result1[0]  # Extract the image path from the tuple result1

            # Load the known image and encode it
            known_image = face_recognition.load_image_file(image_path1)
            biden_encoding = face_recognition.face_encodings(known_image)[0]

            # Fetch all image paths and specific text values except for the first one
            cursor.execute("SELECT image_name, image_path, region FROM ImageTable5 WHERE image_name != ?",
                           (image_name1,))
            result2 = cursor.fetchall()

            for image_name, image_path, specific_text in result2:
                # Load the unknown image and encode it
                unknown_image = face_recognition.load_image_file(image_path)
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                # Compare face encodings
                results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

                if results[0]:
                    print(f"Face of {image_name1} matches with {image_name}")
                    print(f"Path of the matching image: {image_path}")
                    print(f"Specific text value: {specific_text}")

                    # Open and display the images
                    reference_image = Image.open(image_path1)
                    matching_image = Image.open(image_path)

                    reference_image.show()
                    matching_image.show()
                else:
                    print(f"Face of {image_name1} does not match with {image_name}")
        else:
            print(f"Image {image_name1} not found in the database.")


@app.route('/data', methods=['POST'])
def process_image():
    data = request.form
    image_name = data['imageName']
    print(image_name)

    open_image_by_name(image_name)

    return "Images processed successfully"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
