from posixpath import expanduser
import requests, os, zipfile, sys, time
print("Android Platform Tools Installer v2.0")
print("By: @matejmajny and @dumpydev")
print("OS: " + sys.platform)

def download(link): #taken from my older project
    with open("platform-tools.zip", "wb") as f:
        print("Downloading platform-tools")
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()

if (os.name == "nt"): #Windows code
    download("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
    print("\nUnzipping...")
    with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
        zip_ref.extractall("C:\\")

    print("Deleting zip and adding platform-tools to path...")
    os.remove("platform-tools.zip")
    os.system('set Path=%Path%;C:\\platform-tools')
    print("All done! You can now use adb/fastboot commands anywhere!")  
elif (os.name == "posix"): # Linux code (by dumpy)
    logoutrequired = False
    download("https://dl.google.com/android/repository/platform-tools-latest-linux.zip")
    print("\nUnzipping...")
    with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
        zip_ref.extractall(expanduser("~"))
    os.remove("platform-tools.zip")
    print("Would you like to add to path?")
    if(input('[Y]es [N]o: ').lower() == 'y'):
        shell = os.readlink('/proc/%d/exe' % os.getppid())
        print("Detected Shell: " + shell[shell.rfind('/')+1:])
        if (shell.endswith("bash")):
            print("Adding to bashrc...")
            os.system(r'echo "export PATH=$PATH:~/platform-tools" >> ~/.bashrc')
            os.system(r'source ~/.bashrc')
            print("Done!")
        elif (shell.endswith("zsh")):
            print("Adding to zshrc...")
            os.system(r'echo "export PATH=$PATH:~/platform-tools" >> ~/.zshrc')
            os.system(r'source ~/.zshrc')
            print("Done!")
        elif (shell.endswith("fish")):
            print("Adding to config.fish...")
            os.system(r'echo "export PATH=$PATH:~/platform-tools" >> ~/.config/fish/config.fish')
            os.system(r'source ~/.config/fish/config.fish')
            print("Done!")
        print("Adding executeable permissions...")
        os.system(r'chmod +x ~/platform-tools/*')
        print("Done!")
        print("Checking if user is in plugdev group...")
        if (os.system(r'groups | grep plugdev') == 0):
            print("User is in plugdev group, nothing to do...")
            print("Done!")
        else:
            print("User is not in plugdev group, adding... (SUDO required)")
            os.system(r'sudo usermod -a -G plugdev $USER')
            logoutrequired = true
            print("Done!")
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

        print("Done!")
        print("Reloading udev rules...")
        os.system('sudo udevadm control --reload-rules')
        print("Done!")
        print("Adding USB device permissions...")
        os.system('sudo chmod 666 /dev/bus/usb/*/*')
        print("Done!")
        print("All done! You can now use adb/fastboot commands anywhere!")
    else: 
        print("You can add it manually by adding ~/platform-tools to your PATH variable")

    if (logoutrequired):
        print("Please logout and login for changes to take effect!")
    else:
        print("No logout required!")
    print("All done! You can now use adb/fastboot commands anywhere!")
else:
    print("Your OS is not supported yet, please open an issue on GitHub")
