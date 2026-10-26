#!/usr/bin/env python3
"""Fotos und Videos der Kundin in einem Rutsch websitefertig machen.

Aufruf:  python3 werkzeuge/medien.py ORDNER_DATEIEN_ODER_LINKS...
         python3 werkzeuge/medien.py --vorschau video-3 5   (Kandidat 5 als Vorschaubild für video-3)

- Links   -> Google-Drive-Ordner/-Datei („Jeder mit dem Link“) oder Dropbox werden erst heruntergeladen
- Videos  -> site/videos/video-N.mp4 (H.264, max. 720p, Ton bleibt, schnellstartend)
             + site/videos/video-N.webp (vorläufiges Vorschaubild)
             + werkzeuge/ausgabe/kandidaten-video-N.jpg (12 nummerierte Standbilder zur Auswahl)
- Fotos   -> site/bilder/foto-N.webp (max. 1600 px, richtig gedreht)
- Übersicht -> werkzeuge/ausgabe/uebersicht.jpg (alle Ergebnisse nummeriert auf einem Blatt,
             damit Claude mit einem Blick sieht, was wohin passt)

Vorhandene Dateien werden nicht überschrieben, die Nummerierung läuft weiter.
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parent.parent
VID_DIR, IMG_DIR = ROOT / "site/videos", ROOT / "site/bilder"
OUT = ROOT / "werkzeuge/ausgabe"
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".avi", ".mkv", ".3gp"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".gif", ".bmp", ".tif", ".tiff"}


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def next_name(folder, prefix, ext):
    n = 1
    while (folder / f"{prefix}-{n}{ext}").exists():
        n += 1
    return folder / f"{prefix}-{n}{ext}"


def duration(path):
    info = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", str(path)]))
    return float(info["format"].get("duration") or 0)


def score(img):
    # Schärfe (Kanten) und nicht zu dunkel: ein guter Moment fürs Vorschaubild
    gray = img.convert("L").resize((270, 480))
    edges = ImageStat.Stat(gray.filter(ImageFilter.FIND_EDGES)).var[0]
    bright = ImageStat.Stat(gray).mean[0]
    return edges * (0.4 if bright < 60 or bright > 215 else 1)


def candidates_dir(name):
    return OUT / "kandidaten" / name


def video(src):
    dst = next_name(VID_DIR, "video", ".mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-vf", "scale='if(gt(iw,ih),-2,min(720,iw))':'if(gt(iw,ih),min(720,ih),-2)'",
         "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(dst)])
    d = duration(dst)
    cdir = candidates_dir(dst.stem)
    cdir.mkdir(parents=True, exist_ok=True)
    frames, best, best_s = [], None, -1
    for i, f in enumerate([0.06 + k * 0.08 for k in range(12)], start=1):
        frame = cdir / f"{i}.png"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{d * f:.2f}", "-i", str(dst), "-frames:v", "1", str(frame)])
        if frame.exists():
            img = Image.open(frame).convert("RGB")
            frames.append((i, img))
            s = score(img)
            if s > best_s:
                best, best_s = img, s
    poster = dst.with_suffix(".webp")
    best.save(poster, "WEBP", quality=80)
    candidate_sheet(dst.stem, frames)
    w, h = best.size
    return {"art": "video", "quelle": src.name, "datei": f"videos/{dst.name}", "vorschau": f"videos/{poster.name}",
            "breite": w, "hoehe": h, "sekunden": round(d, 1), "mb": round(dst.stat().st_size / 1e6, 1)}, best


def photo(src):
    if src.suffix.lower() in {".heic", ".heif"}:
        tmp = Path(tempfile.mkdtemp()) / "foto.png"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), str(tmp)])
        src_img = Image.open(tmp)
    else:
        src_img = Image.open(src)
    img = ImageOps.exif_transpose(src_img).convert("RGB")
    img.thumbnail((1600, 1600))
    dst = next_name(IMG_DIR, "foto", ".webp")
    img.save(dst, "WEBP", quality=80)
    return {"art": "foto", "quelle": src.name, "datei": f"bilder/{dst.name}",
            "breite": img.width, "hoehe": img.height, "mb": round(dst.stat().st_size / 1e6, 2)}, img


def candidate_sheet(name, frames):
    tw, th = 216, 384
    page = Image.new("RGB", (4 * tw, ((len(frames) + 3) // 4) * th), "#F6F2EA")
    draw = ImageDraw.Draw(page)
    for k, (i, img) in enumerate(frames):
        x, y = (k % 4) * tw, (k // 4) * th
        page.paste(ImageOps.fit(img, (tw - 8, th - 8)), (x + 4, y + 4))
        draw.rectangle((x + 4, y + 4, x + 44, y + 44), fill="#6E1020")
        draw.text((x + 18, y + 16), str(i), fill="#FFFFFF", font_size=22)
    page.save(OUT / f"kandidaten-{name}.jpg", quality=80)


def choose(name, number):
    src = candidates_dir(name) / f"{number}.png"
    if not src.exists():
        sys.exit(f"Kandidat {number} für {name} gibt es nicht.")
    Image.open(src).convert("RGB").save(VID_DIR / f"{name}.webp", "WEBP", quality=80)
    print(f"Vorschaubild für {name}: Kandidat {number}")


def download(url):
    target = OUT / "download" / str(abs(hash(url)))
    target.mkdir(parents=True, exist_ok=True)
    if "drive.google.com" in url:
        try:
            import gdown  # noqa: F401
        except ImportError:
            run([sys.executable, "-m", "pip", "install", "-q", "gdown"])
        if "/folders/" in url:
            run([sys.executable, "-m", "gdown", "--folder", "-q", "-O", str(target), url])
        else:
            run([sys.executable, "-m", "gdown", "--fuzzy", "-q", "-O", str(target) + "/", url])
    elif "dropbox.com" in url:
        url = url.replace("dl=0", "dl=1") if "dl=0" in url else url + ("&" if "?" in url else "?") + "dl=1"
        run(["curl", "-sSL", "--fail", "-o", str(target / "datei"), url])
        f = target / "datei"
        if f.read_bytes()[:4] == b"PK\x03\x04":  # Dropbox-Ordner kommen als ZIP
            import zipfile
            zipfile.ZipFile(f).extractall(target)
            f.unlink()
        else:
            kind = run(["file", "-b", "--mime-type", str(f)]).strip()
            ext = {"video/mp4": ".mp4", "video/quicktime": ".mov", "image/jpeg": ".jpg", "image/png": ".png",
                   "image/heic": ".heic", "image/webp": ".webp"}.get(kind, "")
            f.rename(f.with_suffix(ext))
    else:
        sys.exit(f"Nur Links von Google Drive oder Dropbox gehen: {url}")
    return target


def sheet(items):
    tw, th = 240, 360
    cols = 4
    rows = (len(items) + cols - 1) // cols
    page = Image.new("RGB", (cols * tw, rows * (th + 30)), "#F6F2EA")
    draw = ImageDraw.Draw(page)
    for i, (info, img) in enumerate(items):
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        page.paste(ImageOps.fit(img, (tw - 10, th - 10)), (x + 5, y + 5))
        draw.text((x + 8, y + th), Path(info["datei"]).name, fill="#6E1020")
    OUT.mkdir(parents=True, exist_ok=True)
    page.save(OUT / "uebersicht.jpg", quality=80)


def main(args):
    if args[0] == "--vorschau":
        return choose(args[1], args[2])
    OUT.mkdir(parents=True, exist_ok=True)
    files = []
    for a in args:
        try:
            p = download(a) if a.startswith("http") else Path(a)
        except subprocess.CalledProcessError:
            sys.exit(f"Download klappt nicht: {a}\nIst der Link auf „Jeder mit dem Link“ gestellt?")
        files += sorted(x for x in p.rglob("*") if x.is_file()) if p.is_dir() else [p]
    VID_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    done, skipped = [], []
    for f in files:
        ext = f.suffix.lower()
        try:
            if ext in VIDEO_EXT:
                done.append(video(f))
            elif ext in IMAGE_EXT:
                done.append(photo(f))
            else:
                skipped.append(f.name)
        except Exception as e:  # eine kaputte Datei soll nicht alles stoppen
            skipped.append(f"{f.name} ({e})")
    if done:
        sheet(done)
    print(json.dumps({"fertig": [d for d, _ in done], "uebersprungen": skipped,
                      "uebersicht": str(OUT / "uebersicht.jpg") if done else None,
                      "naechster_schritt": "Jede kandidaten-video-N.jpg ansehen und das schönste Bild wählen: "
                                           "python3 werkzeuge/medien.py --vorschau video-N NUMMER"},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
