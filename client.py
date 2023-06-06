import socket
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.5"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
file = open('koala.jpg', 'rb')
image_data = file.read(2048)
while image_data:
    client.send(image_data)
    image_data = file.read(2048)
client.send(b"%IMAGE_COMPLETED%")
file.close()
client.close()


