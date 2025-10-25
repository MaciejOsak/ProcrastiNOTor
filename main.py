import time
import psutil
import sys
import winreg
import os
import xml.etree.ElementTree as ET

from tkinter import *
from tkinter import ttk


MINUTE: int = 60
METADATA_DOC = ET.parse("metadata/meta.xml")
META = METADATA_DOC.getroot()

registered_running_time_wasters: list = []
rrtw_timers: list = []

def run_app(time_wasters: list, maximum_time_waste: int = 30 * MINUTE):
    global root
    while True:
        for process in psutil.process_iter(["pid", "name", "username"]):
            if process.name() in time_wasters:
                if process.name() not in registered_running_time_wasters:
                    registered_running_time_wasters.append(process.name())
                    rrtw_timers.append(time.time())
                else:
                    if time.time() - rrtw_timers[registered_running_time_wasters.index(process.name())] > maximum_time_waste:

                        process.terminate()

                        popup = Tk()
                        popup_frame = ttk.Frame(width=150, height=100)

                        popup_label = ttk.Label(popup, text="Get down to business already!", foreground="red")
                        popup_label.pack()

                        popup.mainloop()

        time.sleep(1 * MINUTE)


def add_to_startup():

    cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}"'

    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

    with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
        winreg.SetValueEx(registry_key, "ProcrastiNOTor", 0, winreg.REG_SZ, cmd)
        winreg.CloseKey(key)

    META[0].text = "TRUE"
    METADATA_DOC.write("metadata/meta.xml")


def assert_time_wasters(value):
    global improper_time_wasters_error
    if value == "":
        improper_time_wasters_error = ttk.Label(root, text="You must provide a list of time wasters.",
                                                foreground="red")
        improper_time_wasters_error.grid(column=1, row=3)
        return False
    if len(value.split(", ")) > 100:
        improper_time_wasters_error = ttk.Label(root, text="Time wasters count must be less than/equal to 100.",
                                                foreground="red")
        improper_time_wasters_error.grid(column=1, row=3)
        return False
    improper_time_wasters_error.grid_remove()
    return True


def assert_minute_limit(value):
    global improper_minute_limit_error
    try:
        int(value)
    except (ValueError, TypeError):
        improper_minute_limit_error = ttk.Label(root, text="Minute limit must be a number.",
                                                foreground="red")
        improper_minute_limit_error.grid(column=1, row=2)
        return False
    if int(value) > 1440:
        improper_minute_limit_error = ttk.Label(root, text="Limit must be shorter than/equal to a day.",
                                                foreground="red")
        improper_minute_limit_error.grid(column=1, row=2)
        return False
    improper_minute_limit_error.grid_remove()
    return True


def format_time_wasters(wasters: str):
    wasters = wasters.split(", ")
    for i in range(len(wasters)):
        if wasters[i][(len(wasters[i]) - 4):] != ".exe":
            wasters[i] = f"{wasters[i]}.exe"
    return wasters


def try_launch():

    time_wasters = time_wasters_enter.get()
    waster_minute_limit = waster_minute_limit_enter.get()

    if assert_time_wasters(time_wasters) and assert_minute_limit(waster_minute_limit):
        time_wasters = format_time_wasters(time_wasters)
        root.destroy()
        run_app(time_wasters=time_wasters, maximum_time_waste=int(waster_minute_limit))


if META[0].text == "FALSE":
    add_to_startup()


root = Tk()
frame = ttk.Frame(root, width=400, height=250)
frame.grid()


time_wasters_label = ttk.Label(root, text="Please enter your main enemies below")
time_wasters_label.grid(column=0, row=0)

time_wasters_enter = ttk.Entry(root)
time_wasters_enter.grid(column=0, row=1)


waster_minute_limit_label = ttk.Label(root, text="Please enter maximum time of procrastination below")
waster_minute_limit_label.grid(column=1, row=0)

waster_minute_limit_enter = ttk.Entry(root)
waster_minute_limit_enter.grid(column=1, row=1)


launching_button = ttk.Button(root, text="Stop wasting time!", command=try_launch, width=50)
launching_button.grid(column=0, row=2, columnspan=2, pady=20)

improper_minute_limit_error = None
improper_time_wasters_error = None

root.mainloop()
