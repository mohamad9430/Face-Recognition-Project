import os
import sqlite3
from flask import Flask, request, jsonify
import face_recognition
from PIL import Image
import cv2

app = Flask(__name__)
db = r"C:\Users\admin\Desktop\t.db"
db2 = r"C:\Users\admin\Desktop\t3.db"
db3 = r"C:\Users\admin\Desktop\t4.db"


def load_reference_data_from_database():
    reference_data = []
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT image_path, image_name FROM ImageTable2")
        db_image_data = cursor.fetchall()

        for row in db_image_data:
            image_path, image_name = row
            reference_data.append({"path": image_path, "name": image_name.replace(" ", "_")})

    return reference_data


def compare_images(image_name1, image_name2):
    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name1,))
        result1 = cursor.fetchone()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name2,))
        result2 = cursor.fetchone()
        print(result2)

        if result1 and result2:

            image_path1 = result1[0]
            image_path2 = result2[0]

            print(image_path1)
            print(image_path2)

            known_image = face_recognition.load_image_file(image_path1)
            unknown_image1 = face_recognition.load_image_file(image_path2)
            unknown_image2 = face_recognition.load_image_file(image_path2)

            biden_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding1 = face_recognition.face_encodings(unknown_image1)[0]
            unknown_encoding2 = face_recognition.face_encodings(unknown_image2)[0]

            results1 = face_recognition.compare_faces([biden_encoding], unknown_encoding1)
            results2 = face_recognition.compare_faces([biden_encoding], unknown_encoding2)



            if results1[0]:
                print(f"Face of {image_name1} matches with {image_name2}")
                reference_image = Image.open(image_path1)
                matching_face_image = Image.open(image_path2)

                reference_image.show()
                matching_face_image.show()
                return f"Face of {image_name1} matches with {image_name2}"
            elif results2[0]:
                reference_image = Image.open(image_path1)
                matching_face_image = Image.open(image_path2)

                reference_image.show()
                matching_face_image.show()
                return f"Face of {image_name1} matches with {image_name2}"
            else:
                return f"Faces of {image_name1} and {image_name2} do not match"
        else:
            return f"At least one of the images not found."


def authenticate_user(username, password):
    conn = sqlite3.connect("C:\\Users\\admin\\Desktop\\t4.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data:
        if password == user_data[2]:
            print("Authentication successful!")
            conn.close()
            return "Authentication successful"
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")

    conn.close()
    return "Authentication failed"


def send(path, name):
    print("Current Working Directory:", os.getcwd())

    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO ImageTable (image_name, image_path) VALUES (?, ?)",
                       (name, path))

    print("Data inserted successfully.")


def send3(path, name, region):
    # print("Current Working Directory:", os.getcwd())

    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO ImageTable (image_name, image_path, region) VALUES (?, ?, ?)",
                       (name, path, region))

    print("Data inserted successfully.")


def check_admin_user_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
    count = cursor.fetchone()[0]
    return count > 0


def update_row(username, password, column2_value, column3_value):
    conn = sqlite3.connect(r'C:\Users\admin\Desktop\t4.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()

    if row:
        cursor.execute("UPDATE users SET upload=?, detection=? WHERE username=?",
                       (column2_value, column3_value, username))
        conn.commit()
        conn.close()
        print("Permissions updated successfully!")
        return "Permissions updated successfully!"
    else:
        conn.close()
        print("Username or password incorrect.")
        return "Username or password incorrect."


def extract_images(image_name):
    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name,))
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


def detect_faces(image_name1, image_name2):
    extracted_face_paths = []  # Initialize an empty list to store the paths of extracted face images

    # image_name2 = "crowd_test3"

    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name2,))
        result = cursor.fetchone()

        if result:
            image_path = result[0]

            known_image_path = image_path
            image = face_recognition.load_image_file(known_image_path)

            face_locations = face_recognition.face_locations(image)

            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            if len(face_locations) == 0:
                print("No faces found. Check if the image contains faces.")
                return []

            input_directory, input_filename = os.path.split(known_image_path)

            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

                face_filename = os.path.splitext(input_filename)[0] + f"_face_{i + 1}.jpg"
                face_filepath = os.path.join(input_directory, face_filename)

                pil_image.save(face_filepath)

                print(f"Saved face {i + 1} as {face_filename}")

                extracted_face_paths.append((face_filepath, f"Face_{i + 1}"))
                print(extracted_face_paths)

                # pil_image.show()

    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name1,))
        result1 = cursor.fetchone()

        if result1 and extracted_face_paths:

            image_path1 = result1[0]

            print(image_path1)

            known_image = face_recognition.load_image_file(image_path1)
            biden_encoding = face_recognition.face_encodings(known_image)[0]

            for extracted_face_path, face_name in extracted_face_paths:
                unknown_image = face_recognition.load_image_file(extracted_face_path)
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                result = face_recognition.compare_faces([biden_encoding], unknown_encoding)

                if result[0]:
                    print(f"Face of {image_name1} is in {image_name2}")
                    reference_image = Image.open(image_path)
                    matching_face_image = Image.open(image_path1)


                    reference_image.show()
                    matching_face_image.show()
                    return f"Face of {image_name1} is in {image_name2}"

            print(f"No match found for {image_name1}")
            return f"No match found for {image_name1}"

        else:
            print(f"At least one of the images not found.")
            return f"At least one of the images not found."


def send2(path, name):
    print("Current Working Directory:", os.getcwd())

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        video_name = name
        video_path = path

        cursor.execute("INSERT INTO VideoTable (video_name, video_path) VALUES (?, ?)", (video_name, video_path))


@app.route('/login', methods=['POST'])
def login():
    global global_username_input
    data = request.json
    username = data.get('text3')
    password = data.get('text4')
    if authenticate_user(username, password) == "Authentication successful":
        global_username_input = username
        print("Stored username:", global_username_input)
        return "Authentication successful"
    else:
        return "Username or password incorrect"



@app.route('/search-database', methods=['POST', 'GET'])
def process_images():
    data = request.form
    image_name1 = data['imageName']
    print(image_name1)

    extracted_face_paths = []

    # image_name1 = "moh1"

    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM ImageTable WHERE image_name = ?", (image_name1,))
        result = cursor.fetchone()

        if result:
            image_path = result[0]

            known_image_path = image_path
            image = face_recognition.load_image_file(known_image_path)

            face_locations = face_recognition.face_locations(image)

            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            if len(face_locations) == 0:
                print("No faces found. Check if the image contains faces.")
                return []

            input_directory, input_filename = os.path.split(known_image_path)

            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

                face_filename = os.path.splitext(input_filename)[0] + f"_face_{i + 1}.jpg"
                face_filepath = os.path.join(input_directory, face_filename)

                pil_image.save(face_filepath)

                print(f"Saved face {i + 1} as {face_filename}")

                extracted_face_paths.append((face_filepath, f"Face_{i + 1}"))
                print(extracted_face_paths)

    with sqlite3.connect(db3) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT image_name, image_path FROM ImageTable"
                       " WHERE image_name != ?",
                       (image_name1,))
        result1 = cursor.fetchall()
        print(result1)

        if result1 and extracted_face_paths:

            for image_name, image_path1 in result1:
                print(image_name, image_path1)

                known_image = face_recognition.load_image_file(image_path1)
                biden_encodings = face_recognition.face_encodings(known_image)

                for biden_encoding in biden_encodings:
                    for extracted_face_path, face_name in extracted_face_paths:
                        unknown_image = face_recognition.load_image_file(extracted_face_path)
                        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                        result = face_recognition.compare_faces([biden_encoding], unknown_encoding)

                        if result[0]:
                            print(f"Face of {image_name1} is in {image_name}")
                            reference_image = Image.open(known_image_path)
                            matching_face_image = Image.open(image_path1)

                            reference_image.show()
                            matching_face_image.show()
                            return f"Face of {image_name1} is in {image_name}"

                print(f"No match found for {image_name1}")
                return f"No match found for {image_name1}"

        else:
            print(f"At least one of the images not found.")

@app.route('/bool', methods=['GET', 'POST'])
def get_boolean_values():
    global global_username_input
    print("Stored username:", global_username_input)
    if global_username_input:
        conn = sqlite3.connect("C:\\Users\\admin\\Desktop\\t4.db")
        cursor = conn.cursor()

        cursor.execute("SELECT upload, detection, is_admin FROM users WHERE username = ?", (global_username_input,))
        row = cursor.fetchone()

        if row:
            upload_value = bool(row[0])
            detection_value = bool(row[1])
            is_admin = bool(row[2])
            cursor.close()
            conn.close()
            print("Upload Value:", upload_value)
            print("Detection Value:", detection_value)
            print("IsAdmin Value:", is_admin)
            return jsonify({'upload': upload_value, 'detection': detection_value, 'is_admin': is_admin})
        else:
            cursor.close()
            conn.close()
            return 'Boolean values not found', 404
    else:
        return 'User not logged in', 401


@app.route('/create-account', methods=['POST'])
def create_account():
    conn = sqlite3.connect(db3)
    cursor = conn.cursor()

    data = request.json
    upload = data.get('text3')

    detection = data.get('text4')

    user_name = data.get('text5')

    password2 = data.get('text6')

    admin_username = user_name

    password = password2

    is_admin_input = "false"

    is_admin = is_admin_input == 'true'

    cursor.execute('''INSERT INTO users (username, password, is_admin, upload, detection)
                              VALUES (?, ?, ?, ?, ?)''', (admin_username, password, is_admin, upload, detection))

    print("User inserted successfully.")

    conn.commit()
    conn.close()

    print(user_name)
    print(password2)
    print(upload)
    print(detection)
    return "User inserted successfully."


@app.route('/process-images', methods=['POST'])
def process_image():
    data = request.form
    image_path = data[r'imagePath']
    image_name = data['imageName']
    region = data['imageRegion']
    print(f"Received image path in Python: {image_path}")
    print(image_name)

    send3(image_path, image_name, region)

    return "Images processed successfully"


@app.route('/create-admin', methods=['POST'])
def create_admin():
    conn = sqlite3.connect(db3)
    cursor = conn.cursor()

    data = request.json
    ad_user_name = data.get('text3')
    password2 = data.get('text4')

    admin_username = ad_user_name
    password = password2
    is_admin_input = "true"
    is_admin = is_admin_input == 'true'
    upload = True
    detection = True

    cursor.execute('''INSERT INTO users (username, password, is_admin, upload, detection)
                          VALUES (?, ?, ?, ?, ?)''', (admin_username, password, is_admin, upload, detection))

    print("Admin user inserted successfully.")

    conn.commit()
    conn.close()

    return "Admin user inserted successfully."


@app.route('/check-admin', methods=['GET'])
def check_admin():
    conn = sqlite3.connect(db3)
    cursor = conn.cursor()

    if check_admin_user_exists(cursor):
        conn.close()
        return "There is at least one admin user."
    else:
        conn.close()
        return "There are no admin users."


@app.route('/compare-faces', methods=['POST'])
def process_text():
    data = request.json
    text1 = data.get('text5')
    text2 = data.get('text6')
    print(text1)
    print(text2)
    return compare_images(text1, text2)


@app.route('/edit', methods=['POST'])
def create_account2():
    data = request.json
    upload = data.get('text3')
    detection = data.get('text4')
    user_name = data.get('text5')
    password2 = data.get('text6')

    result = update_row(user_name, password2, upload, detection)
    print(user_name)
    print(password2)
    print(upload)
    print(detection)
    return result


@app.route('/detect-faces', methods=['POST'])
def process_text2():
    data = request.json
    image_name2 = data.get('text3')
    image_name = data.get('text4')
    print(image_name2)
    print(image_name)
    return detect_faces(image_name, image_name2)


@app.route('/recognize-video', methods=['POST'])
def process_video():
    data = request.get_json()
    text_data = data['text']

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT video_path FROM VideoTable WHERE video_name = ?", (text_data,))
        result1 = cursor.fetchone()

        if result1:
            cleaned_string = result1[0].replace("(", "").replace("'", "").replace(")", "").replace(",", "")
            print(cleaned_string)
        else:
            print("No matching record found.")

    print(f"Received data in Python: {text_data}")

    reference_data = load_reference_data_from_database()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    input_video_path = cleaned_string
    cap = cv2.VideoCapture(input_video_path)
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_video_path = "output_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    known_face_encodings = []
    known_face_names = []
    for item in reference_data:
        image_path = item["path"]
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            encoding = face_encodings[0]
            known_face_encodings.append(encoding)
            known_face_names.append(item["name"])
        else:
            print(f"No face detected in {image_path}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (x, y, w, h), face_encoding in zip(faces, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if any(matches):
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (66, 135, 245), 2)

        out.write(frame)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.resizeWindow("Frame", 200, 400)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return "done"


@app.route('/upload-video', methods=['POST'])
def upload_video():
    try:
        data = request.form
        video_path = data['videoPath']
        video_name = data['videoName']
        print(f"Received video path in Python: {video_path}")
        print(video_name)

        send2(video_path, video_name)

        return "Video processed successfully"
    except Exception as e:
        print(f"Error processing video: {e}")
        return "Internal Server Error", 500


@app.route('/extract', methods=['GET', 'POST'])
def get_text():
    data = request.get_json()
    text = data['text1']
    print(f"Received data in Python: {text}")
    extract_images(text)
    return "Done"


if __name__ == '__main__':
    app.run(debug=True, port=8000)
