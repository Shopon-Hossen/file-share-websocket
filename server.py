import socket
from tqdm import tqdm
import os


def print_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # The IP doesn't need to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    print(f"Local IP: {ip}")


def get_unique_filename(directory, filename):
    """Ensure the file doesn't overwrite an existing one by adding a number if needed."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1
    return new_filename


def start_server(host='0.0.0.0', port=5001):
    print_local_ip()

    # Use current directory with a subfolder "Received"
    output_dir = os.path.join(os.getcwd(), "Received")
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Files will be saved in: {output_dir}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Receive the file name (padded to 1024 bytes)
        filename = conn.recv(1024).decode().strip()
        if not filename:
            print("No filename received. Skipping transfer.")
            conn.close()
            continue

        # Ensure the filename doesn't overwrite an existing file
        filename = get_unique_filename(output_dir, filename)
        save_path = os.path.join(output_dir, filename)

        with open(save_path, 'wb') as f:
            with tqdm(unit='B', unit_scale=True, desc=f"Receiving {filename}") as pbar:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    pbar.update(len(data))

        print(f"File received and saved as {save_path}")
        conn.close()


if __name__ == "__main__":
    start_server()
