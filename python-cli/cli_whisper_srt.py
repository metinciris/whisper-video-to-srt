#!/usr/bin/env python
import argparse
import os
import sys
import whisper


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


def main():
    parser = argparse.ArgumentParser(
        description="Whisper ile video / ses dosyasından SRT altyazı üret"
    )
    parser.add_argument("input", help="Video veya ses dosyası (mp4, mkv, wav vs.)")
    parser.add_argument(
        "-m",
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Kullanılacak Whisper modeli (varsayılan: medium)",
    )
    parser.add_argument(
        "-l",
        "--language",
        default=None,
        help="Dil kodu (örn: en, it, tr). Boş bırakılırsa otomatik algılar.",
    )
    parser.add_argument(
        "-t",
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="transcribe: orijinal dilde yaz, translate: İngilizceye çevir.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Çıkış SRT yolu. Boş bırakılırsa input dosya adıyla .srt üretir.",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"HATA: Dosya bulunamadı: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"[+] Model yükleniyor: {args.model}")
    model = whisper.load_model(args.model)

    print(f"[+] Transkripsiyon başlıyor: {args.input}")
    result = model.transcribe(
        args.input,
        language=args.language,
        task=args.task,
        verbose=True,
        fp16=False,  # GPU yoksa sorun çıkmasın diye
    )

    out_path = (
        args.output
        if args.output
        else os.path.splitext(args.input)[0] + ".srt"
    )

    print(f"[+] SRT kaydediliyor: {out_path}")
    save_srt(result["segments"], out_path)
    print("[+] Bitti.")


if __name__ == "__main__":
    main()
