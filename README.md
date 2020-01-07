# blast-daq
USB NDIR Gas Data Acquisition 

For use on Raspberry Pi 4

##Setup
First update Raspbian
sudo apt-get update
sudo apt-get upgrade

Install Dependencies
sudo apt-get install git
sudo apt-get install python3-pip
sudo pip3 install paho-mqtt
sudo pip3 install pyserial
git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git
cd Adafruit_Python_ADS1x15
sudo python setup.py install

