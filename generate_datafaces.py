""" Generate processed faces database """
from sys import argv
from glob import glob
import face_recognition

FILES = glob(argv[1])
DATAFACES = {}

for filepath in FILES:
    name = filepath.split(".")[0].split("/")[-1]
    image = face_recognition.load_image_file(filepath)
    image_encodings = face_recognition.face_encodings(image)
    if image_encodings:
        DATAFACES[name] = list(image_encodings[0])

print("known_faces = ")
print(DATAFACES)
