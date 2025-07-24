# stage2_audio_whisper.py
import sounddevice as sd
import whisper
import numpy as np

model = whisper.load_model("tiny")

def record_and_transcribe(seconds=5):
    fs = 16000
    print("🎙️ Recording...")
    audio = sd.rec(int(fs * seconds), samplerate=fs, channels=1)
    sd.wait()
    audio = np.squeeze(audio).astype(np.float32)  # 🔁 Added dtype casting

    print("🧠 Transcribing...")
    result = model.transcribe(audio, fp16=False)
    print("📝 You said:", result["text"])
    return result["text"]

if __name__ == "__main__":
    record_and_transcribe()
