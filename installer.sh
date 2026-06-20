#!/bin/bash

set -e

tput civis >/dev/null 2>&1

cleanup() {
    tput cnorm >/dev/null 2>&1
    if [ -n "$SPIN_PID" ]; then
        kill "$SPIN_PID" >/dev/null 2>&1
    fi
    clear >/dev/null 2>&1
}
trap cleanup EXIT INT TERM

show_spinner() {
    local items=("|" "/" "-" "/" "-" "\\")
    local cindex=0
    clear >/dev/null 2>&1
    while true; do
        cindex=$((cindex + 1))
        if [ "$cindex" -eq 6 ]; then
            cindex=0
        fi
        printf "\r[%s]" "${items[cindex]}"
        printf " Installing SwiftStore file manager..."
        sleep 0.25
    done
}

show_spinner &
SPIN_PID=$!

if [ "$EUID" -ne 0 ]; then
    kill "$SPIN_PID" >/dev/null 2>&1
    echo -e "\nError: This installer requires root privileges."
    echo "Please run with: sudo ./installer.sh"
    exit 1
fi

# System dependencies installation
install_build_tools() {
    if command -v apt-get &> /dev/null; then
        apt-get update -qq >/dev/null 2>&1
        apt-get install -y build-essential gcc python3 python3-pip python3-venv git >/dev/null 2>&1
    elif command -v dnf &> /dev/null; then
        dnf install -y gcc "Development Tools" python3 python3-pip git >/dev/null 2>&1
    elif command -v yum &> /dev/null; then
        yum groupinstall -y "Development Tools" >/dev/null 2>&1
        yum install -y gcc python3 python3-pip git >/dev/null 2>&1
    elif command -v pacman &> /dev/null; then
        pacman -Syu --noconfirm base-devel gcc python python-pip git >/dev/null 2>&1
    elif command -v apk &> /dev/null; then
        apk add --no-cache build-base gcc python3 py3-pip git >/dev/null 2>&1
    elif command -v zypper &> /dev/null; then
        zypper install -y gcc pattern:devel_basis python3 python3-pip git >/dev/null 2>&1
    fi
}

install_build_tools >/dev/null 2>&1

INSTALL_DIR="/opt/swiftstore"
mkdir -p "$INSTALL_DIR" >/dev/null 2>&1
cd "$INSTALL_DIR" >/dev/null 2>&1

# Repository handling
if [ ! -f main.py ]; then
    git clone https://github.com/Mark1-codex/SwiftStore.git . >/dev/null 2>&1
else
    git pull >/dev/null 2>&1
fi

python3 -m venv venv >/dev/null 2>&1
source venv/bin/activate >/dev/null 2>&1
pip install rapidfuzz keyboard >/dev/null 2>&1

touch /usr/bin/swiftstore >/dev/null 2>&1
touch /usr/bin/swiftstore-uninstall >/dev/null 2>&1
touch /usr/bin/swiftstore-update >/dev/null 2>&1

sudo tee /usr/bin/swiftstore > /dev/null << 'EOF'
#!/bin/bash
sudo -E /opt/swiftstore/venv/bin/python /opt/swiftstore/main.py "$@"
EOF

sudo tee /usr/bin/swiftstore-uninstall > /dev/null << 'EOF'
#!/bin/bash
echo "Uninstalling SwiftStore..."
sudo rm -rf /opt/swiftstore /usr/bin/swiftstore /usr/bin/swiftstore-uninstall /usr/bin/swiftstore-update "$@"
echo "Uninstalled SwiftStore successfully!"
EOF

sudo tee /usr/bin/swiftstore-update > /dev/null << 'EOF'
#!/bin/bash
echo "Updating SwiftStore..."
sudo rm -rf /usr/bin/swiftstore-uninstall /usr/bin/swiftstore-update /usr/bin/swiftstore /opt/swiftstore
curl -fsSL https://raw.githubusercontent.com/Mark1-codex/SwiftStore/main/installer.sh | sudo bash
EOF

sudo chmod +x /usr/bin/swiftstore >/dev/null 2>&1
sudo chmod +x /usr/bin/swiftstore-uninstall >/dev/null 2>&1
sudo chmod +x /usr/bin/swiftstore-update >/dev/null 2>&1

if [ ! -d "$INSTALL_DIR/venv" ]; then
    kill "$SPIN_PID" >/dev/null 2>&1
    echo -e "\nError: SwiftStore is not properly installed."
    exit 1
fi

if [ -f term.cpp ]; then
    g++ term.cpp -o term >/dev/null 2>&1
    rm -rf term.cpp >/dev/null 2>&1
fi

cd "$INSTALL_DIR" >/dev/null 2>&1
source venv/bin/activate >/dev/null 2>&1


kill "$SPIN_PID" >/dev/null 2>&1
clear >/dev/null 2>&1
tput cnorm >/dev/null 2>&1

clear
echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo ""
echo "You can now run SwiftStore by typing:"
echo "    swiftstore"
echo ""
echo "Installation location: /opt/swiftstore"
echo "Launcher: /usr/bin/swiftstore"
echo ""
echo "Hotkeys:"
echo "  ↑/↓          - Navigate"
echo "  ←/→          - Switch tabs"
echo "  Enter        - Open / Edit"
echo "  Space        - Select"
echo "  Ctrl+Enter   - Go to parent"
echo "  Ctrl+N       - New file"
echo "  Shift+N      - New folder"
echo "  Ctrl+D       - Delete"
echo "  Ctrl+S       - Copy"
echo "  Ctrl+M       - Move"
echo "  Ctrl+R       - Rename"
echo "  Ctrl+F       - Search"
echo ""
echo "To uninstall later: swiftstore-uninstall"
echo "To update later: swiftstore-update"