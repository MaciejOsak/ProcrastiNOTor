import tkinter as tk

from exceptions import *


def get_error_label(error: ProcrastiNOTorError, root: tk.Tk):
    return tk.Label(root, text=error.__cause__, foreground="red")
