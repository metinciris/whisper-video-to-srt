#!/usr/bin/env python
import os
import whisper
import tkinter as tk
from tkinter import filedialog, messagebox

def to_srt_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msec = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{msec:03}"

def save_srt(segments, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = to_srt_time(seg["start"])
            end = to_srt_time(seg["end"])
            text = seg["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

def run_whisper():
    # Dosya seçtir
    filepath = filedialog.askopenfilename(
        title="Video veya Ses Dosyası Seç",
        filetypes=(
            ("Media Files", "*.mp4 *.mkv *.mp3 *.wav *.flac *.ogg"),
            ("All Files", "*.*"),
        ),
    )

    if not filepath:
        return

    try:
        messagebox.showinfo("Model", "Whisper modeli yükleniyor (medium)...")
        model = whisper.load_model("medium")

        messagebox.showinfo("Başladı", "Transkripsiyon başlıyor...")

        result = model.transcribe(filepath, fp16=False)

        out_path = os.path.splitext(filepath)[0] + ".srt"

        save_srt(result["segments"], out_path)

        messagebox.showinfo("Bitti", f"SRT oluşturuldu:\n{out_path}")

    except Exception as e:
        messagebox.showerror("Hata", str(e))

# Basit GUI
root = tk.Tk()
root.title("Whisper SRT Üretici")

root.geometry("300x150")

label = tk.Label(root, text="Whisper SRT Oluşturucu", font=("Arial", 14))
label.pack(pady=15)

button = tk.Button(root, text="Video/Ses Seç ve SRT Üret", command=run_whisper)
button.pack(pady=10)

root.mainloop()
