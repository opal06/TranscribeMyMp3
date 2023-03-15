#!/usr/bin/python3

import os
import inotify.adapters
from pathlib import Path
from transcriber import Transcriber


def writeToFile(result, out_file):
    with open(out_file, "w") as outf:
        outf.write(str(result))


def run_transcriber(in_file, model_size):
    t = Transcriber(model_size)
    buffer = t.getAudioBuffer(in_file)
    result = t.transcribe(buffer)
    return result["text"]


def main():
    in_dir = Path(os.environ["INPUT_DIR"])
    out_dir = Path(os.environ["OUTPUT_DIR"])
    model_size = os.environ["MODEL"]

    print(f"Loaded env variables: {in_dir}, {out_dir}, {model_size}")

    notifier = inotify.adapters.Inotify()
    notifier.add_watch(str(in_dir))
    print("Started notifier")

    for event in notifier.event_gen():
        if event is not None and "IN_CREATE" in event[1]:
            in_file = in_dir / event[3]
            out_file = (out_dir / event[3]).with_suffix(".txt")
            print(f"Detected new file {in_file}, creating transcription...")
            transcript = run_transcriber(in_file, model_size)
            writeToFile(transcript, out_file)
            print(f"File transcribed, output written to {out_file}")
            in_file.unlink(missing_ok=True)

main()
