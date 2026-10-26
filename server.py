import http.server
import ssl
import socket
import sys

# Force UTF-8 encoding for standard output if needed
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

PORT = 8443

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

local_ip = get_local_ip()

Handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(('0.0.0.0', PORT), Handler)

# Wrap with SSL (Required for DeviceMotion / Sensors on mobile browsers)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("=" * 60)
print("Motion Detector HTTPS Server Running!")
print(f"Open this URL on your Android phone's browser:")
print(f"   https://{local_ip}:{PORT}")
print("=" * 60)
print("Note: Because this uses a self-signed certificate, your browser")
print("will show a warning ('Your connection is not private').")
print("Tap 'Advanced' -> 'Proceed to ... (unsafe)' to open the page.")
print("Press Ctrl+C to stop the server.")
print("=" * 60)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
