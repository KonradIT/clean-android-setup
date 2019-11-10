import json
import requests
import io
import os
from zipfile import ZipFile
from ppadb.client import Client as AdbClient

config = json.loads(open("config.json", "r").read())
client = AdbClient(host="127.0.0.1", port=5037)
mode = -1
index = "https://f-droid.org/repo/index-v1.jar"
download_uri = "https://f-droid.org/repo/%s"
def ask(statement):
	print(">>>", statement)
	return input("\t>>> ")

def get_apps(mode):
	return config[mode]["apps"]

def download_index():
	if os.path.isfile("index.json"):
		if ask("Index exists... Update? [Y/n]").upper() == "Y":
			os.remove("index.json")
		else:
			return 0
	r = requests.get(index, allow_redirects=True)
	with open("index.json","w") as out:
		with ZipFile(io.BytesIO(r.content), 'r') as zipfile:
			json.dump(json.loads(zipfile.read("index-v1.json")), out)

def find_app(name):
	with open("index.json","r") as out:
		j = json.loads(out.read())
		for app in j.get("apps"):
			if app.get("packageName") == name:
				return app
def download_app(app):
	print("Starting")
	filename = app.get("packageName") + "_" + app.get("suggestedVersionCode") + ".apk"
	r = requests.get(download_uri % filename, allow_redirects=True)
	open("apps/" + filename, 'wb').write(r.content)
	print("Downloaded %s" % filename)
	return filename
def install_app(app):
	devices = client.devices()
	for device in devices:
		try:
			device.install("apps/" + app)
		except Exception as e:
			print(e)

def check_settings(mode):
	for setting in config[mode]["settings"]:
		print("[%s]\n\tactual val: %s\n\texpected val: %s\n\tpassed: %s" % (setting[0], device.shell("getprop " + setting[0]), setting[1], device.shell("getprop " + setting[0]) == setting[1]))

def check_devices():
	return len(client.devices()) >= 1


print("Clean Android Tool")
print("Trying to make wiping your phone less of a PITA")

print("Checking for devices now...")
print("Plug in device and enable ADB\nPress enter when done.")
input("")
if not check_devices():
	print("No devices detected")
	exit()
print("Devices detected:")
devices = client.devices()
for device in devices:
	for index, device in enumerate(devices):
		print("[%s] - %s" % (index, device.get_serial_no())) 
c = ask("What's your desired configuration?\n\t- [0] Pseudo-burner phone\n\t- [1] Sandbox testing environment") 
if int(c) == 0:
	mode = "burner"
	print("Burner phone setting")
	download_index()
	for app in get_apps(mode):
		obj = find_app(app)
		f = download_app(obj)
		install_app(f)
elif int(c) == 1:
	mode = "sandbox"
	print("Sandbox testing setting")
	download_index()
	for app in get_apps(mode):
		obj = find_app(app)
		f = download_app(obj)
		install_app(f)
else:
	print("Number not recognized.")
