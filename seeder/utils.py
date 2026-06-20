import io
import logging
import requests
from django.core.files.images import ImageFile


logger = logging.getLogger(__name__)


IMAGE_CACHE = {}


def cache_image(width, height, keyword=None):
    """Downloads and caches images from Picsum Photos."""
    cache_key = f"{width}x{height}-{keyword}" if keyword else f"{width}x{height}"
    if cache_key in IMAGE_CACHE:
        return IMAGE_CACHE[cache_key]

    url = f"https://picsum.photos/{width}/{height}"
    if keyword:
        url += f"?random={keyword}"

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error downloading image: {e}")
        return None

    image_data = io.BytesIO(response.content)
    image_file = ImageFile(image_data, name=f"{cache_key}.jpg")

    IMAGE_CACHE[cache_key] = image_file
    return image_file
