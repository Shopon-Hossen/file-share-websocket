import socket
import os
from tkinter import filedialog
from tqdm import tqdm


def send_file(server_ip, port=5001, file_to_send=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
    except Exception as e:
        print("Connection failed:", e)
        return

    filesize = os.path.getsize(file_to_send)
    with open(file_to_send, 'rb') as f, tqdm(total=filesize, unit='B', unit_scale=True, desc='Sending') as pbar:
        chunk = f.read(1024)
        while chunk:
            client_socket.sendall(chunk)
            pbar.update(len(chunk))
            chunk = f.read(1024)
    client_socket.close()


if __name__ == "__main__":
    server_ip_last_octet = input("Server IP (192.168.1.?): ")
    file_to_send = filedialog.askopenfilename(title="Select file to send")
    if file_to_send:
        send_file(f"192.168.1.{server_ip_last_octet}", file_to_send=file_to_send)
    else:
        print("No file selected. Exiting.")
