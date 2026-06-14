#!/bin/bash
# COSMOS Hand Controller — Mac/Linux Launcher

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN} COSMOS HAND CONTROLLER - PC CONTROL MODE${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# Find python3
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo -e "${RED}ERROR: Python not found!${NC}"
    echo "Install Python from https://python.org or via your package manager."
    exit 1
fi

echo -e "${GREEN}Python found: $($PYTHON --version)${NC}"
echo ""
echo "Installing/updating required packages..."
$PYTHON -m pip install websockets pyautogui --quiet --upgrade

# macOS specific note
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo -e "${CYAN}macOS NOTE:${NC} You may need to grant Accessibility"
    echo "and Screen Recording permissions to Terminal in:"
    echo "System Settings > Privacy & Security > Accessibility"
    echo ""
fi

echo -e "${CYAN}============================================${NC}"
echo " Starting COSMOS Controller on port 8765"
echo -e "${CYAN}============================================${NC}"
echo ""
echo "NEXT STEPS:"
echo "1. Open your COSMOS app in the browser"
echo "2. Click the 'Connect' button at the top"
echo "3. Your hand now controls this device!"
echo ""
echo -e "${RED}SAFETY:${NC} Move mouse to TOP-LEFT corner of"
echo "screen anytime to instantly stop control."
echo ""
echo "Press Ctrl+C here to stop the controller."
echo -e "${CYAN}============================================${NC}"
echo ""

$PYTHON cosmos_controller.py
