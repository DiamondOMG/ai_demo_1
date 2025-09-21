import http.server
import socketserver
import webbrowser
import os
import json
import threading
import queue
import asyncio
import websockets
import wake_word
from ai_stream import process_ai_response  # Import ฟังก์ชันจาก ai_stream

PORT = 8000
WS_PORT = 8001

wakeword_queue = queue.Queue()
ws_clients = set()

def wakeword_listener():
    while True:
        event = wakeword_queue.get()
        if event == "detected":
            # ส่ง event ไปยังทุก websocket client
            asyncio.run(send_ws_event("detected"))

async def ws_handler(websocket):
    ws_clients.add(websocket)
    try:
        async for _ in websocket:
            pass  # ไม่รับข้อความจาก client
    finally:
        ws_clients.remove(websocket)

async def send_ws_event(event):
    if ws_clients:
        await asyncio.gather(*(ws.send(event) for ws in ws_clients))

def start_ws_server():
    async def ws_main():
        async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
            await asyncio.Future()  # run forever
    asyncio.run(ws_main())

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/log":
            length = int(self.headers["Content-Length"])
            data = self.rfile.read(length)
            text = json.loads(data.decode("utf-8"))["message"]

            print(f"[Browser STT] {text}")  # แสดง text ที่รับมา

            # ส่ง text ไปให้ ai_stream โดยไม่รอผลลัพธ์
            threading.Thread(target=process_ai_response, args=(text,), daemon=True).start()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_error(404)

if __name__ == "__main__":
    threading.Thread(target=wake_word.start_listening, args=(wakeword_queue,), daemon=True).start()
    threading.Thread(target=wakeword_listener, daemon=True).start()
    threading.Thread(target=start_ws_server, daemon=True).start()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
            print(f"Serving at port {PORT}")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")