# GenZ Bhajan – Event QR Codes

Nine QR codes, one per night of GenZ Bhajan (Oct 11–19, 2026, Guru Nanak College, Velachery).
Scanning a code opens a page with the VVIP Pass followed by that night's artist picture and details.

The site is the static `docs/` folder, served at `https://events.iqtechmax.com/`.
Old links `/1/` … `/9/` redirect to the new ones.

## How updates work

1. Edit the content (pictures in `events/`, `vvip_pass.jpg`, or the page template in `make_qr.py`),
   then run `python make_qr.py` to rebuild `docs/`.
2. Commit and push to `main`.
3. GitHub Actions checks that all 9 printed QR links still exist, then updates the server
   automatically (usually under a minute). Progress is on the repo's **Actions** tab.

**The QR codes are printed. Never rename or move these 9 folders in `docs/`:**

```
genz-bhajan/day1/Emayavaramban-Band     genz-bhajan/day6/Sai-Vignesh-Band
genz-bhajan/day2/Skanda-Band            genz-bhajan/day7/Iskcon-Band
genz-bhajan/day3/Varahi-Band            genz-bhajan/day8/Thisram-Band
genz-bhajan/day4/Bridge-Academy         genz-bhajan/day9/Sharanya-Srinivas-Band
genz-bhajan/day5/Sarangi-Band
```

If one must move, keep the old folder with an `index.html` that redirects to the new place
(see `docs/1/index.html` for an example). A push that removes any of them fails the check and is
not deployed (`scripts/check_qr_links.py`).

## Server setup (one time, Nginx)

```sh
cd /var/www
git clone https://github.com/vyshak-spec/genz-bhajan-qr-login.git
```

```nginx
server {
    listen 80;
    server_name events.iqtechmax.com;
    root /var/www/genz-bhajan-qr-login/docs;
    index index.html;
    location / { try_files $uri $uri/ =404; }
}
```

DNS: `A` record `events` → server IP. HTTPS: `sudo certbot --nginx -d events.iqtechmax.com`.
Auto-deploy (`.github/workflows/deploy.yml`) needs the repo secrets `DEPLOY_HOST`, `DEPLOY_USER`
and `DEPLOY_SSH_KEY`.

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
- `scripts/check_qr_links.py` – fails if any of the 9 printed QR paths is missing (`--live URL` checks the site)
- `.github/workflows/deploy.yml` – on every push to `main`: QR link check → deploy to server → live check

## Rebuild

```sh
pip install -r requirements.txt
python extract_events.py   # only if the deck or picture choices change
python make_qr.py
python scripts/check_qr_links.py   # same check the deploy runs
git add . && git commit -m "Update event pages" && git push
python verify_qr.py        # after the deploy finishes
```
