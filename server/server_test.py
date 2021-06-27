import sys
sys.path.append("/home/pi/rover-pi")
from server import Server

if __name__ == "__main__":
    server = Server()
    app = server.app
    app.run(debug=True, host='0.0.0.0')