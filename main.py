import os
from pathlib import Path
from rapidfuzz import process, fuzz
import keyboard as kb
import time
import sys
import termios
import pwd

sf = Path.home()
sfi = os.listdir(sf)
citem = sfi[0] if len(sfi) >= 1 else ""
selected_items = set()
VIEWPORT_SIZE = 20
view_start = 0

def get_user_ids():
    user = pwd.getpwnam(os.getlogin())
    return user.pw_uid, user.pw_gid

def toggle_select():
    global citem, selected_items
    if citem in selected_items:
        selected_items.remove(citem)
    else:
        selected_items.add(citem)
    update()

def update(e=""):
    global citem, sf, sfi, view_start
    sfi = os.listdir(sf)
    if e == "parent":
        sf = sf.parent
        sfi = os.listdir(sf)
        citem = sfi[0] if len(sfi) >= 1 else ""
        view_start = 0
    os.system("clear")
    if not sfi:
        print("No items in this directory!")
        return
    if e == "down":
        idx = sfi.index(citem)
        citem = sfi[0] if idx == len(sfi) - 1 else sfi[idx + 1]
    elif e == "up":
        idx = sfi.index(citem)
        citem = sfi[len(sfi) - 1] if idx == 0 else sfi[idx - 1]
    idx = sfi.index(citem)
    if idx < view_start:
        view_start = idx
    elif idx >= view_start + VIEWPORT_SIZE:
        view_start = idx - VIEWPORT_SIZE + 1
    print("==========================")
    print(f"{sf}")
    print("==========================")
    view_end = view_start + VIEWPORT_SIZE
    show_boxes = len(selected_items) > 0
    for i in range(view_start, min(view_end, len(sfi))):
        item = sfi[i]
        item_path = sf / item
        emoji = "📁" if item_path.is_dir() else "📄"
        marker = ' >' if item == citem else '  '
        if show_boxes:
            sel = '[x]' if item in selected_items else '[ ]'
            print(f"{marker} {sel} {emoji} {item}")
        else:
            print(f"{marker} {emoji} {item}")
    print("==========================")

def clear_buffer():
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def enter():
    global sf, citem, sfi, view_start
    target = sf / citem
    if target.is_dir():
        sf = target
        sfi = os.listdir(sf)
        citem = sfi[0] if sfi else ""
        view_start = 0
        update()
    elif target.is_file():
        kb.unhook_all()
        os.system(f"nano '{target}'")
        rehook()
        update()

def delete_item():
    global sf, citem, sfi, selected_items
    kb.unhook_all()
    time.sleep(0.2)
    items_to_delete = selected_items if selected_items else {citem}
    for item in items_to_delete:
        target = sf / item
        os.system(f"rm -rf '{target}'")
    selected_items.clear()
    sfi = os.listdir(sf)
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
    new_path = Path(sf) / filename
    new_path.touch()
    uid, gid = get_user_ids()
    os.chown(new_path, uid, gid)
    rehook()
    update()

def makefolder():
    global sf
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    filename = input('New folder name: ')
    new_path = Path(sf) / filename
    os.mkdir(new_path)
    uid, gid = get_user_ids()
    os.chown(new_path, uid, gid)
    rehook()
    update()

def copy():
    global sf, citem, selected_items
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    items_to_copy = selected_items if selected_items else {citem}
    newfilepath = input('Enter the destination path: ')
    for item in items_to_copy:
        source = sf / item
        newlocation = Path(newfilepath) / item
        os.system(f"cp -r '{source}' '{newlocation}'")
        uid, gid = get_user_ids()
        os.chown(newlocation, uid, gid)
    selected_items.clear()
    rehook()
    update()

def move():
    global sf, citem, selected_items
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    items_to_move = selected_items if selected_items else {citem}
    newfilepath = input('Enter the new destination path: ')
    for item in items_to_move:
        source = sf / item
        newlocation = Path(newfilepath) / item
        os.system(f"mv '{source}' '{newlocation}'")
        uid, gid = get_user_ids()
        os.chown(newlocation, uid, gid)
    selected_items.clear()
    rehook()
    update()

def rename():
    global sf, citem
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    newfilename = Path(input('Enter the new file name: '))
    oldlocation = Path(sf) / citem
    newlocation = Path(sf) / newfilename.name
    os.rename(oldlocation, newlocation)
    citem = newfilename.name
    uid, gid = get_user_ids()
    os.chown(newlocation, uid, gid)
    rehook()
    update()

def search():
    global sfi, sf
    kb.unhook_all()
    time.sleep(0.2)
    clear_buffer()
    os.system("clear")
    option = input("Enter the location to search (;current - current location, ;home - home folder): ")
    path_to_search = Path.home() if option == ";home" else sf
    search_query = input("Enter the query: ")
    data = [str(p.name) for p in path_to_search.rglob("*")]
    found_files = process.extract(search_query, data, scorer=fuzz.WRatio, score_cutoff=80)
    os.system("clear")
    if not found_files:
        print("No files found. Press shift+enter to return.")
    else:
        print(f"Found {len(found_files)} file(s):")
        for i in found_files:
            print(f"{i[0]}")
        print("\nSearch complete. Press shift+enter to return.")
    rehook()

def rehook():
    kb.add_hotkey("shift+enter", lambda: update())
    kb.add_hotkey("enter", enter)
    kb.add_hotkey("up", lambda: update("up"))
    kb.add_hotkey("down", lambda: update("down"))
    kb.add_hotkey("space", toggle_select)
    kb.add_hotkey("ctrl+enter", lambda: update("parent"))
    kb.add_hotkey("ctrl+n", makefile)
    kb.add_hotkey("ctrl+shift+n", makefolder)
    kb.add_hotkey("ctrl+d", delete_item)
    kb.add_hotkey("ctrl+s", copy)
    kb.add_hotkey("ctrl+r", rename)
    kb.add_hotkey("ctrl+m", move)
    kb.add_hotkey("ctrl+f", search)

os.system("clear")
import logo
print("Welcome to VaultTUI-remastered! Press shift+enter to begin.")
rehook()
kb.wait()