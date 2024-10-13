from getkey import getkey
import os

terminal_width = os.get_terminal_size().columns

# This is the legacy version
# It was discontinued because i got a better idea:
# instead of interacting with the annoying terminal systems that are probably from the 90s
# how about we just use a carriage return every single time something changed
# so instead of doing all this weird shit below
# we clear the current line and then calculate what should it look like
# and not apply everything live


def low_print(string):
    print(string, end="", flush=True)

def reset_line():
    print(f"\r{' ' * terminal_width}\r", end="")

def back(full_string):
    if full_string:
        full_string = full_string[:-1]
        reset_line()
        return full_string
    return full_string

def base_input(prefix="", newline_after=True):
    full_string = ""
    prefix_length = len(prefix)
    print(prefix, end="", flush=True)

    while True:
        key, keyname = getkey()

        if keyname == "return":
            if newline_after:
                print()
            return full_string

        elif keyname == "backspace":
            full_string = back(full_string)
            reset_line()
            low_print(prefix)
            low_print(full_string)

        else:
            char = key.decode()
            full_string += char
            low_print(char)

if __name__ == "__main__":
    text = base_input("> ", False)
    reset_line()
    print("\rSaved!", flush=True)
