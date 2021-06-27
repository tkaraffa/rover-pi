import sys
sys.path.append("/home/pi/rover-pi")
from server.server import Server

if __name__ == "__main__":
    test_app = Server()
    test_app.app.run(debug=True, host='0.0.0.0')