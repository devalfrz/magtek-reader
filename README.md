# magtek-reader
HID Magtek Reader

This program is a simple example to use the Magtek 99875205 Rev 13 card reader (doc: https://www.magtek.com/docs/99875205.pdf), but may be used by other HID compatible hardware.

## Installation

### Mac and Linux
```
# Install pip
sudo easy_install pip

# Install dependencies
sudo pip install cython

# Download and install cython-hidapi 
git clone https://github.com/gbishop/cython-hidapi
cd cython-hidapi
sudo python setup-mac.py build # Or setup-linux.py
sudo python setup-mac.py install # Or setup-linux.py

# Download magtek-reader.py
git clone https://github.com/devalfrz/magtek-reader
cd magtek-reader

# Test :)
python magtek-reader.py -v
```
