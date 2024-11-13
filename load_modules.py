import os

import yaml
from pathlib import Path
from colorama import just_fix_windows_console, Fore
import interactions
from art import tprint

just_fix_windows_console()

DEFAULT_CONFIG = {
    'enabled': True,
    'default_search_count': 3,  # Пример настройки по умолчанию для модулей, которые поддерживают поиск
}

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_config():
    config_file = 'modules.yaml'
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config.get("modules", {})  # Возвращаем только содержимое modules


def save_config(config):
    with open('modules.yaml', 'w') as f:
        yaml.dump({"modules": config}, f, default_flow_style=False)


def update_config(module, setting, value):
    _config = load_config()
    if module not in _config:
        _config[module] = DEFAULT_CONFIG.copy()
    _config[module][setting] = value
    save_config(_config)


def add_new_modules():
    _config = load_config()
    folder_path = Path('modules')
    files = [file for file in folder_path.iterdir() if file.suffix == '.py' and file.name != '__pycache__']
    modules = [file.stem for file in files]
    new_modules = False

    for module in modules:
        if module not in _config:
            _config[module] = DEFAULT_CONFIG.copy()  # Добавляем новый модуль с настройками по умолчанию
            new_modules = True
            print(
                f'{Fore.BLUE}[>>]{Fore.GREEN} Найден новый модуль: {Fore.CYAN}"{module}"{Fore.GREEN}. Добавлен в конфигурацию YAML.{Fore.RESET}')

    if new_modules:
        save_config(_config)  # Сохраняем изменения в конфигурации
        print(f'{Fore.BLUE}[>>]{Fore.GREEN} Конфигурация YAML обновлена.{Fore.RESET}')
    else:
        print(f'{Fore.BLUE}[>>]{Fore.GREEN} Новых модулей не найдено.{Fore.RESET}')


def load_module(client: interactions.Client):
    clear()
    _config = load_config()
    tprint("LWE-BOT", font="tarty1")
    for module, settings in _config.items():
        if settings.get('enabled', False):
            client.load_extension(f'modules.{module}')
            print(f'{Fore.BLUE}[>>]{Fore.GREEN} Загружен модуль: {Fore.CYAN}"{module}"{Fore.RESET}')
            for setting, value in settings.items():
                if setting != "enabled":
                    print(f"{Fore.BLUE}  -> {Fore.YELLOW}{setting}: {Fore.CYAN}{value}{Fore.RESET}")
        else:
            print(
                f'{Fore.BLUE}[>>]{Fore.RED} Модуль: {Fore.CYAN}"{module}"{Fore.RED} отключен в конфигурациях {Fore.RESET}')


def test_load() -> None:
    _config = load_config()
    for module, settings in _config.items():
        if settings.get('enabled', False):
            print(f'{Fore.BLUE}[>>]{Fore.GREEN} Загружен модуль: {Fore.CYAN}"{module}"{Fore.RESET}')
            for setting, value in settings.items():
                if setting != "enabled":
                    print(f"{Fore.BLUE}  -> {Fore.YELLOW}{setting}: {Fore.CYAN}{value}{Fore.RESET}")
        else:
            print(
                f'{Fore.BLUE}[>>]{Fore.RED} Модуль: {Fore.CYAN}"{module}"{Fore.RED} отключен в конфигурации YAML. {Fore.RESET}')


if __name__ == '__main__':
    test_load()
