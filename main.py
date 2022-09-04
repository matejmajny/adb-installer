import requests, os, zipfile, sys, time

if os.name != "nt":
    print("Different OS than Windows is not supported yet!")
    time.sleep(2)
    exit()

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

download("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")

print("\nUnzipping...")
with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
    zip_ref.extractall("C:\\")

print("Deleting zip and adding platform-tools to path...")
os.remove("platform-tools.zip")
os.system('set Path=%Path%;C:\\platform-tools')
print("\nSuccesful! Now you can open cmd anywhere and use adb/fastboot commands.")
