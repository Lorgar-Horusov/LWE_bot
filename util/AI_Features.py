from openai import OpenAI
import asyncio
import keyring
import tempfile
import io, os

CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
if CHAT_GPT_TOKEN is None:
    CHAT_GPT_TOKEN = input('Write Token: ')
    keyring.set_password('discord_bot', 'token_chatGPT', CHAT_GPT_TOKEN)
    CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
client = OpenAI(base_url='https://api.naga.ac/v1', api_key=CHAT_GPT_TOKEN)


async def chat_gpt(prompt: str):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content


async def speach_to_text(audio_data: io.BytesIO) -> str:
    audio_data.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
        temp_file.write(audio_data.read())
        temp_file.flush()  # Убедимся, что данные записаны в файл
        temp_file_name = temp_file.name  # Сохраняем имя файла
    try:
        with open(temp_file_name, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large",
                file=audio_file
            )
            print(transcription.text)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Удаляем временный файл
        os.remove(temp_file_name)
    text = transcription.text
    return text


async def main():
    await speach_to_text()


if __name__ == '__main__':
    asyncio.run(main())
