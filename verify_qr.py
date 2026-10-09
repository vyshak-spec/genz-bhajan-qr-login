"""Scan each QR image, fetch the live page, and check its day, artist and picture.

Usage: python verify_qr.py [SITE_ROOT]
SITE_ROOT replaces the domain in the scanned link, e.g.
https://vyshak-spec.github.io/genz-bhajan-qr-login/ to test before the custom domain is live.
"""
import hashlib
import re
import sys
import urllib.parse
import urllib.request

import cv2

from extract_events import EVENTS
from make_qr import BASE_URL, event_path


def fetch(url):
    return urllib.request.urlopen(url, timeout=20).read()


if __name__ == "__main__":
    detector = cv2.QRCodeDetector()
    domain = BASE_URL.split("/genz-bhajan/")[0] + "/"
    site_root = sys.argv[1] if len(sys.argv) > 1 else domain
    failed = 0
    for day, date, artist, _ in EVENTS:
        img = cv2.resize(cv2.imread(f"qr/qr_day{day}.png"), None, fx=0.25, fy=0.25)
        scanned, _, _ = detector.detectAndDecode(img)
        url = scanned.replace(domain, site_root, 1)
        page = urllib.request.urlopen(url, timeout=20)  # follows the trailing-slash redirect
        html, url = page.read().decode(), page.geturl()
        badge = re.search(r'class="day">([^<]*)', html).group(1).replace("&middot;", "·")
        name = re.search(r"<h1>([^<]*)", html).group(1).replace("&amp;", "&")
        srcs = re.findall(r'<img src="([^"]*)"', html)
        event_src = urllib.parse.urljoin(url, srcs[-1])
        same_pic = (hashlib.md5(fetch(event_src)).digest()
                    == hashlib.md5(open(f"events/event{day}.jpg", "rb").read()).digest())
        ok = (scanned == BASE_URL + event_path(day, artist)
              and badge == f"DAY {day} · {date.upper()}" and name == artist and same_pic
              and srcs[0].endswith("vvip_pass.jpg"))
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  qr_day{day}.png -> {scanned}  ({badge}, {name})")
    print("All 9 pass." if not failed else f"{failed} failed.")
