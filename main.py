# main.py
from Presentation.home_screen import HomeScreen
import os, sys, re


# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def highlight(value, search_key):
    value_str = str(value)
    pattern = re.compile(re.escape(search_key), re.IGNORECASE)
    return pattern.sub(lambda m: f'\033[91m{m.group(0)}\033[0m', value_str)

if __name__ == "__main__":
    HomeScreen.display()
