# 🛰️ FastAPI WebSocket Server

This project is a FastAPI-based WebSocket server that allows real-time client communication to perform tasks such as matching images or extracting text using provided JSON-based commands.

---

## 📁 Project Setup

Follow the steps below to get the server running locally.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <project-root-directory>
```

2. Create a Virtual Environment

```bash
python -m venv venv
```

## Activate the environment:

`macOS/Linux`

```bash
source venv/bin/activate
```

`Windows`

```bash
venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

⸻

🚀 Running the Server

To start the WebSocket server, run:

```bash
uvicorn ws_server:app --reload --host 0.0.0.0 --port 8000
```

The WebSocket server will be available at:

`ws://localhost:8000/ws/match`

⸻

🔌 WebSocket Usage

Connect to the server using a WebSocket client such as:
• JavaScript WebSocket object
• Postman
• websocat
• Any browser extension for WebSocket testing

🔗 Connection URL

ws://localhost:8000/ws/match

🧠 Example JavaScript Client

const ws = new WebSocket("ws://localhost:8000/ws/match");

ws.onopen = () => {
console.log("Connected");
ws.send(JSON.stringify({
url: "https://www.saucedemo.com/v1/",
sub_image: "images/sauce_login.png"
}));
};

ws.onmessage = (event) => {
console.log("Response from server:", event.data);
};

⸻

🧪 Supported Commands

Send JSON objects with the following structure:

1. 🔍 Match Image from URL

```bash
{
  "url": "https://www.saucedemo.com/v1/",
  "sub_image": "images/sauce_login.png"
}
```

url: Full-page screenshot URL or web address.
sub_image: Relative path to the image that should be matched on the page.

2. 📝 Extract Text from Image

```bash
{
  "task": "extract_text",
  "sub_image": "images/sub_image.png"
}
```

Task: Must be "extract_text" to trigger OCR/text extraction.
sub_image: Path to the image containing text to extract.

⸻

📄 Requirements

Make sure the `images/` and `output` (empty) folder exists and `images` folder contains the images referenced in the requests.

⸻

🧾 License

This project is provided under the MIT License. You’re free to use and modify it as needed.
