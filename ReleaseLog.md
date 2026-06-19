# Welcome to ReleaseLog, here I will post all of my major updates! Note: Added since SwiftStore V2.0
## Version 2.0
### What is new? 
In this version, I refactored the whole code logic to include multi-tab functional with potential for further updates.  
Currently. there are 2 tabs in the app:  
- File manager (main window)  
- File preview tab with basic info about the file.  
You can switch between tabs using left / right arrows.  
I also added tracking of terminal width which auto-detects terminal width on ```update()```. This toggles UI width (divider width, etc.)  
Also included:  
- Uninstaller script (at /usr/bin/swiftstore-uninstall) (access it by ```swiftstore-uninstall```)
- Updater script (at /usr/bin/swiftstore-updater) (access it by ```swiftstore-update```) (only available after Version 2.0)  
### How to download?  
You can reinstall the file manager (```sudo rm -rf /opt/swiftstore /usr/bin/swiftstore && curl -fsSL https://raw.githubusercontent.com/Mark1-codex/SwiftStore/main/installer.sh | sudo bash```).  After updating, there will be a specific script for updating which you can access with:  
```swiftstore-update```.