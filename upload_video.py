import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route('/upload-video', methods=['POST'])
def process_video():
    try:
        data = request.form
        video_path = data['videoPath']
        video_name = data['videoName']
        print(f"Received video path in Python: {video_path}")
        print(video_name)

        send(video_path, video_name)

        return "Video processed successfully"
    except Exception as e:
        print(f"Error processing video: {e}")
        return "Internal Server Error", 500


def send(path, name):
    print("Current Working Directory:", os.getcwd())

    with sqlite3.connect(r"C:\Users\admin\Desktop\t.db") as conn:
        cursor = conn.cursor()

        video_name = name
        video_path = path

        cursor.execute("INSERT INTO VideoTable (video_name, video_path) VALUES (?, ?)", (video_name, video_path))


if __name__ == '__main__':
    app.run(debug=True, port=5500)
