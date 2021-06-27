import sys
sys.path.append("/home/pi/rover-pi")
# sys.path.append("/home/pi/rover-pi/rover")

print(sys.path)
from uploader import Uploader

class Server(Uploader):
    pass