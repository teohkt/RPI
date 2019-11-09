# RPI

Setting up the RPI

The following projects were completed using Rasbian Stretch on a Raspberry Pi 3 B+

To Check which version you have installed:

###cat /etc/os-release

##Wifi Configuration

First you would need to set the country location. This can be found through:
Application Menue > Preferences > Raspberry Pi Configuration > Localisation > Set WiFi Country

Next you can access the Wfi list from the icon in the top left toolbar.

##Setting up SSH
This allows you to connect to the RPI through wifi from a separate computer to avoid the need for a second keyboard, mouse, and HDMI monitor.

Application Menue > Preferences > Raspberry Pi Configuration > Interfaces > Enable SSH.
Restart RPI

From now on, you can access the RPI through the same WIFI config with

###ssh pi@raspberrypi.local


##Installing Dependencies

1. Update and upgrade any existing packages [30 minutes]

###sudo apt-get update && sudo apt-get upgrade

2. Install CMake, used to configure the OpenCV build process

###sudo apt-get install build-essential cmake pkg-config [2 minutes]

3. Install image I/O packages that allow us to load various image file formats such as JPEG, PNG, TIFF, etc [2 minutes]

###sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

4. Install video I/O packages that allow us to load various video file formats and streams [4 minutes]

###sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
###sudo apt-get install libxvidcore-dev libx264-dev

5. In order to utilize a sub module of OpenCV called highgui, we need to install GTK development library. highgui is used to display images to the screen and build basic GUIS [8 minutes]

###sudo apt-get install libgtk2.0-dev libgtk-3-dev

6. These dependencies help optimize matrix operations [3 minutes]

###sudo apt-get install libatlas-base-dev gfortran

7. The following are python 2.7 and python 3 headers so we can compile OpenCV with python bindings [3 minutes]

###sudo apt-get install python2.7-dev python3-dev

##Downloading the OpenCV source code

Currently the latest OpenCV is 4.1.2 [4 minutes]

###wget -O opencv.zip https://github.com/Itseez/opencv/archive/4.1.2.zip
###unzip opencv_contrib.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/4.1.2.zip
unzip opencv_contrib.zip

##Obtaining Python 2.7 and Python 3

1. Get pip [1 minute]
###wget https://bootstrap.pypa.io/get-pip.py

2. Install python 2.7 [1 minute]
###sudo python get-pip.py

3. Install Python 3 [1 minute]
###sudo python3 get-pip.py

##Setting up virtual environments [2 minutes]

###sudo pip install virtualenv virtualenvwrapper
###sudo rm -rf ~/.cache/pip

Apply this to ~./profile through

$ echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
$ echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
$ echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

Reload source and create a virtual evironment!
###source ~/.profile
###mkvirtualenv cv -p python3

To check into your virtual environment,

###source ~/.profile
###workon cv

##Installing Numpy [3 minutes]
Within the cv virtual environment,
###pip install numpy

##Compile and Install OpenCV

cd ~/opencv-4.1.2
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.1.2/modules \
    -D BUILD_EXAMPLES=OFF ..
    
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.1.2/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

observe the current total swap size, this should be < 100
free -m 

Change it to 1024

sudo nano /etc/dphys-swapfile    
#CONDF_SWPASIZE=100
CONF_SWAPSIZE=1024

^ is the control function. Press "ctrl" + "x" to exit, and "Y" for yes. Press enter to save.

$ sudo /etc/init.d/dphys-swapfile stop
$ sudo /etc/init.d/dphys-swapfile start

make -j4

To delete the build directory, we can use

rm -r build

Install OpenCV

sudo make install
sudo ldconfig


Set the bindings so that cv can be called within a script

$ cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
$ ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so
