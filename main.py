from posixpath import expanduser
import requests, os, zipfile, sys, time


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

if (os.name == "nt"):
    download("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
    print("\nUnzipping...")
    with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
        zip_ref.extractall("C:\\")

    print("Deleting zip and adding platform-tools to path...")
    os.remove("platform-tools.zip")
    os.system('set Path=%Path%;C:\\platform-tools')
    print("\nSuccessful! Now you can open cmd anywhere and use adb/fastboot commands.")
elif (os.name == "posix"):
    download("https://dl.google.com/android/repository/platform-tools-latest-linux.zip")
    print("\nUnzipping...")
    with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
        zip_ref.extractall(expanduser("~"))
    print("Deleting zip and adding platform-tools to path...")
    os.remove("platform-tools.zip")
    # add to path
    os.system('export PATH=$PATH:~/platform-tools')
    # add to bashrc
    shell = os.readlink('/proc/%d/exe' % os.getppid())
    if (shell.endswith("bash")):
        os.system('echo "export PATH=$PATH:~/platform-tools" >> ~/.bashrc')
        os.system('source ~/.bashrc')
    elif (shell.endswith("zsh")):
        os.system('echo "export PATH=$PATH:~/platform-tools" >> ~/.zshrc')
        os.system('source ~/.zshrc')
    elif (shell.endswith("fish")):
        os.system('echo "export PATH=$PATH:~/platform-tools" >> ~/.config/fish/config.fish')
        os.system('source ~/.config/fish/config.fish')
    os.system('chmod +x ~/platform-tools/*')
    
    
    print("\nSuccessful! Now you can open terminal anywhere and use adb/fastboot commands.")
