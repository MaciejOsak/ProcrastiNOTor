import sys
import winreg
import os
import xml.etree.ElementTree as ElTr
import tkinter as tk


METADATA_DOC = ElTr.parse("metadata/meta.xml")
META = METADATA_DOC.getroot()


def add_to_startup():

    cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}"'

    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

    with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
        winreg.SetValueEx(registry_key, "ProcrastiNOTor", 0, winreg.REG_SZ, cmd)
        winreg.CloseKey(key)

    META[0].text = "TRUE"
    METADATA_DOC.write("metadata/meta.xml")


def get_startup_menu() -> dict:

    root = tk.Tk()
    frame = tk.Frame(root, width=root.winfo_screenwidth() / 2, height=root.winfo_screenheight() / 2)
    frame.grid(columnspan=2, rowspan=2)
    root.state("zoomed")

    app_choosing_label = tk.Label(text="Choose a functionality you want to use", width=200)
    app_choosing_label.grid(column=1, row=0)

    quitter_button = tk.Button(root, text="Quitter", command=launch_quitter, width=50)
    quitter_button.grid(column=1, row=1)

    return {
        "root": root,
        "frame": frame,
        "labels": {
            "app_choosing_label": app_choosing_label
        },
        "buttons": {
            "quitter_button": quitter_button
        }
    }


def launch_quitter():
    global assets
    from quitter import quitter

    quitter.main()
    assets["root"].withdraw()
    assets["root"].deiconify()


if META[0].text == "FALSE":
    add_to_startup()

assets: dict = {}

if __name__ == "__main__":
    assets = get_startup_menu()
    assets["root"].mainloop()
