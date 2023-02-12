from flask import Flask, request, render_template

from PIL import Image

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/vqa", methods= ["POST"])
def vqa():
    file1 = request.files['image']
    img = Image.open(file1)
    text = "Hello"
    print(text)
    return {"text": text}
if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = "91")