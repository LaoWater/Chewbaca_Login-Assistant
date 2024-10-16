import pygetwindow as gw
import win32process
import win32gui

# Function to get the PID of a window from its title by enumerating windows
def enum_window_callback(hwnd, result):
    # Get window title
    title = win32gui.GetWindowText(hwnd)
    # Check if the window title matches what we are looking for
    if "SQL Server Management Studio" in title and "rdiapp" not in title:
        # Get the process ID (PID) of the window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        result.append((title, pid))

# Iterate through all open window titles and find their PIDs
windows = []
win32gui.EnumWindows(enum_window_callback, windows)

# Print the results
for window_title, pid in windows:
    print(f"Window Title: {window_title}, PID: {pid}")
