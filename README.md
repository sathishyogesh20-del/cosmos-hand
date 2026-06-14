# 🌌 COSMOS — Hand Gesture Device Controller

Control your computer with hand movements using your webcam — no keyboard, no mouse!

---

## 📁 Files in this folder

| File | Purpose |
|---|---|
| `index.html` | The COSMOS web app (PWA) |
| `manifest.json` | Makes it installable as an app named **COSMOS** |
| `sw.js` | Offline support (service worker) |
| `icon.svg` / `icon-192.png` / `icon-512.png` | App icons |
| `cosmos_controller.py` | **Python script** — gives the app real control over your PC mouse/keyboard |
| `requirements.txt` | Python packages needed |
| `START_COSMOS.bat` | One-click launcher for **Windows** |
| `START_COSMOS.sh` | One-click launcher for **Mac/Linux** |

---

## 🚀 PART 1 — Deploy the Web App (GitHub Pages)

1. Create a GitHub repo (e.g. `cosmos-hand`)
2. Upload **all files** from this folder (keep them in the root, not in subfolders)
3. Go to **Settings → Pages**
4. Source: **Deploy from a branch** → Branch: **main** → `/ (root)` → **Save**
5. Wait ~2 minutes → your app is live at:
   `https://YOUR_USERNAME.github.io/cosmos-hand`

---

## 🖥️ PART 2 — Enable Full Device Control (Optional but Powerful)

By default, COSMOS works **inside the browser only** — it can scroll the page, click on-page buttons, and trigger media play/pause for security reasons (browsers can't control your whole OS).

To let COSMOS **move your real mouse, click anywhere, and type on your real keyboard**, run the included Python controller:

### Windows:
1. Make sure [Python](https://python.org) is installed (check "Add to PATH" during install)
2. Double-click **`START_COSMOS.bat`**
3. It auto-installs requirements and starts listening

### Mac/Linux:
1. Open Terminal in this folder
2. Run: `./START_COSMOS.sh` (or `bash START_COSMOS.sh`)
3. **macOS**: grant Terminal **Accessibility** + **Screen Recording** permission in
   System Settings → Privacy & Security (required for PyAutoGUI to work)

### Then:
1. Open your COSMOS web app (the GitHub Pages URL)
2. Click the **"Connect"** button in the top banner
3. The banner turns **green = Connected** ✅
4. Now your hand controls the ENTIRE device!

---

## ✋ Gesture Guide

| Gesture | Action |
|---|---|
| ✋ Open hand | Pause / Play media |
| ✊ Closed fist | Stop |
| ☝️ Point (index finger) | Move cursor — hold position to click |
| ✌️ Peace sign | Scroll up/down |
| 👍 Thumbs up | Confirm / Enter |
| 🤏 Pinch (thumb+index) | Toggle on-screen keyboard |

**Keyboard shortcut:** `Alt + F` → instantly starts camera + hands-free mode

---

## 📱 Install as an App

- **Desktop Chrome/Edge**: Look for the install icon (⊕) in the address bar
- **Android**: Tap "Add to Home Screen" banner
- **iPhone**: Share button → "Add to Home Screen"

Once installed, COSMOS opens fullscreen like a native app — named **COSMOS** on your home screen/desktop!

---

## ⚠️ Safety Notes

- **Emergency stop**: Move your mouse to the **top-left corner** of the screen — PyAutoGUI's fail-safe will immediately stop all automated control.
- The Python controller only runs on **your own PC** (`localhost`) — no data is sent anywhere else.
- Close the Python terminal window anytime to fully disable device control.

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| Camera won't start | Allow camera permission in browser settings |
| "Cannot connect" banner | Make sure `cosmos_controller.py` is running |
| Gestures not detected | Ensure good lighting, hand fully visible in frame |
| Cursor moves erratically | Increase "Dwell Speed" in Settings for more stability |
| Mac: clicks don't work | Grant Accessibility permission to Terminal |

---

Built with 🌌 MediaPipe + PyAutoGUI + PWA technology
