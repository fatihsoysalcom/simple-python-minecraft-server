import socket
import threading

# Basic Minecraft server implementation using Python
# This is a highly simplified example for demonstration purposes.
# A real Minecraft server is significantly more complex.

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 25565      # Default Minecraft server port

# In a real server, this would be a list of connected players and their states.
# For this example, we'll just track connections.
clients = []

def handle_client(conn, addr):
    """Handles a single client connection."""
    print(f"[+] New connection from {addr}")
    clients.append(conn)

    try:
        while True:
            # In a real server, this would parse Minecraft protocol packets.
            # Here, we'll just echo back any received data.
            data = conn.recv(1024)
            if not data:
                break
            print(f"[*] Received from {addr}: {data.decode()}")

            # Simulate a simple server response (e.g., a chat message)
            response = b"Hello from your Python MC server!\n"
            conn.sendall(response)

    except ConnectionResetError:
        print(f"[-] Connection from {addr} reset.")
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        print(f"[-] Connection from {addr} closed.")
        clients.remove(conn)
        conn.close()

def start_server():
    """Starts the main server loop."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 queued connections
    print(f"[*] Listening on {HOST}:{PORT}")

    try:
        while True:
            # Accept new connections
            conn, addr = server_socket.accept()
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("[*] Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
