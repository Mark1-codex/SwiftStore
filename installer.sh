#!/bin/bash


set -e  
echo "=========================================="
echo "Installing SwiftStore"
echo "=========================================="


if [ "$EUID" -ne 0 ]; then
    echo "Error: This installer requires root privileges."
    echo "Please run with: sudo ./installer.sh"
    exit 1
fi


echo "Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    apt-get update -qq
    apt-get install -y python3 python3-pip python3-venv git
elif command -v dnf &> /dev/null; then
    dnf install -y python3 python3-pip git
elif command -v pacman &> /dev/null; then
    pacman -Syu --noconfirm python python-pip git
else
    echo "Warning: Unsupported package manager. Python 3 and pip must be installed manually."
fi


INSTALL_DIR="/opt/swiftstore"
echo "Installing SwiftStore to $INSTALL_DIR..."


mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

if [ ! -f main.py ]; then
    echo "Cloning repository..."
    git clone https://github.com/Mark1-codex/SwiftStore.git .
else
    echo "Repository already exists, pulling latest changes..."
    git pull
fi

# Create virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing Python dependencies..."
pip install rapidfuzz keyboard

echo "Creating launcher /usr/bin/swiftstore..."
cat > /usr/bin/swiftstore << 'EOF'
#!/bin/bash
# SwiftStore launcher

INSTALL_DIR="/opt/swiftstore"

if [ ! -d "$INSTALL_DIR/venv" ]; then
    echo "Error: SwiftStore is not properly installed."
    exit 1
fi

cd "$INSTALL_DIR"
source venv/bin/activate
exec python main.py "$@"
EOF

chmod +x /usr/bin/swiftstore


echo ""
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
echo "  Enter        - Open / Edit"
echo "  Space        - Select"
echo "  Ctrl+Enter   - Go to parent"
echo "  Ctrl+N       - New file"
echo "  Ctrl+Shift+N - New folder"
echo "  Ctrl+D       - Delete"
echo "  Ctrl+S       - Copy"
echo "  Ctrl+M       - Move"
echo "  Ctrl+R       - Rename"
echo "  Ctrl+F       - Search"
echo ""
echo "To uninstall later: sudo rm -rf /opt/swiftstore /usr/bin/swiftstore"