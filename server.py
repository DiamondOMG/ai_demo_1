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
from ai_stream import process_ai_response

PORT = 8000
WS_PORT = 8001

wakeword_queue = queue.Queue()
ws_clients = set()
ws_clients_lock = threading.Lock()

def wakeword_listener():
    while True:
        event = wakeword_queue.get()
        if event == "detected":
            asyncio.run(send_ws_event("detected"))

async def ws_handler(websocket):
    with ws_clients_lock:
        ws_clients.add(websocket)
    try:
        async for message in websocket:
            # รับข้อความ STT จาก browser
            data = json.loads(message)
            if data.get("type") == "stt":
                print(f"[Browser STT] {data['message']}")
                # ส่งไปประมวลผล AI
                threading.Thread(
                    target=process_ai_response,
                    args=(data["message"],),
                    daemon=True
                ).start()
    finally:
        with ws_clients_lock:
            ws_clients.remove(websocket)

async def send_ws_event(event):
    if ws_clients:
        await asyncio.gather(
            *(ws.send(json.dumps({"type": "wakeword", "status": event})) 
            for ws in ws_clients)
        )

def start_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def ws_main():
        async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
            await asyncio.Future()
    loop.run_until_complete(ws_main())

class StaticHandler(http.server.SimpleHTTPRequestHandler):
    # เหลือแค่ serve static files
    pass

if __name__ == "__main__":
    threading.Thread(target=wake_word.start_listening, args=(wakeword_queue,), daemon=True).start()
    threading.Thread(target=wakeword_listener, daemon=True).start()
    threading.Thread(target=start_ws_server, daemon=True).start()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        with socketserver.TCPServer(("", PORT), StaticHandler) as httpd:
            print(f"Serving at port {PORT}")
            print(f"WebSocket running on port {WS_PORT}")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")