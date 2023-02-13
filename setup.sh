curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
sudo mv ./ngrok /usr/bin/ngrok
ngrok config add-authtoken 2L9sr4R8oew4IbODsM4ookVF7Bk_43Kd4JSQnVWvKX8RmoYpS

pip install --upgrade pip 
#pip install "jax[cuda11_cudnn82]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

pip install --upgrade git+https://github.com/google/flax.git
pip install flask

pip install --upgrade jaxlib
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
sudo apt update && sudo apt install ffmpeg pip setuptools-rust einops

git config --global user.email ethantsliu@gmail.com
git config --global user.name Ethan Liu 
cp -r .ssh ~

ngrok http 91
