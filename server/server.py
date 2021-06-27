import sys
sys.path.append("~/rover-pi/rover")
print(sys.path)
from uploader import Uploader

class Server(Uploader):
    pass