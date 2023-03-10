import socket
import sys

IP = ""
PORT = ""
ADDR = ""
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():

    n = len(sys.argv)
    if(n ==2):
        print("total 2 arguments are needed")
        return 
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (IP, PORT)


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

if __name__ == "__main__":
    main()