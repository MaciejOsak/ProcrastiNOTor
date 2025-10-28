import tkinter as ttk

from exceptions import *


def get_error_label(error: ProcrastiNOTorError, root: ttk.Tk):
    return ttk.Label(root, text=error.__cause__, foreground="red")
