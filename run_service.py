import http.server
import socketserver
import webbrowser
import os

# กำหนด port
PORT = 8000

# ตั้งค่า directory ที่มี index.html
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# สร้าง handler สำหรับ web server
Handler = http.server.SimpleHTTPRequestHandler

# สร้าง server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    # เปิด browser อัตโนมัติ
    webbrowser.open(f"http://localhost:{PORT}")
    # รัน server
    httpd.serve_forever()