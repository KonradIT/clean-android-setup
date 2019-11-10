## Clean Android setup tool

Script to automate and ease the pains of setting up a 1) pseudo-burner phone 2) sandboxed testing environment .

This is intended to be used with a device that has been factory resetted. 

### Process:

Depending on the purpose of your device, wether if it's intended to provide with some decent privacy and security options or if it's meant to help debug an app, the script will perform certain actions on your device. For example, installing a custom certificate for capturing network traffic is suited for testing environment and not for a burner phone

- Installs MITM cert
- Installs apps of your choice
- Plugs recommended settings
- Allows for some minor debloating

### Running:
	pip3 install -r requirements.txt # install deps
    python3 clean_android_tool.py 
    
Will use a ncurses-like UI.

### Apps to choose from:

Pseudo-burner phone config (these are the apps I use in my burner, add other apps to download in apps:[] in config.json):

- DNS66
- NetGuard
- Calyx VPN
- FFLITE
- ObscuraCAM
- Haven
- Simple Keyboard
- Riot.im
- Conversations

Testing environment:

- Logs (logcat reader)
- ADB over network
- oandbackup
- WifiAnalyzer
- Termux

### Tools and scripts installed:

Pseudo-burner phone: None

Testing environment:

- if Android version < 5.0:
	- CuckoDroid tools (https://github.com/idanr1986/droidmon, etc... that need root access)
- Frida daemon
- Gnirehtet

More to be added, this is generally what I use, feel free to PR and add your tools and scripts.
