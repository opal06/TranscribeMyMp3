import whisper
import ffmpeg
import numpy as np

class Transcriber:

    def __init__(self, model_size):
        self.model = whisper.load_model(model_size)

    def getAudioBuffer(self, file):
        out, _ = (
                    ffmpeg.input(file, threads=0)
                    .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
                    .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
                )
        audio_buffer = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
        return audio_buffer

    def transcribe(self, audio_buffer):
        result = self.model.transcribe(audio_buffer)
        return result
