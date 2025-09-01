import tkinter as tk
import time
from screeninfo import get_monitors 
import keyboard, mouse
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor DPI awareness


# Get screen size
screen = get_monitors()[0]
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

# Appearance settings
STOPWATCH_WIDTH = 150
STOPWATCH_HEIGHT = 40
MARGIN = 5
FONT = ("Segoe UI", 30)
COLORS = ["#EEEEEE", "#A0A0FC", "#9BFABB", "#F7F787", "#FA8C8C", "#88F8DC"]

class Stopwatch:
    def __init__(self, master, y_offset, color):
        self.start_time = time.time()

        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-transparentcolor", "white")
        self.window.configure(bg="white")

        self.label = tk.Label(self.window, text="0.00", fg=color, bg="black", font=FONT)
        self.label.pack()

        x = SCREEN_WIDTH - STOPWATCH_WIDTH - MARGIN
        y = MARGIN + y_offset
       
        self.window.geometry(f"{STOPWATCH_WIDTH}x{STOPWATCH_HEIGHT}+{x}+{y}")

        self.window.deiconify() 

    def update(self):
        elapsed = time.time() - self.start_time
        self.label.config(text=f"{int(elapsed // 60)}:{round(elapsed % 60, 2):.1f}")

    def move_to(self, y_offset):
        x = SCREEN_WIDTH - STOPWATCH_WIDTH - MARGIN
        y = MARGIN + y_offset
        self.window.geometry(f"{STOPWATCH_WIDTH}x{STOPWATCH_HEIGHT}+{x}+{y}")

    def destroy(self):
        self.window.destroy()

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.stopwatches = []

        # Hotkeys
        add_stopwatch_hotkey = "ctrl+alt+W"
        remove_stopwatch_hotkey = "ctrl+alt+S"

        keyboard.add_hotkey(add_stopwatch_hotkey, self.add_stopwatch)
        keyboard.add_hotkey(remove_stopwatch_hotkey, self.remove_oldest)
        keyboard.add_hotkey("ctrl+alt+R", self.remove_all)

        mouse.on_button(self.add_stopwatch, buttons=('x2',), types=('down',))
        mouse.on_button(self.remove_oldest, buttons=('x',), types=('down',))

        self.update_all()
        print(f"Press {add_stopwatch_hotkey} to add stopwatch, {remove_stopwatch_hotkey} to remove.")

    def add_stopwatch(self):
        y_offset = len(self.stopwatches) * (STOPWATCH_HEIGHT + MARGIN)
        color = COLORS[len(self.stopwatches) % len(COLORS)]
        sw = Stopwatch(self.root, y_offset, color)
        self.stopwatches.append(sw)

    def remove_oldest(self):
        if self.stopwatches:
            sw = self.stopwatches.pop(0)
            sw.destroy()
            # Reposition the rest
            for i, s in enumerate(self.stopwatches):
                y = i * (STOPWATCH_HEIGHT + MARGIN)
                s.move_to(y)
    def remove_all(self):
        while self.stopwatches:
            sw = self.stopwatches.pop(0)
            sw.destroy()

    def update_all(self):
        for sw in self.stopwatches:
            sw.update()
        self.root.after(100, self.update_all)

# Main app
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main root window
    app = StopwatchApp(root)
    root.mainloop()