from posixpath import expanduser
import requests, os, zipfile, sys, time, winreg, ctypes
# Thanks to @flandolf for more like half of this script lmao

print("Android Platform Tools Installer v2.5")
print("By: @matejmajny and @flandolf")
print("OS: " + sys.platform + "/" + os.name)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

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


def main():
    if (os.name == "nt"): # Windows code (by Matt & Andy)
        if not is_admin():
            # Re-run the script with administrative privileges using the 'runas' verb
            print("Admin privileges required, re-running script as admin...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            exit(0)
            
        else:
            # Check if adb is already installed
            if (os.path.exists("C:\\platform-tools")):
                print("Platform tools already installed, deleting...")
                os.system("rmdir /s /q C:\\platform-tools")
                print("Reinstalling...")

            download("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
            print("\nUnzipping...")
            with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
                zip_ref.extractall("C:\\")

            print("Deleting zip and adding platform-tools to path...")
            os.remove("platform-tools.zip")


            # Define the path to modify the PATH environment variable in the registry
            path_to_modify = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"

            # Open the registry key for the path to modify
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path_to_modify, 0, winreg.KEY_ALL_ACCESS)

            # Read the current value of the PATH environment variable
            current_path = winreg.QueryValueEx(key, "Path")[0]

            # Modify the PATH environment variable by appending a new path to it
            new_path = "C:\\platform-tools"
            modified_path = current_path + ";" + new_path

            # Write the modified PATH environment variable back to the registry
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, modified_path)

            # Close the registry key
            winreg.CloseKey(key)
            
            # Exit messages
            print("All done! You can now use adb/fastboot commands anywhere!")
            print("Do not forget to restart CMD/PowerShell or in some cases whole PC.")
            input("Press ENTER to exit")
            exit()
        
    elif (os.name == "posix"): # Linux code (by dumpy), and ngl why is linux so complicated  <------(also he loves PRs)
        path = "$PATH"
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
                with open(expanduser("~") + "/.bashrc", "r") as f:
                    # Check if already added
                    if (f.read().find("platform-tools") == -1):
                        with open(expanduser("~") + "/.bashrc", "a") as f:
                            f.write(r"export PATH=$PATH:~/platform-tools")
                        os.system(r'source ~/.bashrc')
                        print("Done!")
                    else:
                        print("Already added!")
            elif (shell.endswith("zsh")):
                with open(expanduser("~") + "/.zshrc", "r") as f:
                    # Check if already added
                    if (f.read().find("platform-tools") == -1):
                        print("Adding to zshrc...")
                        with open(expanduser("~") + "/.zshrc", "a") as f:
                            f.write(r'export PATH="$PATH:~/platform-tools"')
                        os.system(r'source ~/.zshrc')
                        print("Done!")
                    else:
                        print("Already added!")
            elif (shell.endswith("fish")):
                with open(expanduser("~") + "/.config/fish/config.fish", "r") as f:
                    if (f.read().find("platform-tools") == -1):
                            print("Adding to config.fish...")
                            with open(expanduser("~") + "/.config/fish/config.fish", "a") as f:
                                f.write("set PATH $PATH ~/platform-tools")
                            os.system(r'source ~/.config/fish/config.fish')
                            print("Done!")
                    else:
                        print("Already added!")
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
                logoutrequired = True
                print("Done!")
            
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

        
    else: # OS not supported
        print("Your OS is not supported yet, please open an issue on GitHub")
        input("Press ENTER to exit.")
        exit()

def start():
    tos = input("\nWith pressing ENTER you agree with Android SDK Platform-Tools terms of service. (anything else = no)\n")
    if tos == "":
        main()
    else:
        exit()

start()
exit(0)
