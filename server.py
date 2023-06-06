import socket
import threading
import io
from PIL import Image
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    file = io.BytesIO()
    image_chunk = client_socket.recv(2048)
    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)
        if image_chunk == b"%IMAGE_COMPLETED%":
            break
    image = Image.open(file)
    w, h = image.size
    l = 0
    t = 0
    r = w/2
    b = h
    im = image.crop((l, t, r, b))
    im.save("s_image1.jpeg", format='JPEG')
    l = w/2
    t = 0
    r = w
    b = h
    im1 = image.crop((l, t, r, b))
    im1.save("s_image2.jpeg", format='JPEG')

def handle_client1(client_socket1, client_address1):
    print(f"[NEW CONNECTION] {client_address1} connected.")
    files = open('s_image1.jpeg', 'rb')
    image_data = files.read(2048)
    while image_data:
        client_socket1.send(image_data)
        image_data = files.read(2048)
    client_socket1.send(b'%IMAGE_COMPLETED%')
    files.close()
    with open('client1_edit.jpeg', 'wb') as file:
        recv_data = client_socket1.recv(2048)
        while recv_data:
            file.write(recv_data)
            recv_data = client_socket1.recv(2048)
            if recv_data == b"%IMAGE_COMPLETED%":
                break

def handle_client2(client_socket2, client_address2):
    print(f"[NEW CONNECTION] {client_address2} connected.")
    files = open('s_image2.jpeg', 'rb')
    image_data = files.read(2048)
    while image_data:
        client_socket2.send(image_data)
        image_data = files.read(2048)
    client_socket2.send(b'%IMAGE_COMPLETED%')
    files.close()
    with open('client2_edit.jpeg', 'wb') as file:
        recv_data = client_socket2.recv(2048)
        while recv_data:
            file.write(recv_data)
            recv_data = client_socket2.recv(2048)
            if recv_data == b"%IMAGE_COMPLETED%":
                break
    image1 = Image.open('client1_edit.jpeg')
    image2 = Image.open('client2_edit.jpeg')
    i1_size = image1.size
    i2_size = image2.size
    merge_image = Image.new('RGB', (2*i1_size[0], i1_size[1]), (250, 250, 250))
    merge_image.paste(image1, (0, 0))
    merge_image.paste(image2, (i1_size[0], 0))
    merge_image.save("m_image.jpeg", format='JPEG')

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        client_socket1, client_address1 = server.accept()
        thread1 = threading.Thread(
            target=handle_client1, args=(client_socket1, client_address1))
        thread1.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        client_socket2, client_address2 = server.accept()
        thread2 = threading.Thread(
            target=handle_client2, args=(client_socket2, client_address2))
        thread2.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

print("[STARTING] server is starting...")
start()

