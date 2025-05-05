import time
import cv2
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from image_utils import load_image, take_full_screenshot, highlight_match
from image_matcher import find_subimage_location

def main():
    # Setup Chrome in headless mode (or visible if you prefer)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to target page
        target_url = "https://infuse.it" 
        driver.get(target_url)

        time.sleep(2)  # Wait for page to load

        # Take full page screenshot
        full_img_path = os.path.join("images", "full_image.png")
        take_full_screenshot(driver, full_img_path)

        # Load images
        try:
            full_image = load_image(full_img_path)
            sub_image = load_image(os.path.join("images", "sub_image.png"))
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            return

        # Match image
        result = find_subimage_location(full_image, sub_image)
        print("Matching Result:", result)

        if result["result"] == "success":
            top_left = tuple(result["coordinates"]["top_left"])
            bottom_right = tuple(result["coordinates"]["bottom_right"])

            # Draw rectangle and save result image
            output_path = highlight_match(full_image, top_left, bottom_right)
            print(f"📸 Highlighted match saved to {output_path}")

            center_x = (top_left[0] + bottom_right[0]) // 2
            center_y = (top_left[1] + bottom_right[1]) // 2

            # Scroll to center_y position (to ensure visibility)
            driver.execute_script(f"window.scrollTo(0, {center_y - 300})")
            time.sleep(1)

            # Move to location and click
            actions = ActionChains(driver)
            actions.move_by_offset(center_x, center_y).click().perform()
            print(f"✅ Clicked on sub-image at center: ({center_x}, {center_y})")
        else:
            print("❌ Sub-image not found in full image.")

    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()