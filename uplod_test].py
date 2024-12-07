import sqlite3
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        data = request.form

        image_name = data.get('imageName', '')
        region = data.get('imageRegion', '')

        # Get the absolute path where the file is saved
        full_path = os.path.abspath(file_path)

        # Open a connection to the SQLite database
        with sqlite3.connect(r"C:\Users\admin\Desktop\t4.db") as conn:
            cursor = conn.cursor()

            try:
                # Insert data into the database
                cursor.execute("INSERT INTO ImageTable (image_path, image_name, region) VALUES (?, ?, ?)",
                               (full_path, image_name, region))
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

        print("File saved at:", full_path)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
