import argparse
from image_utils import load_image
from image_matcher import find_subimage_location
import cv2

def main():
    parser = argparse.ArgumentParser(description="Find if sub-image exists in full image.")
    parser.add_argument('--full', type=str, required=True, help='Path to full image')
    parser.add_argument('--sub', type=str, required=True, help='Path to sub-image')
    parser.add_argument('--threshold', type=float, default=0.95, help='Matching threshold (default: 0.95)')
    parser.add_argument('--show', action='store_true', help='Show matched result if found')

    args = parser.parse_args()

    full_image = load_image(args.full)
    sub_image = load_image(args.sub)

    found_result = find_subimage_location(full_image, sub_image, args.threshold)

    if found_result["result"] == "success":
        top_left = tuple(found_result["coordinates"]["top_left"])
        bottom_right = tuple(found_result["coordinates"]["bottom_right"])
        score = found_result["confidence"]
        print(f"✅ Sub-image found at {top_left} with score {score:.4f}")
        if args.show:
            cv2.rectangle(full_image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.imshow("Match", full_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        score = found_result["confidence"]
        print(f"❌ Sub-image not found. Best match score: {score:.4f}")

if __name__ == "__main__":
    main()