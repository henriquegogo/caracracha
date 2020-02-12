import face_recognition
import numpy as np
from flask import Flask, jsonify, request, redirect
from datafaces import known_faces

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return '''<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<body style="margin:0;font-family:sans-serif;color:white">
    <form method="POST" action="analyse" enctype="multipart/form-data">
    <label style="text-align:center;position:fixed;top:0;bottom:0;width:100%;background-position:center;background-size:cover;background-image:url(https://blog.even3.com.br/wp-content/uploads/2019/04/saiba-como-e-por-que-fazer-crachas-para-eventos-1.png)">
        <br /><br />
        <h1>Cara-crachá</h1>
        <h3 id="processing" style="display:none">Processando...</h3>
        <input type="file" name="file" onchange="processing.style.display='block';this.form.submit()" style="display:none" />
    </label>
    </form>
</body>
'''

@app.route('/analyse', methods=['POST'])
def upload():
    file = request.files['file']

    if file and allowed_file(file.filename):
        return detect_faces_in_image(file)


def detect_faces_in_image(file_stream):
    img = face_recognition.load_image_file(file_stream)
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_name = "Nenhum rosto detectado"

    if len(unknown_face_encodings) > 0:
        distances = face_recognition.face_distance(list(known_faces.values()), unknown_face_encodings[0])
        match_index = np.argsort(distances)[0]
        face_name = list(known_faces.keys())[match_index] if distances[match_index] <= 0.6 else "Pessoa desconhecida"

    return '''
<body style="margin:0;padding:20px;height:100%;font-family:sans-serif;text-align:center;font-size:3em;background-image:url(https://blog.doity.com.br/wp-content/uploads/2019/01/crach%C3%A1-para-evento.png);background-size:150%;background-repeat:no-repeat;background-position:center top">
<h1 style="margin-top:50%">'''+ face_name + '</h1><br /><br /><a href="/">Tentar novamente</a>' +'''
</body>
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
