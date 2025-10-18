from tkinter import *
from tkinter import ttk
import time
import psutil


registered_running_time_wasters: list = []

rrtw_timers: list = []

minute: int = 60


def run_app(time_wasters: list, maximum_time_waste: int = 30 * minute):
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

        time.sleep(2)


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

time.sleep(10)

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
