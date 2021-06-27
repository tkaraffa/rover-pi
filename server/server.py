import sys
sys.path.append("/home/pi/rover-pi")

print(sys.path)
from rover.uploader import Uploader

class Server(Uploader):
    pass