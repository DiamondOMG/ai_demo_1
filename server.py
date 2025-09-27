# server.py
import http.server
import socketserver
import webbrowser
import os
import json
import threading
import queue
import asyncio
import websockets
from wake_word import start_listening
from ai_stream import process_ai_response

PORT = 8000
WS_PORT = 8001

# ---------------------------
# Queue สำหรับสื่อสารกับ main thread
wakeword_queue = queue.Queue()
ws_to_main_queue = queue.Queue()
# ---------------------------

# เก็บ client WebSocket
ws_clients = set()
ws_clients_lock = threading.Lock()

# ---------------------------
# Wake word thread
def wakeword_thread():
    start_listening(wakeword_queue)

# ---------------------------
# WebSocket thread
async def ws_handler(websocket):
    with ws_clients_lock:
        ws_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # ส่งข้อความ STT ไป main thread
            ws_to_main_queue.put((data, websocket))
    finally:
        with ws_clients_lock:
            ws_clients.remove(websocket)

def websocket_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def ws_main():
        async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
            await asyncio.Future()  # run forever
    loop.run_until_complete(ws_main())

# ---------------------------
# Main thread loop (blocking)
def main_loop():
    while True:
        # 1. ตรวจ wake word
        try:
            event = wakeword_queue.get(timeout=0.1)
            if event == "detected":
                # ส่งไป WebSocket ทุก client
                with ws_clients_lock:
                    for ws in ws_clients:
                        asyncio.run(ws.send(json.dumps({"type": "wakeword", "status": "detected"})))
        except queue.Empty:
            pass

        # 2. ตรวจข้อความจาก WebSocket
        try:
            (data, websocket) = ws_to_main_queue.get_nowait()
            if data.get("type") == "stt":
                ai_response = process_ai_response(data["message"])
                # ส่งผล AI กลับ client เดียวกัน
                asyncio.run(websocket.send(json.dumps({"type": "output", "message": ai_response})))
        except queue.Empty:
            pass

# ---------------------------
# HTTP server
class StaticHandler(http.server.SimpleHTTPRequestHandler):
    pass

# ---------------------------
if __name__ == "__main__":
    # เริ่ม threads
    threading.Thread(target=wakeword_thread, daemon=True).start()
    threading.Thread(target=websocket_thread, daemon=True).start()

    # เริ่ม main loop ใน thread หลัก
    threading.Thread(target=main_loop, daemon=True).start()

    # Serve static files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        with socketserver.TCPServer(("", PORT), StaticHandler) as httpd:
            print(f"Serving at port {PORT}")
            print(f"WebSocket running on port {WS_PORT}")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        os._exit(0)   # kill ทุก thread ทันที
