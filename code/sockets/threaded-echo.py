# echo_01_seq.py

import socket
import colorama
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Get all colorama colors
COLORAMA_COLOR_LIST = [
    color for color in dir(colorama.Fore) if color.isupper() and "EX" not in color
]
COLORAMA_COLORS = [
    getattr(colorama.Fore, color) for color in COLORAMA_COLOR_LIST if color != "RESET"
]

pool = ThreadPoolExecutor(max_workers=3)


def run_server(host="localhost", port=8085):
    sock = socket.create_server((host, port))
    sock.listen()
    sock.setblocking(True)
    print("Listening on {}:{}".format(host, port))
    print(COLORAMA_COLOR_LIST)
    while True:
        client_sock, x = sock.accept()
        pool.submit(handle_client, client_sock)


def random_color(str):
    """Takes str and returns a string with random color"""
    rand_color = random.choice(COLORAMA_COLORS)
    return rand_color + str + colorama.Fore.RESET


def handle_client(sock):
    """Takes a socket and handles the client"""
    while True:
        """Receive data from client"""
        data = sock.recv(1024)
        # decode data from bytes to string
        if not data or b"quit" in data:
            break
        # Do stuff. Sleep for a random amount of time
        time.sleep(random.randint(2, 10) * 0.05)
        data = data.decode("utf-8")
        """call random_color on data"""
        data = random_color(data)
        # Get current thread name
        thread_name = threading.current_thread().getName()
        colored_response = random_color(f"Rec onn {thread_name} {data}" + "\n")
        sock.sendall(bytes(colored_response, "utf-8"))

    print("Client disconnected:", sock.getpeername())
    sock.close()


if __name__ == "__main__":
    run_server()
