# TranscribeMyMp3

Inspired by [ocrmypdf-auto](https://github.com/cmccambridge/ocrmypdf-auto/tree/master), this program watches a folder for new audio files and uses OpenAI's [Whisper](https://github.com/openai/whisper) to create a transcript which is saved as text file in the output folder. It will run on CPU only, but should be able to make use of NVIDIA GPUs if present. This has not been tested though.

## Setup
```bash
# Clone repository and enter the folder
git clone https://github.com/opal06/TranscribeMyMp3.git && cd TranscribeMyMp3/

# Optional: Create a python virtual environment and enter it
python3.10 -m venv ./.venv
source .venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Set environment variables
export INPUT_DIR="./input"  #The input folder to watch
export OUTPUT_DIR="./output"  #The output folder to save to>
export MODEL="medium"       #The Whisper model to load; see below for options>
export SPEAKER_RECOGNITION=False    #Experimental: Enable support for speaker segmentation files>

# Run the program
python3 main.py
```
In future, Docker images will be available to easily deploy it on a server.

## Configuration
As it is meant to be deployed with Docker, it is configured through environment variables. These variables are currently supported:

`INPUT_DIR`: Path to the folder that should be watched for new files. Currently, files will be **removed** from this folder once processed.

`OUTPUT_DIR`: Path to the folder where the transcript will be saved.

`MODEL`: Defines which model size should be used by Whisper. Available model sizes are `"tiny"`, `"base"`, `"small"`, `"medium"` and `"large"`. Results improve with larger models, but so does computational intensity and required time. 

`SPEAKER_RECOGNITION`: This looks for a `.rttm` file (and the related audio file) instead of just audio files, as to offer support for speaker diarization done by a different model in the future. For now, this is experimental and the program cannot perform speaker diarization itself.

