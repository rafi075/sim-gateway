import socket
import string
import threading
import sys
from client_conn import Client_INFO
from instruction import instruction
from collections import deque
import uuid

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

client_registry = []


instruction_queue = deque()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"
        msg = "ack::from::server" +msg
        conn.send(msg.encode(FORMAT))
        found,data = lookForIns(addr[0],addr[1])

        if(found):
            print(data)
            conn.send(data.encode(FORMAT))            

    conn.close()
    

def lookForIns(address, port):
    found = False
    data = ""
    for ins in instruction_queue:
        
        if(ins.to_address == address and ins.to_port == str(port)):
            data = ins.data
            instruction_queue.remove(ins)
            found = True
            break

    return found,data
        

def generate_unique_id():
    random_id = uuid.uuid1()
    return random_id

def register_client(conn,address):
    id = generate_unique_id()
    new_client = Client_INFO(conn,address[0],address[1],id)
    client_registry.append(new_client)

def print_registry():
    for client in client_registry:
        print("id: ",str(client.id) )
        print(" address: ",client.address )
        print(" port: ",client.port )
        print("\n")

def remove_from_registry(address,port):
    for object in client_registry:
        if(object.address == address and object.port == port ):
            client_registry.remove(object)
    
def load_ins(server,client_registry):
    print("loading instrution")
    while True:
        ins = input()
        ins_list = ins.split(":")
        if(ins_list[0] == "help"):
            print("help")
        elif(ins_list[0] == "SEND"):
            print("Instruction: "+ins)
            enqueue_ins(ins_list)
        elif(ins_list[0] == "exit"):
            server.close()
            break

def enqueue_ins(ins_list):

    ins_code = ins_list[0]
    new_ins = any
    if(ins_code == "SEND"):
        to_address=ins_list[1]
        to_port = ins_list[2]
        data = ins_list[3]
        new_ins = instruction(ins_code,to_address,to_port,data)
    elif(ins_code == "BROADCAST"):
        data = ins_list[1]
        new_ins = instruction(ins_code=ins_code,data=data)

    instruction_queue.append(new_ins)
    print("Instrction inserted to queue.\n")

def main():
    
    n = len(sys.argv)
    if(n ==2):
        print("total 2 arguments are needed. <server_ip_address> <server_port>")
        return 
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (IP, PORT)
    

    print("[STARTING] Server is starting at...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # run load instruction thread
    thread2 = threading.Thread(target=load_ins, args=(server,client_registry))  
    thread2.start()

    
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        register_client(conn,addr)
        print_registry()

        #creare thread for each accepted client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()