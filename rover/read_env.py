from rover.rover_enums import Pins
from rover import Rover
from time import sleep

def main():
    rover = Rover()
    while True:
        data = rover.create_data()
        rover.upload_data(data)
        sleep(rover.upload_frequency)

if __name__=="__main__":
    main()

"""
git --version # make sure git is installed
sudo apt-get install git # if it isn't
cd # go to your home directory
git clone https://github.com/tkaraffa/rover-pi.git # puts the whole repo in a folder called rover-pi
cd rover-pi # cd into the newly created folder
pip install -r requirements.txt # download all the necessary libraries (probably can skip this)

nano rover/rover_enums.py
# change all pins to yours, make sure your credentials.json file is called credentials.json
# this will be around Line 13-23
# also change the spreadsheet name to yours

python rover/read_env.py # this actually runs the script
"""