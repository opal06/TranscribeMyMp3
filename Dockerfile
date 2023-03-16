FROM python:3.10-slim-bullseye
COPY src/ /TranscribeMyMp3
COPY requirements.txt /TranscribeMyMp3

RUN pip install -r /TranscribeMyMp3/requirements.txt
CMD python /TranscribeMyMp3/main.py
