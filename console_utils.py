import os
import ctypes
from pathlib import Path
from datetime import datetime

OUT_FILENAME = datetime.now().strftime('%d_%m_%Y__%H_%M') + '.txt'
TODAY_DATE = datetime.today().strftime('%d/%m/%Y')

def quickedit(enabled: bool = True) -> None:
    """Enable or disable quick edit mode to prevent system hangs in the console."""
    kernel32 = ctypes.windll.kernel32
    quick_edit_mode = 0x40 if enabled else 0x00
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | quick_edit_mode | 0x100)
    print(f"Console Quick Edit {'Enabled' if enabled else 'Disabled'}")

def clearscreen(numlines: int = 100) -> None:
    """Clear the console based on OS type."""
    command = 'clear' if os.name == "posix" else 'CLS'
    os.system(command)

def draw(content: str) -> None:
    """Prints content to the console and saves it to an output file."""
    path = Path(os.getcwd()) / 'output' / OUT_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf8") as file:
        file.write(content + '\n')
    print(content)
