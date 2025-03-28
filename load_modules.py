import os

import yaml
from pathlib import Path

from rich.console import Console
import interactions
from art import tprint
from time import sleep
from random import randint

console = Console()

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
            console.print(f'[blue][>>>][green] Найден новый модуль:[cyan]\"{module}\"[/cyan]. Добавлен в конфигурацию YAML.')

    if new_modules:
        save_config(_config)  # Сохраняем изменения в конфигурации
        console.print(f'[blue][>>>][green] Конфигурация YAML обновлена.')
    else:
        console.print(f'[blue][=!=][yellow] Новых модулей не найдено.')


def load_module(client: interactions.Client):
    clear()
    _config = load_config()
    tprint("LWE-BOT", font="tarty1")
    with console.status("[bold]Loading", spinner='growVertical'):
        for module, settings in _config.items():
            if settings.get('enabled', False):
                client.load_extension(f'modules.{module}')
                console.print(f'[blue][>>>][green] Загружен модуль: [cyan]\"{module}"')
                for setting, value in settings.items():
                    if setting != "enabled":
                        console.print(f"[blue] |->| [yellow]{setting}: [cyan]{value}")
            else:
                console.print(f'[blue][=!=][red] Модуль: [cyan]\"{module}\"[red] отключен в конфигурациях')


def test_load() -> None:
    _config = load_config()
    with console.status("[bold]Loading", spinner='growVertical'):
        for module, settings in _config.items():
            if settings.get('enabled', False):
                console.print(f'[blue][>>>][green] Загружен модуль: [cyan]\"{module}\"')
                for setting, value in settings.items():
                    if setting != "enabled":
                        console.print(f"[blue] |->| [yellow]{setting}: [cyan]{value}")
                        sleep(randint(1, 3))
            else:
                console.print(f'[blue][=!=][red] Модуль: [cyan]\"{module}\"[red] отключен в конфигурациях')
                sleep(randint(1, 3))


if __name__ == '__main__':
    add_new_modules()
