# Spike Voicer

### Runs basic voice commands on Lego Spike Prime hub

1. Install PyBricks firmware on the hub
2. Load Spike with robot_control.py using pybricks IDE.
3. How to run
```sh
git clone https://github.com/cestum/voicer.git

cd voicer
#Change "HUB_NAME" to Spike hub name in voice_to_commands.py

git submodules init 

git submodules update --init --recursive

cd whisper.cpp

sh ./models/download-ggml-model.sh base.en

cd ..

pip install -r requirements.py

python voice_to_commands.py
```
