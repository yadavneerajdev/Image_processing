from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from image_matcher import find_subimage_location
from image_utils import load_image, take_full_screenshot, highlight_match, extract_text_from_image
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.websocket("/ws/match")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            task = data.get("task", "match")

            url = data.get("url")
            sub_image_path = data.get("sub_image")

            if task == "match":
                if not url or not sub_image_path:
                    await websocket.send_json({
                        "result": "failure",
                        "error": "Missing 'url' or 'sub_image' in payload"
                    })
                    continue

                if not os.path.exists(sub_image_path):
                    await websocket.send_json({
                        "result": "failure",
                        "error": f"Sub image '{sub_image_path}' not found"
                    })
                    continue

                chrome_options = Options()
                chrome_options.add_argument("--start-maximized")
                driver = webdriver.Chrome(options=chrome_options)

                try:
                    driver.get(url)
                    time.sleep(2)

                    full_image_path = os.path.join("images", "full_image.png")
                    take_full_screenshot(driver, full_image_path)

                    full_image = load_image(full_image_path)
                    sub_image = load_image(sub_image_path)

                    result = find_subimage_location(full_image, sub_image)

                    if result["result"] == "success":
                        coords = result["coordinates"]
                        result["saved_path"] = highlight_match(full_image, tuple(coords["top_left"]), tuple(coords["bottom_right"]))

                    await websocket.send_json(result)

                except Exception as e:
                    await websocket.send_json({
                        "result": "failure",
                        "error": str(e)
                    })

                finally:
                    driver.quit()

            elif task == "extract_text":
                if not sub_image_path:
                    await websocket.send_json({
                        "result": "failure",
                        "error": "Missing 'sub_image' in payload"
                    })
                    continue

                if not os.path.exists(sub_image_path):
                    await websocket.send_json({
                        "result": "failure",
                        "error": f"Sub image '{sub_image_path}' not found"
                    })
                    continue

                try:
                    sub_image = load_image(sub_image_path)
                    extracted_text = extract_text_from_image(sub_image)
                    await websocket.send_json({
                        "result": "success",
                        "text": extracted_text
                    })
                except Exception as e:
                    await websocket.send_json({
                        "result": "failure",
                        "error": str(e)
                    })

            else:
                await websocket.send_json({
                    "result": "failure",
                    "error": f"Unknown task '{task}'"
                })
    except WebSocketDisconnect:
        print("WebSocket disconnected")