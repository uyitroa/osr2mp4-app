# Linux Installation

You'll be happy to know that this app works great in Linux, too! Here is a guide for installing osr2mp4 on Linux.

**Important**:

Check your current Python version. As of the time of writing, osr2mp4 requires Python 3.7 and does not yet support Python 3.8. You can check your Python version by typing `python --version` in the terminal. If your version is lower than 3.7, consider upgrading. If your version is higher than 3.7 OR you do not want to upgrade to 3.7, please see the following instructions for installing Python 3.7.8 alongside your current Python installation.

**We do NOT want to downgrade Python, as it would break any other apps that rely on the newer version!**

# Installing PyEnv and ffmpeg

## Arch Linux, Manjaro, EndeavourOS

1. Install `ffmpeg` and `pyenv`. If you already have Python 3.7, you can skip the information about installing PyEnv and just install ffmpeg. We'll use PyEnv to allow us to run Python 3.7.8 while still having Python 3.8 on our system. PyEnv and ffmpeg are official packages so they can be installed with `sudo pacman -S ffmpeg pyenv`. You can also get PyEnv [on GitHub](https://github.com/pyenv/pyenv).

2. Next we need the following dependencies so that we can build our Python 3.7.8 installation from source: `sudo pacman -S base-devel openssl zlib`

3. Add `pyenv-init` to your shell configuration file (~/.bashrc in Arch). The easiest way to do this is with your text editor of choice (in this example, I will use nano.) `nano ~/.bashrc` Scroll all the way to the bottom of the file and add a new line: `eval "$(pyenv init -)"`. It's always best practice to leave comments when you edit any file, and this can be done with ## on a new line:

```

## PyEnv Init

eval "$(pyenv init -)"

```

4. Close your terminal and then open it again. You won't notice any changes yet, but we have just made it possible to use different versions of Python through PyEnv without removing your current version.

Proceed to Configuring and Running PyEnv and osr2mp4 to continue.

-------------------------------------------------------------------------------------------------------------------------------------

## Ubuntu 20.04, Pop!_OS, other Ubuntu derivatives

1. Install `ffmpeg` and `pyenv`. If you already have Python 3.7, you can skip the information about installing PyEnv and just install ffmpeg.

```

sudo apt update

sudo apt upgrade

sudo apt-get install ffmpeg

```

To install PyEnv, clone the PyEnv repository to ~/.pyenv `git clone https://github.com/pyenv/pyenv.git ~/.pyenv`

Then define the variable PYENV_ROOT to point to the path where the repo is cloned and add $PYENV_ROOT/bin to your $PATH:

```

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc

echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

```

2. Next we need the following dependencies so that we can build our Python 3.7.8 installation from source. This may take a while depending on your internet connection and your processor:

```

sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

```

If you somehow cannot install libreadline-dev, there is an alternative: `sudo apt install libedit-dev`

3. Add `pyenv-init` to your shell configuration file (~/.bashrc in Ubuntu). The easiest way to do this is with your text editor of choice (in this example, I will use nano.) `nano ~/.bashrc` Scroll all the way to the bottom of the file and add a new line: `eval "$(pyenv init -)"`. It's always best practice to leave comments when you edit any file, and this can be done with ## on a new line:

```

## PyEnv Init

eval "$(pyenv init -)"

```

4. Close your terminal and then open it again. You won't notice any changes yet, but we have just made it possible to use different versions of Python through PyEnv without removing your current version.

Proceed to Configuring and Running PyEnv and osr2mp4 to continue.

-------------------------------------------------------------------------------------------------------------------------------------

## MacOS

1. The easiest way to use osr2mp4 on MacOS will be by installing most of our components with Brew, so please make sure you have this configured before we continue. MacOS has the following requirements before we can begin the installation process: `brew install zlib jpeg freetype xz ffmpeg`. After these are installed we can begin. Install PyEnv through Brew: `brew install pyenv`.

2. For MacOS Catalina or later (or if you are using zsh instead of bash): 
          Do `echo 'eval "$(pyenv init -)"' >>~/.zshrc`
For MacOS Mojave or older, (or if you are using bash):

          Add `pyenv-init` to your shell configuration file (~/.bash_profile in MacOS). The easiest way to do this is with your text editor of choice. Open the file and a new line `eval "$(pyenv init -)"` at the end. It is important that this is put at the end of the file in order to prevent unwanted behavior in your terminal.

3. Close your terminal and then open it again. You won't notice any changes yet, but we have just made it possible to use different versions of Python through PyEnv without removing your current version.

Proceed to Configuring and Running PyEnv and osr2mp4 to continue.

-------------------------------------------------------------------------------------------------------------------------------------

# Configuring and Running PyEnv and osr2mp4

1. Verify that PyEnv has been properly installed by typing `pyenv --version`. It should return a version number. If not, check the output from your installation and see if there are errors.

2. Close your terminal and then open it again. You won't notice any changes yet, but we have just made it possible to use different versions of Python through PyEnv without removing your current version.

3. Install Python 3.7.X. Use `pyenv versions` to list all of the versions available for install. In this example we will be using Python 3.7.8: `pyenv install 3.7.8`. This may take a long time depending on how powerful your processor is.

**Before you proceed, you should switch to Python 3.7 in your terminal or nothing will work.** Do this with `pyenv shell 3.7.8` We're now using Python 3.7.8 in our Terminal. Great! But before we proceed we need to upgrade pip, Python's package manager. `pip install --upgrade pip`.

4. Now change your directory to wherever you need want to install osr2mp4 and clone the osr2mp4 repository, then step into the osr2mp4-app folder in your terminal. This should look something like this:

```

          ~ $ cd /home/username/programs

   programs $ git clone https://github.com/uyitroa/osr2mp4-app

   programs $ cd osr2mp4-app

```

6. Now we'll remove some packages and install dependencies for osr2mp4: 

```
pip uninstall PIL Pillow
pip install -r requirements.txt
python install.py
```
You should now be able to run osr2mp4. Make sure you are in the osr2mp4 file that you cloned from the repo and run `python main.py`. If this returns `No module XXXX` then you need to run `pip install XXXX` and try again.
