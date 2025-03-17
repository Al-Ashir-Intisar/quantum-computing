import ctypes
import os
import sys
import threading
import tkinter as tk

class NoSleep:
    def __init__(self):
        self.running = True
        self.thread = threading.Thread(target=self.prevent_sleep, daemon=True)
        self.thread.start()

    def prevent_sleep(self):
        """Prevent system sleep on Windows or macOS"""
        if os.name == "nt":  # Windows
            ES_CONTINUOUS = 0x80000000
            ES_SYSTEM_REQUIRED = 0x00000001
            ES_DISPLAY_REQUIRED = 0x00000002
            while self.running:
                ctypes.windll.kernel32.SetThreadExecutionState(
                    ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
                )
        elif sys.platform == "darwin":  # macOS
            while self.running:
                os.system("caffeinate -s")
    
    def stop(self):
        self.running = False
        sys.exit(0)

def create_gui(nosleep_instance):
    """Create a simple GUI to stop the program"""
    root = tk.Tk()
    root.title("No Sleep")

    tk.Label(root, text="Your computer will not sleep while this is running.", padx=20, pady=10).pack()
    tk.Button(root, text="Stop Program", command=nosleep_instance.stop, bg="red", fg="white", padx=10, pady=5).pack()

    root.protocol("WM_DELETE_WINDOW", nosleep_instance.stop)  # Close program on window close
    root.mainloop()

if __name__ == "__main__":
    nosleep = NoSleep()
    create_gui(nosleep)
