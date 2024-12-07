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