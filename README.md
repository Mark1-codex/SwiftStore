# SwiftStore

A lightweight, keyboard-driven **Terminal User Interface (TUI)** file manager for Linux.  
Fast, minimal, and powerful — remastered from VaultTUI.

## Features

- Blazing-fast navigation with arrow keys
- Multi-selection with **Space**
- Built-in file editing (opens in `nano`)
- Create files and folders
- Copy, Move, Rename, Delete
- Fuzzy search (powered by `rapidfuzz`)
- Automatic permission handling
- Easy one-command installer

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/Mark1-codex/SwiftStore/main/installer.sh | sudo bash
```  
After installation, launch it anytime with:  
```swiftstore```  

# Hotkeys

Key           Action  
↑ / ↓         Navigate
← / →         Switch tabs  
Enter         Open folder / edit file  
Space         Toggle multi-selection / select multiple items  
Ctrl+Enter    Go to parent directory  
Ctrl+N        New file  
Shift+N  New directory
Ctrl+D        Delete  
Ctrl+S        Copy  
Ctrl+M        Move  
Ctrl+R        Rename  
Ctrl+F        Fuzzy search
Ctrl+T        Open terminal (";exit" or ";quit" in terminal to stop the terminal)  
Shift+Enter   Refresh   

# Dependencies

- Python 3  
- rapidfuzz  
- keyboard  
- nano  
(All automatically installed with installer.sh)  

# Locations across the system

- Launcher - /usr/bin/swiftstore  
- App files - /opt/swiftstore  

### Made with ❤️ by Mark Kapkan (aka. Mark1-codex)
Contributions welcome!  
My email - saneswtsanes@gmail.com
