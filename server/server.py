from flask import Flask, request, render_template

import os 
import whisper

from PIL import Image

import sys
sys.path.append("unified-io-inference")

from uio import runner
import numpy as np
from typing import  Dict
from transformers.pipelines.audio_utils import ffmpeg_read
import whisper
import torch

SAMPLE_RATE = 16000

whisper_model = whisper.load_model("base")

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
    img = Image.open(request.files['photo'])
    aud = request.files['audio'].read()
    #print(request.get_json())
    audio_nparray = ffmpeg_read(aud, SAMPLE_RATE)
    audio_tensor= torch.from_numpy(audio_nparray)
        
    # run inference pipeline
    result = whisper_model.transcribe(audio_nparray)

    # postprocess the prediction
    question = result["text"]
    print(request.files)
    print(request.form)
    print(request.data)

    #print (aud, "asdf")
    image = np.array(img.convert('RGB'))
    #q = request.form["question"]
    output = model.vqa(image, question)
    print(output)
    return {"text": output["text"]}

@app.route("/vavi", methods= ["POST"])
def vavi(): 
    return {"text": 1}


if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = "91")
    
    