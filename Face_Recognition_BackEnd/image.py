import os
import sqlite3
import face_recognition
from PIL import Image, ImageDraw

def display_specific_face(image_name, db2, face_index):
    with sqlite3.connect(db2) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable5 WHERE image_name = ?", (image_name,))
        result = cursor.fetchone()

        if result:
            image_path = result[0]

            known_image_path = image_path
            image = face_recognition.load_image_file(known_image_path)

            face_locations = face_recognition.face_locations(image)

            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            if len(face_locations) == 0:
                print("No faces found. Check if the image contains faces.")
                return "tes"

            # Convert the image to a Pillow Image object
            pil_image = Image.fromarray(image)

            # Create a drawing context
            draw = ImageDraw.Draw(pil_image)

            # Define the color for the frame
            frame_color = (255, 0, 0)  # Red color

            if face_index >= len(face_locations):
                print("Invalid face index. There are fewer faces in the image.")
                return

            top, right, bottom, left = face_locations[face_index]

            draw.rectangle(((left, top), (right, bottom)), outline=frame_color, width=3)

            print(f"Drawn frame around face {face_index + 1}")

            pil_image.show()

        else:
            print("Image not found in the database.")


image_name = "team"
db2 = r"C:\Users\admin\Desktop\t3.db"

face_index = 0
display_specific_face(image_name, db2, face_index)

