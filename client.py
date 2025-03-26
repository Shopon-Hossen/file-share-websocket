# client.py
import socket
import os
from tkinter import filedialog
from tqdm import tqdm

def send_file(server_ip, port=5001, file_to_send=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    filename = os.path.basename(file_to_send)
    client_socket.sendall(filename.encode().ljust(1024))  # Send filename (padded to 1024 bytes)

    filesize = os.path.getsize(file_to_send)
    with open(file_to_send, 'rb') as f, tqdm(total=filesize, unit='B', unit_scale=True, desc=f"Sending {filename}") as pbar:
        chunk = f.read(1024)
        while chunk:
            client_socket.sendall(chunk)
            pbar.update(len(chunk))
            chunk = f.read(1024)

    print(f"File {filename} sent successfully!")
    client_socket.close()


if __name__ == "__main__":
    server_ip_last_octet = input("Server IP (192.168.1.?): ")
    full_server_ip = f"192.168.1.{server_ip_last_octet}"

    while True:
        input("Press Enter to send a file... ")
        file_to_send = filedialog.askopenfilename(title="Select file to send")

        if file_to_send:
            send_file(full_server_ip, port=5001, file_to_send=file_to_send)
        else:
            print("No file selected.")
