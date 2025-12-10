#!/usr/bin/env python
import os
import whisper
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import scrolledtext
import threading

def to_srt_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msec = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{msec:03}"

def build_srt_text(segments) -> str:
    """Segmentlerden tam SRT metni üret."""
    lines = []
    for i, seg in enumerate(segments, start=1):
        start = to_srt_time(seg["start"])
        end = to_srt_time(seg["end"])
        text = seg["text"].strip()

        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")  # boş satır
    return "\n".join(lines)

def on_transcription_complete(out_path: str, srt_text: str):
    """İşlem başarıyla bitince GUI güncellemesi."""
    progress.stop()
    status_var.set("Tamamlandı.")

    # Panelde SRT’yi göster
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, srt_text)
    output_text.configure(state="disabled")

    messagebox.showinfo("Bitti", f"SRT oluşturuldu:\n{out_path}")

def on_transcription_error(error_msg: str):
    """Hata olunca GUI güncellemesi."""
    progress.stop()
    status_var.set("Hata oluştu.")
    messagebox.showerror("Hata", error_msg)

def transcribe_thread(filepath, lang_code, model_name, model_label):
    try:
        # Model yükleniyor
        def set_loading():
            status_var.set(f"Model yükleniyor ({model_label})...")
        root.after(0, set_loading)
        progress.start(10)

        model = whisper.load_model(model_name)

        def set_transcribing():
            status_var.set("Transkripsiyon yapılıyor...")
        root.after(0, set_transcribing)

        result = model.transcribe(
            filepath,
            language=lang_code,
            task="transcribe",
            fp16=False,
        )

        out_path = os.path.splitext(filepath)[0] + ".srt"
        srt_text = build_srt_text(result["segments"])

        # Dosyaya yaz
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(srt_text)

        # GUI’yi ana thread’den güncelle
        root.after(0, on_transcription_complete, out_path, srt_text)

    except Exception as e:
        root.after(0, on_transcription_error, str(e))

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
    model_map = {
        "Hızlı": "small",
        "Orta": "medium",
        "Ağır": "large"
    }
    selected_model_label = model_var.get()
    model_name = model_map[selected_model_label]

    # Önce paneli temizle
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "İşlem başladı, lütfen bekleyin...\n")
    output_text.configure(state="disabled")

    status_var.set("Hazırlanıyor...")
    progress.start(10)

    # Transkripsiyon ayrı thread’de (GUI donmasın)
    thread = threading.Thread(
        target=transcribe_thread,
        args=(filepath, lang_code, model_name, selected_model_label),
        daemon=True,
    )
    thread.start()

# ---- GUI ----
root = tk.Tk()
root.title("Whisper SRT Üretici")
root.geometry("500x450")

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

# Başlatma butonu
button = tk.Button(root, text="Video/Ses Seç ve SRT Üret", command=run_whisper)
button.pack(pady=15)

# Progress bar
progress = ttk.Progressbar(root, mode="indeterminate", length=350)
progress.pack(pady=5)

# Durum etiketi
status_var = tk.StringVar(value="Hazır.")
status_label = tk.Label(root, textvariable=status_var, fg="gray")
status_label.pack(pady=5)

# SRT çıktısı için panel (kaydırılabilir metin alanı)
output_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill="both", expand=True)
output_text.configure(state="disabled")

root.mainloop()
