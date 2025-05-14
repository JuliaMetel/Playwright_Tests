import io
import time
from PIL import Image, ImageChops
from exeption import TextIsDifferent
from playwright.sync_api import Locator


def is_images_equal(img1, img2):
    image_1 = img1.convert('RGB')
    image_2 = img2.convert('RGB')
    result = ImageChops.difference(image_1, image_2).getbbox()
    if result is None:
        return True
    return False

def wait_page_stable(page):
    image_1 = Image.open(io.BytesIO(page.screenshot()))
    for x in range(100):
        image_2 = Image.open(io.BytesIO(page.screenshot()))
        if is_images_equal(image_1, image_2):
            break
        time.sleep(0.1)
        image_1 = image_2

def is_elements_screenshots_equal(link: str, element: Locator, name: str) -> bool:
    image_1 = Image.open(io.BytesIO(element.screenshot()))
    if is_images_equal(image_1, Image.open(link)):
        return True
    image_1.save(f'{name}.png')
    return False

def is_text_equal(text1, text2):
    return text1 == text2


def check_text_equal(text1, text2):
    if not (is_text_equal(text1, text2)):
        raise TextIsDifferent('The text on the page is different than expected')


def check_text_not_equal(text1, text2):
    if is_text_equal(text1, text2):
        raise TextIsDifferent('The text on the page is as expected')