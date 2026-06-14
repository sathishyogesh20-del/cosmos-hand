"""
COSMOS Hand Controller — PC Device Control Script
================================================
This script runs on your PC and receives hand gesture commands
from the COSMOS web app via WebSocket, then controls your mouse,
keyboard, and media using PyAutoGUI.

SETUP (run once):
  pip install websockets pyautogui

RUN:
  python cosmos_controller.py

Then open your COSMOS app and click "Connect" in the banner.
"""

import asyncio
import json
import sys
import os
import subprocess
import platform

# Check dependencies
try:
    import websockets
except ImportError:
    print("Installing websockets...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
    import websockets

try:
    import pyautogui
except ImportError:
    print("Installing pyautogui...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

# Safety settings
pyautogui.FAILSAFE = True   # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.01      # Small delay between actions

SCREEN_W, SCREEN_H = pyautogui.size()
print(f"Screen size: {SCREEN_W}x{SCREEN_H}")
print("COSMOS Controller starting on ws://localhost:8765")
print("Open your COSMOS app and click 'Connect'")
print("Move mouse to top-left corner to emergency stop")
print("-" * 50)

# Track last position for smooth movement
last_x, last_y = SCREEN_W // 2, SCREEN_H // 2

async def handle_command(cmd_data):
    global last_x, last_y
    try:
        cmd = cmd_data.get("cmd", "")
        
        # MOUSE MOVE — smooth cursor control
        if cmd == "move_mouse":
            bx = cmd_data.get("x", 0)
            by = cmd_data.get("y", 0)
            bw = cmd_data.get("sw", 1920)
            bh = cmd_data.get("sh", 1080)
            # Map browser coordinates to screen coordinates
            sx = int((bx / bw) * SCREEN_W)
            sy = int((by / bh) * SCREEN_H)
            # Clamp to screen bounds
            sx = max(0, min(SCREEN_W - 1, sx))
            sy = max(0, min(SCREEN_H - 1, sy))
            # Smooth movement
            pyautogui.moveTo(sx, sy, duration=0.05)
            last_x, last_y = sx, sy

        # CLICK
        elif cmd == "click":
            bx = cmd_data.get("x", last_x)
            by = cmd_data.get("y", last_y)
            bw = cmd_data.get("sw", 1920)
            bh = cmd_data.get("sh", 1080)
            sx = int((bx / bw) * SCREEN_W)
            sy = int((by / bh) * SCREEN_H)
            sx = max(0, min(SCREEN_W - 1, sx))
            sy = max(0, min(SCREEN_H - 1, sy))
            pyautogui.click(sx, sy)
            print(f"🖱️  Click at ({sx}, {sy})")

        # RIGHT CLICK
        elif cmd == "right_click":
            pyautogui.rightClick(last_x, last_y)
            print(f"🖱️  Right click at ({last_x}, {last_y})")

        # DOUBLE CLICK
        elif cmd == "double_click":
            pyautogui.doubleClick(last_x, last_y)
            print(f"🖱️  Double click at ({last_x}, {last_y})")

        # SCROLL
        elif cmd == "scroll":
            dy = cmd_data.get("dy", 0)
            clicks = int(dy / 30)  # Convert pixels to scroll clicks
            if clicks != 0:
                pyautogui.scroll(-clicks)  # Negative = scroll down
                direction = "↓" if clicks < 0 else "↑"
                print(f"🖱️  Scroll {direction} ({abs(clicks)} clicks)")

        # TYPE TEXT
        elif cmd == "type_text":
            text = cmd_data.get("text", "")
            if text == "\b":
                pyautogui.hotkey("backspace")
            elif text == "\n" or text == "enter":
                pyautogui.press("enter")
            elif text:
                pyautogui.write(text, interval=0.02)
            print(f"⌨️  Typed: {repr(text)}")

        # KEY PRESS
        elif cmd == "key_press":
            key = cmd_data.get("key", "")
            if key:
                pyautogui.press(key)
                print(f"⌨️  Key: {key}")

        # HOTKEY
        elif cmd == "hotkey":
            keys = cmd_data.get("keys", [])
            if keys:
                pyautogui.hotkey(*keys)
                print(f"⌨️  Hotkey: {'+'.join(keys)}")

        # MEDIA CONTROLS
        elif cmd == "media_play_pause":
            pyautogui.press("playpause")
            print("🎵 Play/Pause")

        elif cmd == "media_stop":
            pyautogui.press("stop")
            print("🎵 Stop")

        elif cmd == "media_next":
            pyautogui.press("nexttrack")
            print("🎵 Next track")

        elif cmd == "media_prev":
            pyautogui.press("prevtrack")
            print("🎵 Previous track")

        elif cmd == "volume_up":
            pyautogui.press("volumeup")
            print("🔊 Volume up")

        elif cmd == "volume_down":
            pyautogui.press("volumedown")
            print("🔉 Volume down")

        elif cmd == "volume_mute":
            pyautogui.press("volumemute")
            print("🔇 Mute")

        # WINDOW CONTROLS
        elif cmd == "minimize_window":
            pyautogui.hotkey("win", "down")
            print("🪟 Minimize window")

        elif cmd == "maximize_window":
            pyautogui.hotkey("win", "up")
            print("🪟 Maximize window")

        elif cmd == "close_window":
            pyautogui.hotkey("alt", "f4")
            print("🪟 Close window")

        elif cmd == "switch_window":
            pyautogui.hotkey("alt", "tab")
            print("🪟 Switch window")

        elif cmd == "show_desktop":
            pyautogui.hotkey("win", "d")
            print("🪟 Show desktop")

        # SCREENSHOT
        elif cmd == "screenshot":
            img = pyautogui.screenshot()
            img.save("cosmos_screenshot.png")
            print("📸 Screenshot saved: cosmos_screenshot.png")

        else:
            print(f"❓ Unknown command: {cmd}")

    except pyautogui.FailSafeException:
        print("🛑 Emergency stop triggered (mouse moved to corner)")
    except Exception as e:
        print(f"❌ Error executing '{cmd}': {e}")

async def handler(websocket, path=None):
    client = websocket.remote_address
    print(f"✅ COSMOS app connected from {client}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                await handle_command(data)
            except json.JSONDecodeError:
                print(f"Invalid message: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 COSMOS app disconnected from {client}")

async def main():
    print("\n" + "="*50)
    print("  COSMOS HAND CONTROLLER — PC CONTROL MODE")
    print("="*50)
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Screen: {SCREEN_W} x {SCREEN_H}")
    print(f"  Server: ws://localhost:8765")
    print("="*50)
    print("\n  Waiting for COSMOS app to connect...")
    print("  Open COSMOS in your browser and click 'Connect'\n")

    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 COSMOS Controller stopped.")
