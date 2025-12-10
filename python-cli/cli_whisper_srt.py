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
    filepath = filedialog.askopenfilename(
        title="Video veya Ses Dosyası Seç",
        filetypes=(
            ("Media Files", "*.mp4 *.mkv *.mp3 *.wav *.flac *.ogg"),
            ("All Files", "*.*"),
        ),
    )

    if not filepath:
        return

    # Dil seçimi
    selected_lang = language_var.get()
    if selected_lang == "Otomatik":
        lang_code = None
    elif selected_lang == "Türkçe":
        lang_code = "tr"
    elif selected_lang == "İngilizce":
        lang_code = "en"
    else:
        lang_code = None

    # Model seçimi
    selected_model = model_var.get()
    model_map = {
        "Hızlı": "small",
        "Orta": "medium",
        "Ağır": "large"
    }
    model_name = model_map[selected_model]

    status_var.set(f"Model yükleniyor ({selected_model})...")
    root.update_idletasks()

    try:
        model = whisper.load_model(model_name)

        status_var.set("Transkripsiyon yapılıyor...")
        root.update_idletasks()

        result = model.transcribe(
            filepath,
            language=lang_code,
            task="transcribe",
            fp16=False,
        )

        out_path = os.path.splitext(filepath)[0] + ".srt"
        save_srt(result["segments"], out_path)

        status_var.set("İşlem tamamlandı.")
        messagebox.showinfo("Bitti", f"SRT oluşturuldu:\n{out_path}")

    except Exception as e:
        status_var.set("Hata oluştu.")
        messagebox.showerror("Hata", str(e))

# ---- GUI ----
root = tk.Tk()
root.title("Whisper SRT Üretici")
root.geometry("360x260")

title_label = tk.Label(root, text="Whisper SRT Oluşturucu", font=("Arial", 14))
title_label.pack(pady=10)

# Dil seçimi
language_var = tk.StringVar(value="Otomatik")
language_frame = tk.Frame(root)
language_frame.pack(pady=5)

lang_label = tk.Label(language_frame, text="Dil:")
lang_label.pack(side=tk.LEFT, padx=5)

lang_options = ["Otomatik", "Türkçe", "İngilizce"]
lang_menu = tk.OptionMenu(language_frame, language_var, *lang_options)
lang_menu.pack(side=tk.LEFT)

# Model seçimi
model_var = tk.StringVar(value="Orta")
model_frame = tk.Frame(root)
model_frame.pack(pady=5)

model_label = tk.Label(model_frame, text="Model:")
model_label.pack(side=tk.LEFT, padx=5)

model_options = ["Hızlı", "Orta", "Ağır"]
model_menu = tk.OptionMenu(model_frame, model_var, *model_options)
model_menu.pack(side=tk.LEFT)

# Çalıştırma butonu
button = tk.Button(root, text="Video/Ses Seç ve SRT Üret", command=run_whisper)
button.pack(pady=15)

# Durum etiketi
status_var = tk.StringVar(value="Hazır.")
status_label = tk.Label(root, textvariable=status_var, fg="gray")
status_label.pack(pady=5)

root.mainloop()
