
import os

# Command to check on/off on linux:
# xset -q | sed -n 's/^.*Caps Lock:\s*\(\S*\).*$/\1/p'
# above is from https://askubuntu.com/users/484187/mateo-de-mayo, thanks!

# Determine the operating system and import whats needed
OS = os.name
if OS == "NT":
    from win32api import GetKeyState # type: ignore
    from win32con import VK_CAPITAL  # type: ignore
    GetKeyState(VK_CAPITAL)
else:
    import subprocess

def is_Capslock_On():
    if OS == "NT":
        result = GetKeyState(VK_CAPITAL)
        if str(result) == "1":
            return True
        else:
            return False
    else:
        command = r"xset -q | sed -n 's/^.*Caps Lock:\s*\(\S*\).*$/\1/p'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result = str(result.stdout)
        result = result.lower().strip()
        if result == "on":
            return True
        else:
            return False