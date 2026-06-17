# SwiftStore

A lightweight, keyboard-driven **Terminal User Interface (TUI)** file manager for Linux.  
Fast, minimal, and powerful — remastered from VaultTUI.

![SwiftStore](https://raw.githubusercontent.com/Mark1-codex/SwiftStore/main/logo.py)  

# Features  

- Blazing-fast navigation with arrow keys  
- Multi-selection with **Space**  
- Built-in file editing (opens in `nano`)  
- Create files/folders  
- Copy, Move, Rename, Delete  
- Fuzzy search across files (powered by  `rapidfuzz`)  
- Automatic permission handling  
- Easy one-command installer  

# Installation

```bash
git clone https://github.com/Mark1-codex/SwiftStore.git
cd SwiftStore
sudo ./installer.sh
```  
After installation, launch it anytime with:  
```swiftstore```  

# Hotkeys

Key    Action  
↑ / ↓  Navigate  
Enter  Open folder / edit file  
Space  Toggle multi-selection / select multiple items  
Ctrl+Enter    Go to parent directory  
Ctrl+N        New file  
Ctrl+Shift+N  New directory
Ctrl+D        Delete  
Ctrl+S        Copy  
Ctrl+M        Move  
Ctrl+R        Rename  
Ctrl+F        Fuzzy search  
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

### Made with ❤️ by Mark1-codex
Contributions welcome!  
My email - saneswtsanes@gmail.com
