from pathlib import Path
from colorama import just_fix_windows_console, Fore
import interactions

just_fix_windows_console()

folder_path = Path('modules')
files = [file for file in folder_path.iterdir() if file.name != '__pycache__']
modules = [module.stem for module in files]


def load_module(client: interactions.Client):
    for module in modules:
        client.load_extension(f'modules.{module}')
        print(f'[>>]Загружен модуль: {Fore.CYAN}"{module}"{Fore.RESET}')
