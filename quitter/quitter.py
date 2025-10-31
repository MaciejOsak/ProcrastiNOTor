import time
import psutil

from assertions import *
from constants import MINUTE
from exceptions_handling import *


ACTIVATED: bool = False

assets: dict
registered_running_time_wasters: list = []
rrtw_timers: list = []


def get_display() -> dict:

    root = tk.Tk()
    frame = tk.Frame(root, width=400, height=250)
    frame.grid()

    go_back_button = tk.Button(root, text="Go back", command=turn_quitter_off, width=50)
    go_back_button.grid(column=1, row=0)

    time_wasters_label = tk.Label(root, text="Please enter your main enemies below")
    time_wasters_label.grid(column=0, row=1)

    time_wasters_enter = tk.Entry(root)
    time_wasters_enter.grid(column=0, row=2)

    waster_minute_limit_label = tk.Label(root, text="Please enter maximum time of procrastination below")
    waster_minute_limit_label.grid(column=1, row=2)

    waster_minute_limit_enter = tk.Entry(root)
    waster_minute_limit_enter.grid(column=1, row=3)

    launching_button = tk.Button(root, text="Stop wasting time!", command=try_launch, width=50)
    launching_button.grid(column=0, row=3, columnspan=2, pady=20)

    incorrect_input_label = None
    incorrect_input_text: str = ""

    return {
        "root": root,
        "frame": frame,
        "labels": {
            "time_wasters_label": time_wasters_label,
            "waster_minute_limit_label": waster_minute_limit_label,
            "incorrect_input_label": incorrect_input_label
        },
        "enters": {
            "time_wasters_enter": time_wasters_enter,
            "waster_minute_limit_enter": waster_minute_limit_enter
        },
        "buttons": {
            "launching_button": launching_button
        },
        "values": {
            "incorrect_input_text": incorrect_input_text
        }
    }


def format_time_wasters(wasters: str):
    wasters = wasters.split(", ")
    for i in range(len(wasters)):
        if wasters[i][(len(wasters[i]) - 4):] != ".exe":
            wasters[i] = f"{wasters[i]}.exe"
    return wasters


def turn_quitter_off():
    global assets, ACTIVATED
    ACTIVATED = False
    assets["root"].destroy()


def try_launch():
    global assets

    time_wasters = assets["enters"]["time_wasters_enter"].get()
    waster_minute_limit = assets["enters"]["waster_minute_limit_enter"].get()

    try:
        assert_time_wasters(time_wasters)
        assert_minute_limit(waster_minute_limit)
    except ProcrastiNOTorErrors as exception:
        incorrect_input_label = get_error_label(exception, assets["root"])
        incorrect_input_label.grid(column=1, row=2)
    else:
        if assets["labels"]["incorrect_input_label"] is not None:
            assets["labels"]["incorrect_input_label"].grid_remove()
        time_wasters = format_time_wasters(time_wasters)
        assets["root"].destroy()
        run_app(time_wasters=time_wasters, maximum_time_waste=int(waster_minute_limit))


def run_app(time_wasters: list, maximum_time_waste: int = 30 * MINUTE):
    while True:
        for process in psutil.process_iter(["pid", "name", "username"]):
            if process.name() in time_wasters:
                if process.name() not in registered_running_time_wasters:
                    registered_running_time_wasters.append(process.name())
                    rrtw_timers.append(time.time())
                else:
                    if time.time() - rrtw_timers[registered_running_time_wasters.index(process.name())] > maximum_time_waste:

                        process.terminate()

                        popup = tk.Tk()

                        popup_label = tk.Label(popup, text="Get down to business already!", foreground="red")
                        popup_label.pack()

                        popup.mainloop()

        time.sleep(1)


def main():
    global assets, ACTIVATED

    assets = get_display()
    ACTIVATED = True
    assets["root"].mainloop()
    return


if __name__ == "__main__":
    main()
