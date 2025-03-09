import socket
import subprocess
from tkinter import filedialog
from tqdm import tqdm


def print_ipconfig():
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if 'IPv4 Address' in line:
            print(line.strip())


def start_server(host='0.0.0.0', port=5001):
    print_ipconfig()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    while True:
        conn, addr = server_socket.accept()
        client_ip = addr[0]
        response = input(f"Request from {client_ip}, Accept? (y/n): ").strip() or "y"
        if response.lower() != "y":
            conn.close()
            continue

        output_file = filedialog.asksaveasfilename(title="Save received file as")
        if not output_file:
            conn.close()
            continue

        with open(output_file, 'wb') as f:
            with tqdm(unit='B', unit_scale=True, desc='Receiving') as pbar:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    pbar.update(len(data))
        conn.close()


if __name__ == "__main__":
    start_server()
