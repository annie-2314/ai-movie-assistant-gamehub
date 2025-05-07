# utils/image_utils.py
from PIL import Image, ImageFilter
import requests
from io import BytesIO

def blur_image(image_url, blur_radius=10):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        return blurred_img
    return None
