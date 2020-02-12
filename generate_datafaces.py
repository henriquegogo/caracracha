from sys import argv
from glob import glob
import face_recognition

files = glob(argv[1])
datafaces = {}

for filepath in files:
    name = filepath.split(".")[0].split("/")[-1]
    image = face_recognition.load_image_file(filepath)
    image_encoding = face_recognition.face_encodings(image)[0]
    datafaces[name] = list(image_encoding)

print("known_faces = ")
print(datafaces)
