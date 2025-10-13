This is a quick project i used chatgpt to make. It uses your phone camera to detect blinking 
and if it does, it scrolls on your screen on for example tiktok.

I did this on windows, haven't tested on other operating systems
There's an installation guide at the end of this readme

Here are the links to some of the libraries i used

https://pypi.org/project/opencv-python/
https://pypi.org/project/mediapipe/
https://numpy.org/
https://pyautogui.readthedocs.io/en/latest/install.html


  ----  Installation guide

1. First you need to download and install platform-tools and add it to path.
If you dont know how to add stuff to path, search it up

Link: https://developer.android.com/tools/releases/platform-tools

2. Also make sure you have python and pip installed

3. Then you need to open a command prompt inside the folder this folder
After that you need to type this into cmd

python -m pip install -r requirements.txt

4. Now follow a tutorial online to turn on developer mode on your phone and then inside developer settings, turn on usb debugging

5. If you want to use your phone camera then its probably best to install droidcam on both pc and phone
Now make sure if your using droidcam to edit the settings of the video to use mjpeg
Link to droidcam: https://droidcam.app/

6. Open main.py and when choosing the cameranumber the laptop camera often defaults to zero. If you want to use your phone camera you should try to use 1, 2, 3, etc. It depends on how many cameras are on or connected to your computer.

Connect your phone via usb to your computer. Now launch the main.py and blink into the camera your using to swipe