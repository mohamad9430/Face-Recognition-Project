import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route('/process-images', methods=['POST'])
def process_image():
    data = request.form
    image_path = data[r'imagePath']
    image_name = data['imageName']
    print(f"Received image path in Python: {image_path}")
    print(image_name)

    send(image_path, image_name)

    return "Image processed successfully"


def send(path, name):
    print("Current Working Directory:", os.getcwd())

    path = "Image Path to save "
    name = "Image Name ou want to Save"


    with sqlite3.connect(r"C:\Users\admin\Desktop\t3.db") as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO ImageTable (image_name, image_path) VALUES (?, ?)", (name, path))

    print("Data inserted successfully.")



if __name__ == '__main__':
    app.run(debug=True, port=5600)
