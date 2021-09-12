# Linux Installation

You'll be happy to know that this app works great in Linux, too! Here is a guide for installing osr2mp4 on Linux.

**Important**:

Check your current Python version. As of the time of writing, osr2mp4 requires Python 3.7 or higher and does not properly support lower versions. You can check your Python version by typing `python --version` in the terminal. If your version is lower than 3.7, consider upgrading.

**We do NOT want to downgrade Python, as it would break any other apps that rely on the newer version!**

# Installing ffmpeg

## Arch Linux, Manjaro, EndeavourOS

On arch, ffmpeg is an official package so it can be installed with `sudo pacman -S ffmpeg`. 

Proceed to Configuring and Running osr2mp4 to continue.

-------------------------------------------------------------------------------------------------------------------------------------

## Ubuntu, Pop!_OS and other Debian derivatives

Install `ffmpeg`.

```

sudo apt update

sudo apt upgrade

sudo apt-get install ffmpeg

```

Proceed to Configuring and Running osr2mp4 to continue.

-------------------------------------------------------------------------------------------------------------------------------------

## MacOS

The easiest way to use osr2mp4 on MacOS will be by installing most of our components with Brew, so please make sure you have this configured before we continue. MacOS has the following requirements before we can begin the installation process: `brew install zlib jpeg freetype xz ffmpeg`. After these are installed we can begin. 

Proceed to Configuring and Running PyEnv and osr2mp4 to continue.

-------------------------------------------------------------------------------------------------------------------------------------

# Configuring and Running osr2mp4

1. Change your directory to wherever you need want to install osr2mp4 and clone the osr2mp4 repository, then step into the osr2mp4-app folder in your terminal. This should look something like this:

```

          ~ $ cd /home/username/Documents

   Documents $ git clone https://github.com/uyitroa/osr2mp4-app

   Documents $ cd osr2mp4-app

```

2. Now we'll remove some packages and install dependencies for osr2mp4: 

```
pip uninstall PIL Pillow
pip install -r requirements.txt
python install.py
```
You should now be able to run osr2mp4. Make sure you are in the osr2mp4 file that you cloned from the repo and run `python main.py`. If this returns `No module XXXX` then you need to run `pip install XXXX` and try again.
