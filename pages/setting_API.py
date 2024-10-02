import streamlit as st
import keyring

# Инициализация переменных состояния для каждого API
if 'discord_saved' not in st.session_state:
    st.session_state['discord_saved'] = False
if 'naga_ai_saved' not in st.session_state:
    st.session_state['naga_ai_saved'] = False
if 'e621_login_saved' not in st.session_state:
    st.session_state['e621_login_saved'] = False
if 'e621_api_key_saved' not in st.session_state:
    st.session_state['e621_api_key_saved'] = False


# Функция для отображения сообщений об успешном сохранении
def display_success_message(service_name):
    st.success(f"{service_name} API key saved successfully!")


# Функция для создания полей ввода с кнопками
def create_api_input(service_name, key_name, value, password=False):
    st.text_input(label=service_name,
                  key=key_name,
                  value=value,
                  type="password" if password else "default"
                  )


def create_save_button(key, service_name, saved_state_key):
    if st.button("Save", key=key):
        st.session_state[saved_state_key] = True
        display_success_message(service_name)


st.title("API Settings")

col1, col2, col3 = st.columns(3)

# Discord API Settings
with col1:
    st.header("Discord")
    st.image("assets/discord-mark-blue.png", width=50,  use_column_width=False)
    st.markdown("**Please enter your Discord API key.**")
    st.markdown(":gray[_If you don't have one, you'll need to obtain it from the Discord Developer Portal."
                " You can create an application and obtain your API key by following this link:"
                " [Discord Developer Portal](https://discord.com/developers/applications)_]")
    create_api_input("api key", "api_key", keyring.get_password('discord_bot', 'token'), password=True)
    create_save_button("discord_api_token", "Discord", "discord_saved")

# Naga AI API Settings
with col2:
    st.header("Naga AI")
    st.image("assets/naga.png", width=50, use_column_width=False)
    st.markdown("**Please enter your Naga AI token.**")
    st.markdown(":gray[_You can obtain your token by signing up for a free [NagaAI](https://naga.ac/)_]")
    create_api_input("token", "naga_ai_token", keyring.get_password('discord_bot', 'token_chatGPT'), password=True)
    create_save_button("naga_ai_token_save", "Naga AI", "naga_ai_saved")

# e621 API Settings
with col3:
    st.header("e621")
    st.image("assets/e621_logo.png", width=50, use_column_width=False)
    st.markdown("**Please enter your e621 Login and API key.**")
    st.markdown(":gray[_You can obtain your API and Login key by following this link: [e621](https://e621.net/)_]")
    create_api_input("Login", "e621_login", keyring.get_password('e621', 'username'))
    create_save_button("e621_login_save", "e621 Login", "e621_login_saved")
    create_api_input("API key", "e621_api_key", keyring.get_password('e621', 'api_key'), password=True)
    create_save_button("e621_api_key_save", "e621 API key", "e621_api_key_saved")
