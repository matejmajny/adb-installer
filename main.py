import requests, os, zipfile, sys

url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip" #platform tools
r = requests.get(url, allow_redirects=True)
open('platform-tools.zip', 'wb').write(r.content)

with zipfile.ZipFile("platform-tools.zip", 'r') as zip_ref:
    zip_ref.extractall("C:\\")

os.remove("platform-tools.zip")
os.system('set Path=%Path%;C:\\platform-tools')
