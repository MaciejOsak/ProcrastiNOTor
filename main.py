import sys
import winreg
import os
import xml.etree.ElementTree as ET


METADATA_DOC = ET.parse("metadata/meta.xml")
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


if META[0].text == "FALSE":
    add_to_startup()
