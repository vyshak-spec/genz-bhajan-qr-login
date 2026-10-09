"""Build the 9 event pages and their QR code images."""
import os
import shutil

import qrcode
from PIL import Image, ImageDraw, ImageFont

from extract_events import EVENTS

BASE_URL = "https://events.iqtechmax.com/genz-bhajan/"
SITE = "docs"
EVENT_DIR = f"{SITE}/genz-bhajan"
QR_DIR = "qr"
FONT = "C:/Windows/Fonts/arialbd.ttf"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Day {day} - {artist} | GenZ Bhajan</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
         justify-content: center; gap: 20px; padding: 16px; background: radial-gradient(circle at 50% 0%, #2a0f22 0%, #0b0b0f 60%);
         color: #f7f2ea; font-family: "Outfit", system-ui, sans-serif; }}
  figure {{ margin: 0; width: min(100%, 480px); border-radius: 20px; overflow: hidden;
           background: #111015; box-shadow: 0 24px 60px rgba(0, 0, 0, .6); }}
  .pass img {{ display: block; width: 100%; height: auto; }}
  .photo {{ position: relative; }}
  .photo > img {{ display: block; width: 100%; height: auto; }}
  /* soft shade behind the watermark so it reads on bright photos */
  .photo::before {{ content: ""; position: absolute; inset: 0; pointer-events: none;
                   background: radial-gradient(ellipse at 0 0, rgba(0, 0, 0, .45), rgba(0, 0, 0, 0) 42%); }}
  .powered {{ position: absolute; top: 12px; left: 14px; width: clamp(80px, 24%, 118px); opacity: .88;
             pointer-events: none; filter: drop-shadow(0 1px 2px rgba(0, 0, 0, .5)); }}
  .powered span {{ display: block; margin-bottom: 4px; font-size: 8px; font-weight: 600; letter-spacing: .24em;
                  color: #fff; }}
  .powered img {{ display: block; width: 100%; height: auto; }}
  .photo::after {{ content: ""; position: absolute; inset: auto 0 0 0; height: 30%;
                  background: linear-gradient(to bottom, rgba(17, 16, 21, 0), #111015); }}
  figcaption {{ position: relative; margin-top: -36px; padding: 0 22px 22px; }}
  .wide .photo::after {{ display: none; }}
  .wide figcaption {{ margin-top: 0; padding-top: 18px; }}
  .day {{ display: inline-block; padding: 6px 12px; border-radius: 999px; font-size: 12px; font-weight: 600;
         letter-spacing: .18em; background: linear-gradient(90deg, #ff2e7e, #ff8a3d); color: #fff; }}
  h1 {{ margin: 12px 0 6px; font-size: clamp(26px, 7vw, 38px); font-weight: 800; line-height: 1.05;
       letter-spacing: -.02em; }}
  .info {{ margin: 0; font-size: 15px; font-weight: 300; color: #d8cfc2; }}
  .brand {{ margin: 14px 0 0; font-size: 12px; font-weight: 400; letter-spacing: .14em;
           text-transform: uppercase; color: #8d8579; }}
</style>
</head>
<body>
<figure class="pass">
  <img src="../../img/vvip_pass.jpg" alt="GenZ Bhajan VVIP Pass">
</figure>
<figure class="{shape}">
  <div class="photo">
    <img src="../../img/event{day}.jpg" alt="{artist}">
    <div class="powered"><span>POWERED BY</span><img src="../../img/iqtechmax_white.png" alt="IQ Techmax"></div>
  </div>
  <figcaption>
    <span class="day">DAY {day} &middot; {date_upper}</span>
    <h1>{artist}</h1>
    <p class="info">6 &ndash; 8 PM &middot; Guru Nanak College, Velachery</p>
    <p class="brand">GenZ Bhajan &middot; High On Events</p>
  </figcaption>
</figure>
</body>
</html>
"""

# Earlier links (/1/ ... /9/) forward to the new pages so nothing already shared breaks.
REDIRECT = """<!doctype html>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=../genz-bhajan/{path}/">
<link rel="canonical" href="{url}">
<a href="../genz-bhajan/{path}/">Continue to Day {day}</a>
"""


def slug(artist):
    """'Sai Vignesh & Band' -> 'Sai-Vignesh-Band'."""
    return "-".join(artist.replace("&", " ").split())


def event_path(day, artist):
    return f"day{day}/{slug(artist)}"


def build_watermark(out):
    """White, transparent, side-by-side version of iqtechmax_logo.png (icon left of the wordmark)."""
    logo = Image.open("iqtechmax_logo.png").convert("L")
    icon, word = logo.crop((98, 134, 235, 382)), logo.crop((44, 413, 301, 459))
    icon = icon.resize((round(icon.width * 96 / icon.height), 96), Image.LANCZOS)
    gap = 18
    shade = Image.new("L", (icon.width + gap + word.width, icon.height), 255)
    shade.paste(icon, (0, 0))
    shade.paste(word, (icon.width + gap, (icon.height - word.height) // 2))
    # dark ink -> opaque white, white paper -> transparent
    alpha = shade.point(lambda v: min(255, round((255 - v) * 1.25)))
    mark = Image.new("RGBA", shade.size, (255, 255, 255, 0))
    mark.putalpha(alpha)
    mark.save(out)


def build_site():
    shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(f"{EVENT_DIR}/img")
    shutil.copy("vvip_pass.jpg", f"{EVENT_DIR}/img/vvip_pass.jpg")
    build_watermark(f"{EVENT_DIR}/img/iqtechmax_white.png")
    for day, date, artist, _ in EVENTS:
        path = event_path(day, artist)
        shutil.copy(f"events/event{day}.jpg", f"{EVENT_DIR}/img/event{day}.jpg")
        # A folder with index.html, so any web server answers the extension-less URL.
        os.makedirs(f"{EVENT_DIR}/{path}")
        with open(f"{EVENT_DIR}/{path}/index.html", "w", encoding="utf-8") as f:
            w, h = Image.open(f"events/event{day}.jpg").size
            f.write(PAGE.format(day=day, date_upper=date.upper(), artist=artist,
                                shape="wide" if w / h > 1.8 else "tall"))
        os.makedirs(f"{SITE}/{day}")
        with open(f"{SITE}/{day}/index.html", "w", encoding="utf-8") as f:
            f.write(REDIRECT.format(day=day, path=path, url=BASE_URL + path))


def build_qr():
    os.makedirs(QR_DIR, exist_ok=True)
    big, small = ImageFont.truetype(FONT, 44), ImageFont.truetype(FONT, 30)
    for day, date, artist, _ in EVENTS:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=4)
        url = BASE_URL + event_path(day, artist)
        qr.add_data(url)
        code = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        card = Image.new("RGB", (code.width, code.height + 130), "white")
        card.paste(code, (0, 0))
        draw = ImageDraw.Draw(card)
        cx = code.width // 2
        draw.text((cx, code.height + 10), f"DAY {day}  |  {date}", font=big, fill="black", anchor="mt")
        draw.text((cx, code.height + 70), artist, font=small, fill="#444444", anchor="mt")
        card.save(f"{QR_DIR}/qr_day{day}.png")
        print(f"qr/qr_day{day}.png -> {url}")


if __name__ == "__main__":
    if not BASE_URL:
        raise SystemExit("Set BASE_URL in make_qr.py first.")
    build_site()
    build_qr()
