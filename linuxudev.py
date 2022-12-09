import os, time

# adds usb device to udev
if (os.name != 'posix'):
    print("This script only works on Linux")
    time.sleep(1.5)
    exit()
else:
    mode = input("Select mode [1] Download generic rules [2] Attempt to detect device: ")
    
    if (mode == '1'):
        print("Adding generic list...")
        os.system(r'sudo wget https://raw.githubusercontent.com/M0Rf30/android-udev-rules/master/51-android.rules -O /etc/udev/rules.d/51-android.rules')
        print("Reloading udev rules...")
        os.system(r'sudo udevadm control --reload-rules')
        os.system(r'sudo udevadm trigger')
        # see package manager
        if (os.system(r'which apt') == 0):
            print("Downloading package...")
            os.system(r'sudo apt install android-sdk-platform-tools-common')
        print("Done!")
    else:
        print("Adding udev rules...")
        print("Plug your device in now...")
        input("Press any key to continue...")
        # Get ID from lsusb
        id = os.popen(r'lsusb | grep -i android | cut -d " " -f 6').read()
        print("Device found! ID: " + id)
        # Get vendor and product ID
        vendor = id[:4]
        product = id[5:9]
        # Write udev rules
        os.system('sudo echo SUBSYSTEM=="usb", ATTR{idVendor}=="{}", ATTR{idProduct}=="{}", MODE="0666", GROUP="plugdev" > /etc/udev/rules.d/51-android.rules'.format(vendor, product))
