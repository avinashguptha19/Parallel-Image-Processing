import socket
import io
from PIL import Image
from PIL import ImageFilter
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.5"
ADDR = (SERVER, PORT)
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect(ADDR)
file = io.BytesIO()
recv_data = client1.recv(2048)
while recv_data:
    file.write(recv_data)
    recv_data = client1.recv(2048)
    if recv_data == b"%IMAGE_COMPLETED%":
        break
image = Image.open(file)
im = image.filter(ImageFilter.FIND_EDGES)
im.save("client1_image.jpeg", format='JPEG')
files = open('client1_image.jpeg', 'rb')
image_data = files.read(2048)
while image_data:
    client1.send(image_data)
    image_data = files.read(2048)
client1.send(b"%IMAGE_COMPLETED%")
files.close()
client1.close()

