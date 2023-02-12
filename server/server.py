from flask import Flask, request, render_template

import os

from PIL import Image

import sys
sys.path.append("unified-io-inference")

from uio import runner
import numpy as np


os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"]="false"
os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"]=".XX"
os.environ["XLA_PYTHON_CLIENT_ALLOCATOR"]="platform"

model = runner.ModelRunner("large", "/notebooks/chkpts/large_1000k.bin")


UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/vqa", methods= ["POST"])
def vqa():
    #print(request.get_json())
    print(request.files)
    print(request.form)
    print(request.data)
    
    img = Image.open(request.files['file'])
    image = np.array(img.convert('RGB'))
    q = request.form["question"]
    output = model.vqa(image, q)
    print (output["text"])
    return {"text": output["text"]}

@app.route("/vavi", methods= ["POST"])
def vavi(): 
    return {"text": 1}




if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = "91")
    
    