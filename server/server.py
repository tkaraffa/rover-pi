import sys
sys.path.append("/home/pi/rover-pi")

from flask import Flask, render_template
from datetime import datetime

from rover.uploader import Uploader
from config.uploader_enums import Flask_Enums

class Server(Uploader):
    def __init__(self):
        super(Server, self).__init__()


    def run(self):
        self.app.run(debug=self.debug, host=self.host)

    