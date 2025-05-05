import cv2
import numpy as np

def find_subimage_location(full_image, sub_image, threshold=0.95):
    result = cv2.matchTemplate(full_image, sub_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w = sub_image.shape[:2]
        return {
            "result": "success",
            "confidence": float(max_val),
            "coordinates": {
                "top_left": list(max_loc),
                "bottom_right": [max_loc[0] + w, max_loc[1] + h]
            }
        }
    else:
        return {
            "result": "failure",
            "confidence": float(max_val),
            "coordinates": None
        }