"""Extract the main artist picture for each of the 9 GenZ Bhajan nights from the deck."""
import pymupdf
from PIL import Image, ImageChops

PDF = "GenZ_Bhajan_Sponsorship_Deck_.pdf"

# (day, date, artist, image xref in the PDF)
EVENTS = [
    (1, "Oct 11", "Emayavaramban & Band", 126),  # phone screenshot, see PRE_CROP
    (2, "Oct 12", "Skanda Band", 137),
    (3, "Oct 13", "Varahi Band", 153),
    (4, "Oct 14", "Bridge Academy", 168),
    (5, "Oct 15", "Sarangi Band", 179),
    (6, "Oct 16", "Sai Vignesh & Band", 191),
    (7, "Oct 17", "Iskcon Band", 203),
    (8, "Oct 18", "Thisram Band", 217),
    (9, "Oct 19", "Sharanya Srinivas & Band", 223),
]

# Fixed crops applied before trimming, for images with extra chrome around the photo.
PRE_CROP = {126: (0, 211, 632, 1159)}  # drop status bar and nav bar

# Cut-outs on black whose heads reach the top edge: extra black above (as a fraction of
# the width) so the "Powered by" watermark in the top-left corner doesn't cover anyone.
HEADROOM = {153: 0.12, 168: 0.12, 217: 0.12}


def load(doc, xref):
    pix = pymupdf.Pixmap(doc, xref)
    if pix.colorspace and pix.colorspace.n != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    if img.mode == "RGBA":  # flatten cut-outs onto black, matching the deck
        bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
        bg.alpha_composite(img)
        img = bg
    return img.convert("RGB")


def trim_black(img, pad=24):
    """Crop away empty near-black borders, keeping a small margin."""
    diff = ImageChops.difference(img, Image.new("RGB", img.size, (0, 0, 0)))
    bbox = diff.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if not bbox:
        return img
    l, t, r, b = bbox
    return img.crop((max(l - pad, 0), max(t - pad, 0),
                     min(r + pad, img.width), min(b + pad, img.height)))


if __name__ == "__main__":
    doc = pymupdf.open(PDF)
    for day, date, artist, xref in EVENTS:
        img = load(doc, xref)
        if xref in PRE_CROP:
            img = img.crop(PRE_CROP[xref])
        img = trim_black(img)
        if xref in HEADROOM:
            extra = round(img.width * HEADROOM[xref])
            padded = Image.new("RGB", (img.width, img.height + extra), (0, 0, 0))
            padded.paste(img, (0, extra))
            img = padded
        out = f"events/event{day}.jpg"
        img.save(out, quality=90)
        print(f"Day {day} {date} {artist}: {out} {img.size}")
