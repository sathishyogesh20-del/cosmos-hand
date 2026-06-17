"""
COSMOS Hand Controller — Full Device Control + Local Server
===========================================================
Run this script → it serves COSMOS locally AND controls your PC.
Open http://localhost:7860 in your browser — no GitHub needed!
"""

import asyncio, json, sys, subprocess, platform, time, os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ── Auto-install dependencies ──────────────────────────────
def install(pkg):
    subprocess.check_call([sys.executable,"-m","pip","install",pkg,"--quiet","--upgrade"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try: import websockets
except: print("  Installing websockets..."); install("websockets"); import websockets

try: import pyautogui
except: print("  Installing pyautogui..."); install("pyautogui"); import pyautogui

# PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.005

SCREEN_W, SCREEN_H = pyautogui.size()
OS = platform.system()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Local HTTP Server ──────────────────────────────────────
class SilentHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)
    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

def start_http_server():
    server = HTTPServer(("localhost", 7860), SilentHandler)
    server.serve_forever()

# ── Cursor tracking ────────────────────────────────────────
cur_x, cur_y = SCREEN_W // 2, SCREEN_H // 2

# ── Command handler ────────────────────────────────────────
async def run_cmd(data):
    global cur_x, cur_y
    cmd = data.get("cmd", "")
    try:

        # MOUSE MOVE
        if cmd == "move_mouse":
            bx = data.get("x",0); by = data.get("y",0)
            bw = data.get("sw",1920); bh = data.get("sh",1080)
            tx = int((bx/bw) * SCREEN_W)
            ty = int((by/bh) * SCREEN_H)
            tx = max(0, min(SCREEN_W-1, tx))
            ty = max(0, min(SCREEN_H-1, ty))
            cur_x += (tx - cur_x) * 0.55
            cur_y += (ty - cur_y) * 0.55
            pyautogui.moveTo(int(cur_x), int(cur_y))

        # CLICK
        elif cmd == "click":
            bx=data.get("x",cur_x); by=data.get("y",cur_y)
            bw=data.get("sw",1920); bh=data.get("sh",1080)
            sx=int((bx/bw)*SCREEN_W); sy=int((by/bh)*SCREEN_H)
            sx=max(0,min(SCREEN_W-1,sx)); sy=max(0,min(SCREEN_H-1,sy))
            pyautogui.click(sx,sy)
            print(f"  🖱  Click ({sx},{sy})")

        elif cmd == "double_click":
            pyautogui.doubleClick(int(cur_x),int(cur_y))
            print("  🖱  Double-click")

        elif cmd == "right_click":
            pyautogui.rightClick(int(cur_x),int(cur_y))
            print("  🖱  Right-click")

        elif cmd == "drag_start":
            pyautogui.mouseDown()
            print("  🖱  Drag start")

        elif cmd == "drag_end":
            pyautogui.mouseUp()
            print("  🖱  Drag end")

        # SCROLL
        elif cmd == "scroll":
            dy = data.get("dy",0)
            clicks = int(dy/25)
            if clicks != 0:
                pyautogui.scroll(-clicks)
                print(f"  🖱  Scroll {'↓' if clicks<0 else '↑'}")

        elif cmd == "scroll_up":
            pyautogui.scroll(5); print("  🖱  Scroll ↑")

        elif cmd == "scroll_down":
            pyautogui.scroll(-5); print("  🖱  Scroll ↓")

        # KEYBOARD TYPE
        elif cmd == "type_text":
            text = data.get("text","")
            if text == "\b": pyautogui.press("backspace")
            elif text in ("\n","enter"): pyautogui.press("enter")
            elif text == "\t": pyautogui.press("tab")
            elif text: pyautogui.write(text, interval=0.03)
            if text not in ("","\b"): print(f"  ⌨  Type: {repr(text)}")

        elif cmd == "key_press":
            key = data.get("key","")
            if key: pyautogui.press(key); print(f"  ⌨  Key: {key}")

        elif cmd == "hotkey":
            keys = data.get("keys",[])
            if keys: pyautogui.hotkey(*keys); print(f"  ⌨  Hotkey: {'+'.join(keys)}")

        # SHORTCUTS
        elif cmd == "copy":        pyautogui.hotkey("ctrl","c"); print("  ⌨  Copy")
        elif cmd == "paste":       pyautogui.hotkey("ctrl","v"); print("  ⌨  Paste")
        elif cmd == "cut":         pyautogui.hotkey("ctrl","x"); print("  ⌨  Cut")
        elif cmd == "undo":        pyautogui.hotkey("ctrl","z"); print("  ⌨  Undo")
        elif cmd == "select_all":  pyautogui.hotkey("ctrl","a"); print("  ⌨  Select All")
        elif cmd == "save":        pyautogui.hotkey("ctrl","s"); print("  ⌨  Save")
        elif cmd == "find":        pyautogui.hotkey("ctrl","f"); print("  ⌨  Find")
        elif cmd == "zoom_in":     pyautogui.hotkey("ctrl","+"); print("  ⌨  Zoom In")
        elif cmd == "zoom_out":    pyautogui.hotkey("ctrl","-"); print("  ⌨  Zoom Out")
        elif cmd == "new_tab":     pyautogui.hotkey("ctrl","t"); print("  ⌨  New Tab")
        elif cmd == "close_tab":   pyautogui.hotkey("ctrl","w"); print("  ⌨  Close Tab")
        elif cmd == "reload":      pyautogui.hotkey("ctrl","r"); print("  ⌨  Reload")

        # MEDIA KEYS
        elif cmd == "media_play_pause":
            pyautogui.press("playpause"); print("  🎵 Play/Pause")
        elif cmd == "media_stop":
            pyautogui.press("stop"); print("  🎵 Stop")
        elif cmd == "media_next":
            pyautogui.press("nexttrack"); print("  🎵 Next")
        elif cmd == "media_prev":
            pyautogui.press("prevtrack"); print("  🎵 Prev")
        elif cmd == "volume_up":
            for _ in range(3): pyautogui.press("volumeup")
            print("  🔊 Volume Up")
        elif cmd == "volume_down":
            for _ in range(3): pyautogui.press("volumedown")
            print("  🔉 Volume Down")
        elif cmd == "volume_mute":
            pyautogui.press("volumemute"); print("  🔇 Mute")

        # WINDOW MANAGEMENT
        elif cmd == "minimize_window":
            pyautogui.hotkey("win","down") if OS=="Windows" else pyautogui.hotkey("super","h")
            print("  🪟 Minimize")
        elif cmd == "maximize_window":
            pyautogui.hotkey("win","up") if OS=="Windows" else pyautogui.hotkey("super","up")
            print("  🪟 Maximize")
        elif cmd == "close_window":
            pyautogui.hotkey("alt","f4") if OS=="Windows" else pyautogui.hotkey("ctrl","q")
            print("  🪟 Close Window")
        elif cmd == "switch_window":
            pyautogui.hotkey("alt","tab"); print("  🪟 Alt+Tab")
        elif cmd == "show_desktop":
            pyautogui.hotkey("win","d") if OS=="Windows" else None
            print("  🪟 Show Desktop")
        elif cmd == "task_view":
            pyautogui.hotkey("win","tab"); print("  🪟 Task View")
        elif cmd == "open_start":
            pyautogui.hotkey("ctrl","esc"); print("  🪟 Start Menu")

        # OPEN APPS
        elif cmd == "open_browser":
            subprocess.Popen("start chrome",shell=True) if OS=="Windows" else subprocess.Popen(["open","-a","Google Chrome"])
            print("  🌐 Opened Browser")
        elif cmd == "open_notepad":
            subprocess.Popen("notepad",shell=True) if OS=="Windows" else subprocess.Popen(["open","-a","TextEdit"])
            print("  📝 Opened Notepad")
        elif cmd == "open_calculator":
            subprocess.Popen("calc",shell=True) if OS=="Windows" else subprocess.Popen(["open","-a","Calculator"])
            print("  🔢 Opened Calculator")
        elif cmd == "open_explorer":
            subprocess.Popen("explorer",shell=True) if OS=="Windows" else subprocess.Popen(["open","."])
            print("  📁 Opened Explorer")

        # SCREENSHOT
        elif cmd == "screenshot":
            fname = f"cosmos_screenshot_{int(time.time())}.png"
            pyautogui.screenshot(os.path.join(SCRIPT_DIR, fname))
            print(f"  📸 Screenshot: {fname}")

        # LOCK / SLEEP
        elif cmd == "lock_screen":
            pyautogui.hotkey("win","l") if OS=="Windows" else subprocess.Popen(["pmset","displaysleepnow"])
            print("  🔒 Locked Screen")

        else:
            pass  # Unknown command — silently ignore

    except pyautogui.FailSafeException:
        print("\n  🛑 EMERGENCY STOP — mouse moved to corner!\n")
    except Exception as e:
        print(f"  ❌ Error [{cmd}]: {e}")

# ── WebSocket handler ──────────────────────────────────────
async def ws_handler(ws, path=None):
    ip = ws.remote_address[0]
    print(f"\n  ✅ COSMOS connected! Full PC control is ACTIVE.")
    print(f"  🖐  Move your hand to control this computer!\n")
    try:
        async for msg in ws:
            try: await run_cmd(json.loads(msg))
            except json.JSONDecodeError: pass
    except websockets.exceptions.ConnectionClosed:
        print(f"\n  🔌 COSMOS disconnected.\n")

# ── Main ───────────────────────────────────────────────────
async def main():
    # Start HTTP server in background thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    print(f"\n{'='*54}")
    print(f"   COSMOS HAND CONTROLLER")
    print(f"{'='*54}")
    print(f"   OS     : {OS} {platform.release()}")
    print(f"   Screen : {SCREEN_W} x {SCREEN_H}")
    print(f"{'='*54}")
    print(f"\n  ✅ Local app server started!")
    print(f"\n  ➡  OPEN THIS URL IN YOUR BROWSER:")
    print(f"\n       http://localhost:7860")
    print(f"\n  (Copy and paste it into Chrome/Edge)")
    print(f"\n{'='*54}")
    print(f"  SAFETY: Move mouse to TOP-LEFT corner to stop!")
    print(f"{'='*54}\n")

    # Auto-open browser
    try:
        if OS == "Windows":
            subprocess.Popen("start http://localhost:7860", shell=True)
        elif OS == "Darwin":
            subprocess.Popen(["open", "http://localhost:7860"])
        else:
            subprocess.Popen(["xdg-open", "http://localhost:7860"])
        print("  🌐 Browser opened automatically!\n")
    except:
        pass

    # Start WebSocket server
    async with websockets.serve(ws_handler, "localhost", 8765,
                                ping_interval=20, ping_timeout=20):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  👋 COSMOS Controller stopped.\n")
