# 🎬 Whisper Video → SRT Altyazı Aracı

Whisper tabanlı bu araç, video veya ses dosyalarından **otomatik SRT altyazı** üretir.
Hem **komut satırı (CLI)** hem de **grafik arayüz (GUI)** desteklenir.

✔ MP4, MKV, MOV, AVI, WAV, MP3 vb. çalışır
✔ Tek seferde **tam SRT dosyası** üretir
✔ Whisper'ın tüm modelleri desteklenir (`tiny` → `large`)
✔ CPU veya GPU üzerinde çalışabilir
✔ Python bilmeyen kullanıcılar için GUI mevcuttur

---

## 📁 Proje Yapısı

```text
whisper-video-to-srt/
├─ python-cli/
│  ├─ cli_whisper_srt.py
│  └─ requirements.txt
├─ python-gui/
│  ├─ whisper_gui_srt.py
│  └─ requirements.txt
└─ README.md
```

---

# 🚀 Özellikler

### 🔹 Video → SRT

Her dosya için:

* Otomatik konuşma tanıma
* Zaman kodlu altyazı
* Whisper segmentlerinden doğru formatta `.srt` yazımı

### 🔹 GUI (Grafik Arayüz)

Kolay kullanım:

* Video seç
* Model seç
* “Başlat” tuşuna bas
* İşlem bitince `.srt` otomatik oluşturulur

### 🔹 CLI (Komut Satırı)

Geliştiriciler için:

* Parametrelerle kontrol
* Dil ayarlama
* Model seçimi
* Çıktı yolunu belirtme

---

# 🔧 Kurulum

## 1️⃣ Python Gereksinimi

Python 3.9+ önerilir (3.13 dahil çalışır).

Whisper modelinin ses işleme yapabilmesi için **FFmpeg** gereklidir:

### Windows (scoop ile):

```bash
scoop install ffmpeg
```

### Windows (manuel):

[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

### Linux:

```bash
sudo apt install ffmpeg
```

### macOS:

```bash
brew install ffmpeg
```

---

# 🖥️ GUI (Python Bilmeden Kullanmak İsteyenler İçin)

## Çalıştırmak için:

```bash
cd python-gui
pip install -r requirements.txt
python whisper_gui_srt.py
```

### GUI Özellikleri:

* Video seçme
* Whisper modeli seçme (`tiny`, `base`, `small`, `medium`, `large`)
* Transkripsiyon ilerlemesini log penceresinde gösterme
* İşlem bitince `.srt` dosyası otomatik üretme

GUI ile üretilen dosya:

```
video1.mp4  → video1.srt
```

---

# 🧪 CLI Kullanımı (Geliştiriciler İçin)

## Kurulum:

```bash
cd python-cli
pip install -r requirements.txt
```

## Kullanım:

### 1. Orijinal dilde SRT çıkar:

```bash
python cli_whisper_srt.py "video.mp4"
```

### 2. Model seç:

```bash
python cli_whisper_srt.py "video.mp4" -m small
```

### 3. Dili zorla:

```bash
python cli_whisper_srt.py "video.mp4" -l en
```

### 4. İngilizceye çevirerek SRT üret:

(Whisper'ın translate modu **yalnızca İngilizceye çevirir**)

```bash
python cli_whisper_srt.py "video.mp4" -t translate
```

### 5. Çıkış dosyasını belirt:

```bash
python cli_whisper_srt.py "video.mp4" -o output.srt
```

---

# 🧠 Model Seçimi

| Model  | Hız  | Doğruluk | Öneri                      |
| ------ | ---- | -------- | -------------------------- |
| tiny   | ⚡⚡⚡  | ⭐        | Hız önemliyse              |
| base   | ⚡⚡   | ⭐⭐       | Basit içerikler            |
| small  | ⚡    | ⭐⭐⭐      | Dengeli                    |
| medium | 🔥   | ⭐⭐⭐⭐     | En iyi genel model         |
| large  | 🔥🔥 | ⭐⭐⭐⭐⭐    | En kaliteli fakat en yavaş |

**Patoloji dersleri, medikal videolar, aksanlı konuşmalar** → `medium` veya `large` tavsiye edilir.

---

# 📌 Bilinen Kısıtlar

* Whisper’ın `translate` modu yalnızca İngilizce çıkış üretir (Türkçe değil).
* GPU yoksa Large model **çok yavaş** olabilir.
* Elektrik kesintisinde Whisper kaldığı yerden devam edemez (segmentlere bölme önerilir).

---

# 📦 EXE Olarak Dağıtmak (İsteğe Bağlı)

Python bilmeyen kullanıcılar için GUI'yi `.exe`ye dönüştürebilirsin:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole whisper_gui_srt.py
```

Çıktı:

```
dist/whisper_gui_srt.exe
```

Bunu GitHub Releases kısmına ekleyebilirsin.

---

# ❤️ Katkı ve İletişim

Pull request’ler ve katkılar memnuniyetle kabul edilir.
Her türlü öneri ve geliştirme için issue açabilirsiniz.

---

