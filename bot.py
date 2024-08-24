import argparse
import tokken_setting
import os


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-DT", "--discord_token", help="Set your Discord bot token")
    parser.add_argument("-NT", "--nagaAI_token", help="Set your NagaAi token")
    parser.add_argument('-S', '--start', help="start bot", action='store_true')
    args = parser.parse_args()

    if args.discord_token:
        tokken_setting.set_discord_token(args.discord_token)
    elif args.nagaAI_token:
        tokken_setting.set_naga_ai_token(args.nagaAI_token)
    elif args.start:
        if os.name == 'posix':
            os.system('start_linux.sh')
        elif os.name == 'nt':
            os.system('start_windows.bat')
        else:
            print('Ты ебнутый что за у тебя система')


if __name__ == '__main__':
    main()
