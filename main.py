import sys
import os
from pathlib import Path
import keyboard as kb
import time
import shutil
import termios
import rich
from rich.console import Console, Group
from rich.panel import Panel

console = Console()
class Tabs:
    def __init__(self):
        self.tabs = ["Files", "Info"]
        self.current = 0
        self.content = {
            "Files": [],
            "Info": ["Info tab - select a file or folder to see details"]
        }

    def get_width(self):
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80

    def draw(self, file_lines=None):
        global sf
        width = self.get_width()
        console = Console()

        print("\033[2J\033[H\033[?25l", end="")

        tab_line = ""
        for i, tab in enumerate(self.tabs):
            if i == self.current:
                tab_line += f"[ {tab} ]"
            else:
                tab_line += f"  {tab}  "
            if i < len(self.tabs) - 1:
                tab_line += " | "
        print(tab_line)

        if self.current == 0 and file_lines:
            file_group = Group(*[line[:width-2] for line in file_lines[:30]])
            console.print(Panel(file_group, title=str(sf), padding=(0, 1)))
        else:
            lines = self.content[self.tabs[self.current]]
            for line in lines[:30]:
                print(line[:width-2])

        status = f"Tab {self.current+1}/{len(self.tabs)} | ↑ / ↓ Navigate | ← / → Switch Tab | Shift+Enter Refresh"
        print(status[:width])
        sys.stdout.flush()


sf = Path.home()
try:
    sfi = os.listdir(sf)
except:
    sfi = []
citem = sfi[0] if sfi else ""
selected_items = set()
VIEWPORT_SIZE = 15
view_start = 0

tabs = Tabs()


def clear_buffer():
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def get_info(item_path: Path) -> list:
    if not item_path.exists():
        return ["Nothing selected"]
    try:
        stat = item_path.stat()
        info = [
            f"Name: {item_path.name}",
            f"Full Path: {item_path}",
            f"Type: {'Directory' if item_path.is_dir() else 'File'}",
            f"Size: {stat.st_size / 1024:.2f} KB",
            f"Modified: {time.ctime(stat.st_mtime)}"
        ]
        if item_path.is_dir():
            try:
                count = len(os.listdir(item_path))
                info.append(f"Contains: {count} items")
            except:
                info.append("Cannot read directory")
        
        # Wrap the list of strings in a Group and then a Panel
        info_group = Group(*info)
        panel = Panel(info_group, title=f"Info about {str(item_path)}", padding=(0, 1))
        # Return it inside a list since tabs.content["Info"] expects an iterable of lines/renderables
        return [panel]
        
    except Exception as e:
        return [f"Error: {e}"]



def toggle_select():
    global citem, selected_items
    if citem in selected_items:
        selected_items.remove(citem)
    else:
        selected_items.add(citem)
    update()


def update(e=""):
    global citem, sf, sfi, view_start
    
    try:
        sfi = os.listdir(sf)
    except PermissionError:
        sfi = []
    
    if e == "parent":
        sf = sf.parent
        try: sfi = os.listdir(sf)
        except: sfi = []
        citem = sfi[0] if sfi else ""
        view_start = 0

    if e == "down" and sfi:
        idx = sfi.index(citem) if citem in sfi else -1
        citem = sfi[0] if idx == -1 or idx == len(sfi)-1 else sfi[idx+1]
    elif e == "up" and sfi:
        idx = sfi.index(citem) if citem in sfi else 0
        citem = sfi[len(sfi)-1] if idx <= 0 else sfi[idx-1]

    if not sfi:
        citem = ""
        view_start = 0
    elif citem not in sfi:
        citem = sfi[0] if sfi else ""
        view_start = 0
    else:
        idx = sfi.index(citem)
        if idx < view_start:
            view_start = idx
        elif idx >= view_start + VIEWPORT_SIZE:
            view_start = idx - VIEWPORT_SIZE + 1


    file_lines = []
    if not sfi:
        file_lines = ["No items in this directory!"]
    else:
        view_end = view_start + VIEWPORT_SIZE
        show_boxes = len(selected_items) > 0
        for i in range(view_start, min(view_end, len(sfi))):
            item = sfi[i]
            item_path = sf / item
            emoji = "📁" if item_path.is_dir() else "📄"
            marker = ' >' if item == citem else '  '
            if show_boxes:
                sel = '[x]' if item in selected_items else '[ ]'
                file_lines.append(f"{marker} {sel} {emoji} {item}")
            else:
                file_lines.append(f"{marker} {emoji} {item}")

    if citem:
        tabs.content["Info"] = get_info(sf / citem)
    else:
        tabs.content["Info"] = ["No selection"]

    tabs.content["Files"] = file_lines
    tabs.draw(file_lines)

def goup():
    update("up")
    os.system("clear")
    update("down")
    update("up")

def godown():
    update("down")
    os.system("clear")
    update("up")
    update("down")

def righthandler():
    setattr(tabs, 'current', (tabs.current + 2) % len(tabs.tabs)), update()
    os.system("clear")
    setattr(tabs, 'current', (tabs.current - 1) % len(tabs.tabs)), update()

def lefthandler():
    setattr(tabs, 'current', (tabs.current - 2) % len(tabs.tabs)), update()
    os.system("clear")
    setattr(tabs, 'current', (tabs.current + 1) % len(tabs.tabs)), update()

def rehook():
    kb.unhook_all()
    kb.add_hotkey("up", goup)
    kb.add_hotkey("down", godown)
    kb.add_hotkey("shift+up", righthandler)
    kb.add_hotkey("shift+down", lefthandler)
    
    kb.add_hotkey("right", righthandler)
    kb.add_hotkey("left",  lefthandler)
    
    kb.add_hotkey("shift+alt", lambda: update())
    kb.add_hotkey("alt", enter)
    kb.add_hotkey("space", toggle_select)
    kb.add_hotkey("ctrl+alt", lambda: update("parent"))
    
    kb.add_hotkey("ctrl+n", makefile)
    kb.add_hotkey("shift+n", makefolder)
    kb.add_hotkey("ctrl+d", delete_item)
    kb.add_hotkey("ctrl+s", copy)
    kb.add_hotkey("ctrl+m", move)
    kb.add_hotkey("ctrl+r", rename)
    kb.add_hotkey("ctrl+f", search)
    kb.add_hotkey("ctrl+/", chpath)
    kb.add_hotkey("ctrl+t", openterm)



def enter():
    global sf, citem, sfi, view_start
    target = sf / citem
    if target.is_dir():
        sf = target
        try: sfi = os.listdir(sf)
        except: sfi = []
        citem = sfi[0] if sfi else ""
        view_start = 0
        update()
    elif target.is_file():
        kb.unhook_all()
        clear_buffer()
        os.system(f"nano '{target}'" if os.path.exists("/usr/bin/nano") else f"vi '{target}'")
        rehook()
        update()

def delete_item():
    global sf, citem, sfi, selected_items
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    items_to_delete = selected_items if selected_items else {citem}
    for item in list(items_to_delete):
        target = sf / item
        os.system(f"rm -rf '{target}'")
    selected_items.clear()
    try: sfi = os.listdir(sf)
    except: sfi = []
    citem = sfi[0] if sfi else ""
    rehook()
    update()

def makefile():
    global sf
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    filename = input('New file name: ')
    new_path = sf / filename
    new_path.touch()
    clear_buffer()
    rehook()
    update()

def makefolder():
    global sf
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    foldername = input('New folder name: ')
    new_path = sf / foldername
    os.mkdir(new_path)
    clear_buffer()
    rehook()
    update()

def copy():
    global sf, citem, selected_items
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    items = selected_items if selected_items else {citem}
    dest = input('Destination path: ')
    for item in items:
        os.system(f"cp -r '{sf / item}' '{dest}'")
    selected_items.clear()
    clear_buffer()
    rehook()
    update()

def move():
    global sf, citem, selected_items
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    items = selected_items if selected_items else {citem}
    dest = input('Destination path: ')
    for item in items:
        os.system(f"mv '{sf / item}' '{dest}'")
    selected_items.clear()
    clear_buffer()
    rehook()
    update()

def rename():
    global sf, citem
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    newname = input('New name: ')
    old = sf / citem
    new = sf / newname
    os.rename(old, new)
    citem = newname
    clear_buffer()
    rehook()
    update()

def search():
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    query = input("Search query: ")
    results = [f for f in os.listdir(sf) if query.lower() in f.lower()]
    print("Results:", results)
    input("Press Enter to return...")
    clear_buffer()
    rehook()
    update()

def chpath():
    global sf
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    path = input("Enter path: ")
    if os.path.isdir(path):
        sf = Path(path)
    clear_buffer()
    rehook()
    update()

def openterm():
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    os.system("/opt/swiftstore/term" if os.path.exists("/opt/swiftstore/term") else "bash")
    clear_buffer()
    rehook()
    update()



if __name__ == "__main__":
    try:
        os.system("clear")
        import logo
        print("SwiftStore - Tabbed File Manager")
        print("Press shift+alt to begin. ")
        rehook()
        kb.wait()
    except KeyboardInterrupt:
        print("\033[?25h")
        print("Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        kb.unhook_all()