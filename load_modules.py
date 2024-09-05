import json
from pathlib import Path
from colorama import just_fix_windows_console, Fore
import interactions


just_fix_windows_console()


def load_config():
    config_file = 'modules.json'
    with open(config_file, 'r') as f:
        return json.load(f)


def save_config(config):
    with open('modules.json', 'w') as f:
        json.dump(config, f, indent=4)


def update_config(module, status=True):
    _config = load_config()
    _config[module] = status
    save_config(_config)


def add_new_modules():
    _config = load_config()
    folder_path = Path('modules')
    files = [file for file in folder_path.iterdir() if file.name != '__pycache__']
    modules = [module.stem for module in files]
    new_modules = False
    for module in modules:
        if module not in _config:
            _config[module] = True
            new_modules = True
            print(f'[>>] Найден новый модуль: {Fore.GREEN}"{module}"{Fore.RESET}. Добавлен в конфигурацию JSON.')
    if new_modules:
        save_config(_config)
        print(f'[>>] Конфигурация JSON обновлена.')
    else:
        print(f'[>>] Новых модулей не найдено.')


def load_module(client: interactions.Client):
    _config = load_config()
    for module in _config:
        if _config.get(module, False):
            client.load_extension(f'modules.{module}')
            print(f'[>>]Загружен модуль: {Fore.CYAN}"{module}"{Fore.RESET}')
        else:
            print(f'[>>]Модуль {Fore.CYAN}"{module}"{Fore.RESET} отключен в конфигурации JSON.')


if __name__ == '__main__':
    pass