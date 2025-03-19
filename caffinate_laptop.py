import ctypes
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

class NoSleep:
    def __init__(self, duration):
        self.running = True
        self.duration = duration * 60  # Convert minutes to seconds
        self.thread = threading.Thread(target=self.prevent_sleep, daemon=True)
        self.thread.start()

    def prevent_sleep(self):
        """Prevent system sleep on Windows or macOS for the specified duration"""
        end_time = time.time() + self.duration

        if os.name == "nt":  # Windows
            ES_CONTINUOUS = 0x80000000
            ES_SYSTEM_REQUIRED = 0x00000001
            ES_DISPLAY_REQUIRED = 0x00000002
            while self.running and time.time() < end_time:
                ctypes.windll.kernel32.SetThreadExecutionState(
                    ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
                )
                time.sleep(5)  # Check every 5 seconds
        elif sys.platform == "darwin":  # macOS
            while self.running and time.time() < end_time:
                os.system("caffeinate -s &")
                time.sleep(5)

        self.shutdown_system()

    def shutdown_system(self):
        """Closes all apps and shuts down the system"""
        if os.name == "nt":  # Windows
            os.system("taskkill /F /IM *")  # Close all apps
            time.sleep(3)
            os.system("shutdown /s /t 0")  # Shutdown immediately
        elif sys.platform == "darwin":  # macOS
            os.system("osascript -e 'tell application \"System Events\" to log out'")  # Log out first
            time.sleep(3)
            os.system("sudo shutdown -h now")  # Shutdown immediately

    def stop(self):
        """Stops the process"""
        self.running = False
        sys.exit(0)

def create_gui():
    """Create a GUI to get user input and start the NoSleep program"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get user input for duration
    duration = simpledialog.askinteger("Sleep Prevention", "Enter duration (in minutes):", minvalue=1, maxvalue=1440)
    if duration is None:
        return

    nosleep = NoSleep(duration)

    # Create a control window
    control_window = tk.Toplevel()
    control_window.title("No Sleep Active")

    tk.Label(control_window, text=f"Preventing sleep for {duration} minutes.", padx=20, pady=10).pack()
    tk.Button(control_window, text="Stop Program", command=nosleep.stop, bg="red", fg="white", padx=10, pady=5).pack()

    control_window.protocol("WM_DELETE_WINDOW", nosleep.stop)  # Stop when window is closed
    control_window.mainloop()

if __name__ == "__main__":
    create_gui()
