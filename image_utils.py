import cv2
import numpy as np
import os
import time
import pytesseract

def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found at: {path}")
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Failed to load image: {path}")
    return image

def take_full_screenshot(driver, save_path):
    driver.save_screenshot(save_path)

def highlight_match(image, top_left, bottom_right, color=(0, 255, 0), thickness=2):
    image_copy = image.copy()
    cv2.rectangle(image_copy, top_left, bottom_right, color, thickness)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_filename = f"matched_output_{timestamp}.png"
    output_path = os.path.join("outputs", output_filename)
    cv2.imwrite(output_path, image_copy)
    return output_path

def extract_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text