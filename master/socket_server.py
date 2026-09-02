import sys
import socket

HOST = "0.0.0.0"   # IMPORTANT: allow other machines
PORT = 9999

conn = None

def start_socket_server():
    global conn

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Explicitly printing before binding to see what values are actually here
        print(f"DEBUG: Attempting to bind socket to {HOST}:{PORT}")
        server_socket.bind((HOST, PORT))
    except OSError as e:
        print(f"❌ CRITICAL: Failed to bind socket to {HOST}:{PORT}. Error: {e}")
        # Prevent the whole FastAPI app from hanging or behaving weirdly
        return 

    server_socket.listen(5)
    print(f"🔥 Socket server listening on {HOST}:{PORT}")

    while True:
        try:
            new_conn, addr = server_socket.accept()
            conn = new_conn
            print(f"✅ Spark connected from {addr}")
        except Exception as e:
            print("Accept error:", e)


def send_to_spark(message: str):
    global conn

    if conn is None:
        return  # no connection yet, just skip

    try:
        conn.sendall((message + "\n").encode("utf-8"))
    except Exception:
        print("⚠️ Spark disconnected")
        conn = None
