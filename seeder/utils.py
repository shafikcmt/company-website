import io
import logging
import textwrap

import requests
from django.core.files.images import ImageFile
from PIL import Image, ImageDraw, ImageFont


logger = logging.getLogger(__name__)


# Raw bytes per cache key; every call returns a fresh file object so the same
# image can be saved many times (a shared file object would be read to EOF).
IMAGE_CACHE = {}

NAVY = (9, 62, 97)
NAVY_LIGHT = (14, 74, 117)
NAVY_DARK = (6, 41, 63)
AMBER = (245, 158, 11)


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


def placeholder_image(width, height, label=None, style="photo"):
    """Generate a branded placeholder locally (used when picsum is unreachable).

    style="photo" draws a navy gradient with a subtle grid and the label;
    style="logo" draws a white tile with the label as a navy wordmark.
    """
    # The bundled bitmap font only covers Latin-1.
    if label:
        label = label.replace("—", "-").replace("–", "-").replace("®", "").replace("ø", "o")

    if style == "logo":
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        text = (label or "Logo").upper()
        size = max(14, int(height * 0.22))
        font = _font(size)
        while draw.textlength(text, font=font) > width * 0.85 and size > 10:
            size -= 2
            font = _font(size)
        w = draw.textlength(text, font=font)
        draw.text(((width - w) / 2, (height - size) / 2), text, fill=NAVY, font=font)
        draw.rectangle([(width - w) / 2, (height + size) / 2 + 6, (width + w) / 2, (height + size) / 2 + 9], fill=AMBER)
        return img

    img = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(int(NAVY_LIGHT[i] * (1 - t) + NAVY_DARK[i] * t) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    step = max(24, width // 24)
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 0), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(16, 80, 125), width=1)
    draw.rectangle([0, height - max(6, height // 60), width, height], fill=AMBER)
    if label:
        size = max(16, width // 22)
        font = _font(size)
        lines = textwrap.wrap(label, width=max(12, int(width / (size * 0.6))))[:3]
        y = (height - len(lines) * (size + 8)) / 2
        for line in lines:
            w = draw.textlength(line, font=font)
            draw.text(((width - w) / 2, y), line, fill=(255, 255, 255), font=font)
            y += size + 8
    return img


def _to_bytes(img):
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


def cache_image(width, height, keyword=None, label=None, style="photo"):
    """Return an ImageFile for seeding.

    Tries Picsum Photos first (random stock photo); if the network is
    unavailable it falls back to a locally generated placeholder.
    `style="logo"` always generates a local wordmark tile (no stock photo).
    """
    cache_key = f"{width}x{height}-{keyword}-{label}-{style}"
    data = IMAGE_CACHE.get(cache_key)

    if data is None and style != "logo":
        url = f"https://picsum.photos/{width}/{height}"
        if keyword:
            url += f"?random={keyword}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.content
        except requests.exceptions.RequestException as e:
            logger.warning("Picsum unavailable (%s); using a generated placeholder.", e.__class__.__name__)

    if data is None:
        data = _to_bytes(placeholder_image(width, height, label or keyword, style=style))

    IMAGE_CACHE[cache_key] = data
    safe = "".join(ch if ch.isalnum() else "-" for ch in (label or keyword or "image")).strip("-").lower()
    return ImageFile(io.BytesIO(data), name=f"{safe[:40] or 'image'}-{width}x{height}.jpg")
