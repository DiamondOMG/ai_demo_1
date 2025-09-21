import http.server
import socketserver
import webbrowser
import os
import json
import threading
import wake_word
from ai_stream import process_ai_response  # Import ฟังก์ชันจาก ai_stream

PORT = 8000

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
    # รัน wake word ใน thread แยก
    threading.Thread(target=wake_word.start_listening, daemon=True).start()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        webbrowser.open(f"http://localhost:{PORT}/index.html")
        httpd.serve_forever()