import face_recognition
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/process-images', methods=['POST'])
def process_text():
    data = request.json
    image_name2 = data.get('text1')
    image_name = data.get('text2')
    print(image_name2)
    print(image_name)
    # You can add your processing logic here

    # Return a JSON response
    return jsonify({'message': 'Images processed successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=5200)
