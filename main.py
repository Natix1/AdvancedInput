from scripts.getkey import getkey
from scripts.capsLock import is_Capslock_On
import os
import time
import threading

terminal_width = os.get_terminal_size().columns

# llprint - low-level-print. got that name because you need to manually put newline
def llprint(passed):
    print(passed, end="", flush=True)

def resetLine():
    llprint(f"\r{' ' * terminal_width}\r")

def refresh(raw, prefix):
    resetLine()
    full = f"{prefix}{raw}"
    llprint(full)

def refreshpass(raw: str, prefix: str, disguiseas="x", capson=True):
    resetLine()
    rawlen = len(raw)
    hide = disguiseas * rawlen
    full = f"{prefix}{hide}"
    llprint(full)
    if capson:
        # Display Caps Lock status
        targetSpace = terminal_width - len(full) - 20
        resetLine()
        veryfull = f"{full}{' ' * targetSpace}↑ Caps lock on ↑"
        llprint(veryfull)

        # move cursor where it shall be
        targetPos = len(full)
        # actualPos = len(veryfull)

        targetllprint = veryfull[:targetPos]
        llprint(f"\r{targetllprint}")


def backend_uppercasepoll(event, state, prefix):
    while not event.is_set():
        caps = is_Capslock_On()
        state['capson'] = caps  # Directly update Caps Lock state
        
        # Refresh display with current password state
        if state['raw']:
            refreshpass(state['raw'], prefix, state['disguise'], state['capson'])
        time.sleep(0.1)  # Adjust the polling frequency as needed

def getpassword(prefix="", disguiseas="x"):
    raw = "" 
    llprint(prefix)
    
    # Shared state for Caps Lock status
    state = {'capson': False, 'raw': raw, 'disguise': disguiseas}
    event = threading.Event()
    
    # Start the backend thread to monitor Caps Lock
    backend = threading.Thread(target=backend_uppercasepoll, args=(event, state, prefix))
    backend.daemon = True
    backend.start()

    while True:
        key, keyname = getkey()

        if keyname == "backspace":
            if raw:  # Only modify raw if it's not empty
                raw = raw[:-1]  # Remove the last character
        elif keyname == "return":
            event.set()  # Signal the thread to stop when password is entered
            return raw  # Return raw input when Enter is pressed
        else:
            char = key.decode()  # Decode the character
            raw += char  # Add the new character to raw

        # Update state with the latest raw input for real-time updates
        state['raw'] = raw
        refreshpass(raw, prefix, disguiseas, state['capson'])  # Refresh the input line after every key press

if __name__ == "__main__":
    password = getpassword("Enter your password: ", "*")
    resetLine()
    llprint(f"Thank you, password logged.\n")
