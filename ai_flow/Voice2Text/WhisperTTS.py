import whisper
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 这个似乎能直接从音频中提取出文本，而且时间戳，还挺准确
# 加载 Whisper 模型（可以选择较小的模型，如 'base'，或者更大的模型，如 'large'）
model = whisper.load_model("base")

# model.save_pretrained("model_whisper/")
# model = whisper.load_model("model_whisper/")

# 加载音频文件
audio = whisper.load_audio("../VideoFetch/file/2.mp3")
audio = whisper.pad_or_trim(audio)

# 获取音频的语言（Whisper 会自动检测语言）
result = model.transcribe(audio)

# 打印文本和时间戳
print(f"Transcription: {result['text']}")
for segment in result['segments']:
    print(f"Start: {segment['start']} - End: {segment['end']}")
    print(f"Text: {segment['text']}")
