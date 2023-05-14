import io
import socket
import time

SERVER_ADDR = ("127.0.0.1", 9090)
FILE = "received"
TIMEOUT = 0.001
CONTINUE_MSG = b"Continue"
EXIT_MSG = b"Exit"
EXIT_CODES = (0, 1)
AUTH = f"{int(5965 ^ 7788)}".encode()
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE
CC = (b"reno", b"cubic")
NUM_CONNECTIONS = 300
SPLITTER = b"$"
FINAL_SEGMENT = b"F"
NOT_FINAL_SEGMENT = b"N"
CONT = b"liel"
renu_times = []
cubic_times = []


def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, CC[0])
        sock.bind(SERVER_ADDR)
        sock.listen(NUM_CONNECTIONS)
        client, addr = sock.accept()

        while True:
            start = time.time()
            with open(FILE, "wb") as file:
                while True:
                    data = client.recv(io.DEFAULT_BUFFER_SIZE)
                    if data.__contains__(CONT):
                        file.write(data)
                        break
                    file.write(data)
            end = time.time()
            print("First part has been received.")
            renu_times.append(float(end - start))

            client.sendall(AUTH)
            time.sleep(TIMEOUT)
            print("Authentication has been sent.")

            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, CC[1])

            start = time.time()
            with open(FILE, "wb") as file:
                while True:
                    data = client.recv(io.DEFAULT_BUFFER_SIZE)
                    if data.__contains__(CONT):
                        file.write(data)
                        break
                    file.write(data)
            end = time.time()
            print("Second part has been received.")
            cubic_times.append(float(end - start))


            print("Waiting for data from the client...")
            x = client.recv(io.DEFAULT_BUFFER_SIZE)
            print("Data received")
            if x == CONTINUE_MSG:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, CC[0])

            elif x == EXIT_MSG:
                print("####################-RESULTS-####################")
                for i in range(len(renu_times)):
                    print(f"seq={i} reno={renu_times[i]} cubic={cubic_times[i]}")
                client.close()
                break


if __name__ == "__main__":
    main()
