# ADB Installer Script 📱
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/matejmajny/adb-installer?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/flandolf/adrod13?color=orange&style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/flandolf/adrod13?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/flandolf/adrod13?style=for-the-badge)    
A simple Python script for installing ADB (Android Debug Bridge) on Windows and Linux systems, and automatically adding ADB to the system's PATH.

## Requirements
- Python 3.x
- Windows 8.1 or above **or** some linux distro
## Installation
Clone the repo or download the script
Run the script using python 3
```bash
python3 main.py
```
Follow the prompts to install ADB on your system.
## Usage
Once the installation is complete, you can use ADB commands in the command prompt or terminal without having to specify the full path to the ADB binary.

## Troubleshooting
If you get an error message that ADB is not recognized as an internal or external command, make sure that the script has added ADB to the system's PATH.
If you are on Linux and get a permission error, run the script with superuser (sudo) privilege.
Some linux users may need additional udev rules for their device to be succefully recognized, if this is you please run the `linuxudev.py` file which should attempt to find your device and also install a generic rule list.
## Contributing
We welcome contributions to this script. If you have any suggestions or improvements, please feel free to open a pull request.
## License
This script is released under the MIT License.
