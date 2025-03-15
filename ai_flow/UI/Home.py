import pysrt
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio
import random
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json

from ai_flow.CombineFlow.TranslateAudio import generate_translated_audio, generate_translated_srt
from ai_flow.Text2Voice.EdgeTTS_srt import process_subtitles, notify_other_function
from ai_flow.VideoFetch.video_fetch import download

app = FastAPI()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# Handle POST requests to process URL
@app.post("/process_url")
async def process_url(request: Request):
    data = await request.json()
    url = data.get("url")
    # Process the URL as needed
    # For example, download a video from the URL
    key = str(hash(url))
    print(f"download URL: {url}")
    await asyncio.to_thread(download, url, "file", key)

    await asyncio.create_task(
        generate_translated_srt("file/" + key + ".mp3", "file/srt_output.srt", "file/translated_audio.mp3"))

    # and extract the audio
    # translated_srt_output_path = "../CombineFlow/translated_output.srt"
    # await process_subtitles(pysrt.open(translated_srt_output_path))
    # asyncio.create_task(process_subtitles(pysrt.open(translated_srt_output_path)))
    return JSONResponse(content={"message": f"URL received: {url}"})

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)  # Simulate a delay between updates
        random_data = random.randint(1, 100)  # Generate random data
        await websocket.send_text(f"Real-time update: {random_data}")  # Send data to client

# WebSocket endpoint for progress updates
@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    await websocket.accept()
    try:
        data = 0
        while True:
            await asyncio.sleep(1)  # Simulate a delay between updates
            data = notify_other_function()
            print(f"Progress: {data}%")
            await websocket.send_text(json.dumps({"progress": data}))  # Send progress data to client
    except Exception as e:
        print(f"WebSocket error: {e}")
    # finally:
    #     await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
