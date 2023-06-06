import socket
import io
from PIL import Image
from PIL import ImageFilter
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.5"
ADDR = (SERVER, PORT)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(ADDR)
file = io.BytesIO()
recv_data = client2.recv(2048)
while recv_data:
    file.write(recv_data)
    recv_data = client2.recv(2048)
    if recv_data == b"%IMAGE_COMPLETED%":
        break
image = Image.open(file)
im = image.filter(ImageFilter.FIND_EDGES)
im.save("client2_image.jpeg", format='JPEG')
files = open('client2_image.jpeg', 'rb')
image_data = files.read(2048)
while image_data:
    client2.send(image_data)
    image_data = files.read(2048)
client2.send(b"%IMAGE_COMPLETED%")
files.close()
client2.close()

