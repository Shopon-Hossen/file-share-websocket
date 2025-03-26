# server.py
import socket
from tqdm import tqdm
import os


class Path:
    def __init__(self, path=None):
        self.path = path if path else os.getcwd()

    def __str__(self):
        return self.path

    def __truediv__(self, other):
        return Path(os.path.join(self.path, other))


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
    # output_dir = filedialog.askdirectory(title="Where to save received files?")
    output_dir = Path() / "Received"
    if not output_dir:
        print("No directory selected. Exiting.")
        return

    print(output_dir)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, addr = server_socket.accept()

        # Receive the file name first
        filename = conn.recv(1024).decode().strip()
        if not filename:
            print("No filename received. Skipping transfer.")
            conn.close()
            continue

        # Make sure the filename doesn't overwrite an existing file
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
