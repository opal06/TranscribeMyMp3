#!/usr/bin/python3

import os
import inotify.adapters
from pathlib import Path
from transcriber import Transcriber


def writeToFile(result, out_file):
    with open(out_file, "w") as outf:
        outf.write(str(result))

def runTranscriber(in_file, model_size):
    t = Transcriber(model_size)
    buffer = t.getAudioBuffer(in_file)
    result = t.transcribe(buffer)
    return result["text"]

def runTranscriberSegments(in_file, model_size, start_time, stop_time):
    t = Transcriber(model_size)
    buffer = t.getAudioBufferSegments(in_file, start_time, stop_time)
    result = t.transcribe(buffer)
    return result["text"]

def main():
    in_dir = Path(os.environ["INPUT_DIR"]) if os.environ["INPUT_DIR"] else Path("/input")
    out_dir = Path(os.environ["OUTPUT_DIR"]) if os.environ["OUTPUT_DIR"] else Path("/output")
    model_size = os.environ["MODEL"]
    use_segments = os.environ["SPEAKER_RECOGNITION"]

    print(f"Loaded env variables: in_dir={in_dir}, out_dir={out_dir}, model_size={model_size}, use_segments={use_segments}")

    if use_segments == "True":
        use_segments = True
        filetype_filter = [".rttm"]
    else:
        use_segments = False
        filetype_filter = [".mp3", ".wav"]


    notifier = inotify.adapters.Inotify()
    notifier.add_watch(str(in_dir))
    print("Started notifier")

    for event in notifier.event_gen():
        if event is not None and "IN_CREATE" in event[1] and Path(event[3]).suffix in filetype_filter:
            if use_segments:
                seg_file = in_dir / event[3]
                in_file = (in_dir / event[3]).with_suffix(".mp3")
                out_file = (out_dir / event[3]).with_suffix(".txt")
                out_text = ""
                print(f"Detected new file {in_file}, creating segmented transcription...")
                with open(seg_file, "r") as seg_file:
                    segs = seg_file.readlines()
                for line in segs:
                    items = line.split(" ")
                    start_time = float(items[3])
                    stop_time = float(items[4])

                    transcript = runTranscriberSegments(in_file, model_size, start_time, stop_time)
                    formatted_transcript = f"{items[7]}: {transcript}\n\n"
                    out_text = out_text + formatted_transcript

                writeToFile(out_text, out_file)
                print(f"File transcribed, output written to {out_file}")
                in_file.unlink(missing_ok=True)

            else:
                in_file = in_dir / event[3]
                out_file = (out_dir / event[3]).with_suffix(".txt")
                print(f"Detected new file {in_file}, creating transcription...")
                transcript = runTranscriber(in_file, model_size)
                writeToFile(transcript, out_file)
                print(f"File transcribed, output written to {out_file}")
                in_file.unlink(missing_ok=True)

main()
