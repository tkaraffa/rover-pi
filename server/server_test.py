import sys
sys.path.append("/home/pi/rover-pi")
from server import Server

if __name__ == "__main__":
    server = Server()
    server.run()