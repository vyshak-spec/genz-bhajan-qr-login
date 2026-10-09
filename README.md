# GenZ Bhajan – Event QR Codes

Nine QR codes, one per night of GenZ Bhajan (Oct 11–19, 2026, Guru Nanak College, Velachery).
Scanning a code opens a page with the VVIP Pass followed by that night's artist picture and details.

Pages are served from `docs/` via GitHub Pages on the custom domain `events.iqtechmax.com`
(DNS: CNAME `events` → `vyshak-spec.github.io`). Old links `/1/` … `/9/` redirect to the new ones.

| Day | Date | Artist | QR link |
|---|---|---|---|
| 1 | Oct 11 | Emayavaramban & Band | https://events.iqtechmax.com/genz-bhajan/day1/Emayavaramban-Band |
| 2 | Oct 12 | Skanda Band | https://events.iqtechmax.com/genz-bhajan/day2/Skanda-Band |
| 3 | Oct 13 | Varahi Band | https://events.iqtechmax.com/genz-bhajan/day3/Varahi-Band |
| 4 | Oct 14 | Bridge Academy | https://events.iqtechmax.com/genz-bhajan/day4/Bridge-Academy |
| 5 | Oct 15 | Sarangi Band | https://events.iqtechmax.com/genz-bhajan/day5/Sarangi-Band |
| 6 | Oct 16 | Sai Vignesh & Band | https://events.iqtechmax.com/genz-bhajan/day6/Sai-Vignesh-Band |
| 7 | Oct 17 | Iskcon Band | https://events.iqtechmax.com/genz-bhajan/day7/Iskcon-Band |
| 8 | Oct 18 | Thisram Band | https://events.iqtechmax.com/genz-bhajan/day8/Thisram-Band |
| 9 | Oct 19 | Sharanya Srinivas & Band | https://events.iqtechmax.com/genz-bhajan/day9/Sharanya-Srinivas-Band |

## Layout

- `qr/` – the 9 printable QR images (`qr_day1.png` … `qr_day9.png`)
- `events/` – artist pictures cropped from the sponsorship deck
- `vvip_pass.jpg` – VVIP Pass shown first on every page
- `docs/` – the published site (generated)
- `extract_events.py` – crops the artist pictures out of `GenZ_Bhajan_Sponsorship_Deck_.pdf` (not committed; place it in the project root)
- `make_qr.py` – builds `docs/` and the QR images (`BASE_URL` sets the link)
- `verify_qr.py` – scans each QR and checks the live page shows the right day, artist and picture

## Rebuild

```sh
pip install -r requirements.txt
python extract_events.py   # only if the deck or picture choices change
python make_qr.py
git add . && git commit -m "Update event pages" && git push
python verify_qr.py        # after GitHub Pages redeploys
# before the custom domain is live:
python verify_qr.py https://vyshak-spec.github.io/genz-bhajan-qr-login/
```
