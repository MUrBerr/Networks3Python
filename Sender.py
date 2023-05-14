import io
import socket
import os
import sys
import time

SERVER_ADDR = ("127.0.0.1", 9090)
FILE = ("file", os.path.getsize("file"))
FIRST_HALF = "first"
SECOND_HALF = "second"
TIMEOUT = 0.001
CONTINUE_MSG = b"Continue"
EXIT_MSG = b"Exit"
EXIT_CODES = (0, 1)
AUTH = f"{int(5965 ^ 7788)}".encode()
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE
CC = (b"reno", b"cubic")
CONT = b"liel"


def divide_file():
    with open(FILE[0], "rb") as file:
        with open(FIRST_HALF, "wb") as f1:
            f1.write(file.read(FILE[1]))

        file.seek(FILE[1])

        with open(SECOND_HALF, "wb") as f2:
            f2.write(file.read())


def main():
    divide_file()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
        sock.connect(SERVER_ADDR)

        while True:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, CC[0])

            with open(FIRST_HALF, "rb") as file:
                while True:
                    data = file.read(BUFFER_SIZE)
                    if not data:
                        break
                    sock.sendall(f"N${data.decode()}".encode())
                    time.sleep(TIMEOUT)
                    data = file.read(BUFFER_SIZE)
                sock.sendall(f"F${data.decode()}".encode())
                time.sleep(TIMEOUT)
            print("First half has been sent.")

            sock.sendall(CONT)

            data = sock.recv(BUFFER_SIZE)
            if data != AUTH:
                print("Authentication doesn't match.")
                sys.exit(EXIT_CODES[1])
            print("Received Authentication.")

            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, CC[1])

            with open(SECOND_HALF, "rb") as file:
                while True:
                    data = file.read(BUFFER_SIZE)
                    if not data:
                        break
                    sock.sendall(f"N${data.decode()}".encode())
                    time.sleep(TIMEOUT)
                    data = file.read(BUFFER_SIZE)
                sock.sendall(f"F${data.decode()}".encode())
                time.sleep(TIMEOUT)
            print("Second half has been sent.")

            sock.sendall(CONT)

            user_decision = input("Send again? (y/n) ")
            while user_decision.lower() != "y" and user_decision.lower() != "n":
                user_decision = input("Send again? [enter 'y' or 'n' only!] ")

            if user_decision.lower() == "y":
                sock.sendall(CONTINUE_MSG)

                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, CC[0])
                continue

            elif user_decision.lower() == "n":
                sock.sendall(EXIT_MSG)
                sock.shutdown(socket.SHUT_RDWR)
                break

if __name__ == "__main__":
    main()
