import os
import wave
import json
from vosk import Model, KaldiRecognizer

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(script_dir, "vosk-model-cn")
# model_path = "vosk-model-cn"
def load_vosk_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError("Please download the Vosk model first.")
    return Model(model_path)

def open_audio_file(file_path):
    wf = wave.open(file_path, "rb")
    if wf.getsampwidth() != 2:
        raise ValueError("Audio format not supported. Please ensure it is a 16-bit PCM WAV file.")
    return wf

# Load Vosk model
default_model = load_vosk_model(model_path)

# Open audio file
# audio_file = "../VideoFetch/file/output_audio.wav"
# wf = open_audio_file(audio_file)

def transcribe_audio_with_timestamps(model=default_model, wf=None):
    if wf is None:
        raise ValueError("Please provide an audio file to transcribe.")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)
    result = ""
    timestamps = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            partial_result = recognizer.Result()
            result += partial_result
            result_json = json.loads(partial_result)
            for word in result_json.get('result', []):
                word_text = word['word']
                start_time = word['start']
                end_time = word['end']
                timestamps.append((word_text, start_time, end_time))
    return result, timestamps




#  还是要保留测试代码
# Open audio file
# 这里好像只能处理wav的文件
audio_file = "../VideoFetch/file/output_audio.wav"
wf = open_audio_file(audio_file)
# Transcribe audio and extract timestamps
result, timestamps = transcribe_audio_with_timestamps(model=default_model, wf=wf)

# Print transcription with timestamps
print("Transcription with Timestamps:", len(timestamps))
for word, start, end in timestamps:
    print(f"Word: '{word}', Start: {start:.2f}s, End: {end:.2f}s")
#
# Print complete transcription
print("\nComplete Transcription:")
# print(result)