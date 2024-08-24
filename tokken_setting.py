import keyring


def discord_token() -> str:
    if keyring.get_password('discord_bot', 'token') is None:
        token = input('Enter your Discord bot token: ')
        keyring.set_password('discord_bot', 'token', token)
    token = keyring.get_password('discord_bot', 'token')
    return token


def naga_ai_token() -> str:
    if keyring.get_password('discord_bot', 'token_chatGPT') is None:
        token = input('Enter your Naga AI token: ')
        keyring.set_password('discord_bot', 'token_chatGPT', token)
    token = keyring.get_password('discord_bot', 'token_chatGPT')
    return token


def set_discord_token(token) -> None:
    keyring.set_password('discord_bot', 'token', token)
    print('New Discord bot token set')


def set_naga_ai_token(token) -> None:
    keyring.set_password('discord_bot', 'token_chatGPT', token)
    print('New Naga AI token set')
