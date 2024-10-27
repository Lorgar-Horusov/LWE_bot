import yaml
from pathlib import Path
from colorama import just_fix_windows_console, Fore
import interactions

just_fix_windows_console()


def load_config():
    config_file = 'modules.yaml'
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def save_config(config):
    with open('modules.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


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
            print(
                f'{Fore.BLUE}[>>]{Fore.GREEN} Найден новый модуль: {Fore.CYAN}"{module}"{Fore.GREEN}. Добавлен в конфигурацию YAML.{Fore.RESET}')
    if new_modules:
        save_config(_config)
        print(f'{Fore.BLUE}[>>]{Fore.GREEN}Конфигурация YAML обновлена.{Fore.RESET}')
    else:
        print(f'{Fore.BLUE}[>>]{Fore.GREEN}Новых модулей не найдено.{Fore.RESET}')


def load_module(client: interactions.Client):
    _config = load_config()
    for module in _config:
        if _config.get(module, False):
            client.load_extension(f'modules.{module}')
            print(f'{Fore.BLUE}[>>]{Fore.GREEN} Загружен модуль: {Fore.CYAN}"{module}"{Fore.RESET}')
        else:
            print(
                f'{Fore.BLUE}[>>]{Fore.RED} Модуль: {Fore.CYAN}"{module}"{Fore.RED} отключен в конфигурациях {Fore.RESET}')


def test_load() -> None:
    _config = load_config()
    for module in _config:
        if _config.get(module, False):
            print(f'{Fore.BLUE}[>>]{Fore.GREEN} Загружен модуль: {Fore.CYAN}"{module}"{Fore.RESET}')
        else:
            print(
                f'{Fore.BLUE}[>>]{Fore.RED} Модуль: {Fore.CYAN}"{module}"{Fore.RED} отключен в конфигурации YAML. {Fore.RESET}')


if __name__ == '__main__':
    add_new_modules()
