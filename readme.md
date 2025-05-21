# LWE_Bot

- **Project Name**: legendary web enforcer
- **Version**: 0.3.5
- **Author**: Lorgar Horusov

---
<details><summary>Table of Contents</summary>

- [Features](#Features)
- [Technologies Used](#Technologies-Used)
- [1. Introduction](#Introduction)
  - [1.1 Project Purpose](#Introduction)
  - [1.2 Scope](#Introduction)
- [2. General Information](#General-Information)
  - [2.1 System Description](#General-Information)
  - [2.2 Main Functions](#General-Information)
- [3. Module Descriptions](#Module-Descriptions)
  - [3.1 `book_search` Module](#Module-Descriptions)
  - [3.2 `chat_gpt` Module](#Module-Descriptions)
  - [3.3 `e621_search` Module](#Module-Descriptions)
  - [3.4 `img_gen` Module](#Module-Descriptions)
  - [3.5 `logger` Module](#Module-Descriptions)
  - [3.6 `manga` Module](#Module-Descriptions)
  - [3.7 `music` Module](#Module-Descriptions)
  - [3.8 `wishper` Module](#Module-Descriptions)
- [4. Configuration and Installation](#Configuration-and-Installation)
- [5. Configuration Details](#Configuration-Details)
  - [API Keys and Tokens (`tokken_setting.py`)](#Configuration-Details)
  - [Lavalink Audio Server (`application.yml`)](#Configuration-Details)
  - [Module-Specific Settings (`modules.yaml`)](#Configuration-Details)
- [6. User Guide](#User-Guide)
- [7. Technical Requirements](#Technical-Requirements)
- [8. Conclusion](#Conclusion)
- [9. Contributing](#Contributing)
- [10. License](#License)
</details>

-----

# Features <a id='Features'></a>

* **Content Search**: Find books, manga, and images across various platforms (leveraging `book_search`, `manga`, and `e621_search` modules).
* **Content Generation**: Integrate with AI for text and image generation (utilizing `chat_gpt` and `img_gen` modules).
* **Music Streaming**: Stream music from platforms like YouTube (via the `music` module).
* **Logging**: Record bot events and display them in a web interface (handled by the `logger` module).
* **Web Management Interface**: User-friendly interface for configuring bot settings and managing modules.
* **Modular Design**: The system consists of various modules that can be activated or deactivated based on user needs, providing flexibility.
* **Speech Recognition**: Convert speech to text (using the `wishper` module, based on Whisper).

-----

# Technologies Used <a id='Technologies-Used'></a>

* Python 3.10+
* discord-py-interactions
* OpenAI API
* aiohttp
* Lavalink
* interactions-lavalink
* beautifulsoup4
* requests
* rich
* streamlit
* validators
* bs4
* playwright
* pandas
* PyYAML

-----

# 1. Introduction <a id='Introduction'></a>

### 1.1 Project Purpose

The project is a multifunctional bot designed for integration with chats or messengers. The bot
allows searching for books, manga, and images, generating text and images, playing music, and managing
event logging.

### 1.2 Scope

The system is intended for use in chats and messengers where automation of information search and
content generation, as well as multimedia functions, are required.

-----

# 2. General Information <a id='General-Information'></a>

### 2.1 System Description

The system consists of a Python-based bot that interacts with various modules to perform a wide
range of tasks. Each module provides specific functionality and can be activated or deactivated
depending on the needs.

### 2.2 Main Functions

- **Content Search**: Search for books, manga, images, and information on various platforms.
- **Content Generation**: Integration with AI for text and visual content generation.
- **Music Streaming**: Streaming music playback.
- **Logging**: Recording events and displaying them in a web interface.
- **Web Management Interface**: A convenient interface for configuring bot parameters.

-----

# 3. Module Descriptions <a id='Module-Descriptions'></a>

### 3.1 `book_search` Module

- **Purpose**: Performs book searches, possibly using the Flibusta API.
- **Functionality**: Allows finding and displaying book data such as description, author, genre, and rating.

### 3.2 `chat_gpt` Module

- **Purpose**: Integration with ChatGPT for generating text responses.
- **Functionality**: Creates conversational responses, simulating live communication.

### 3.3 `e621_search` Module

- **Purpose**: Searches for images on the e621 platform.
- **Functionality**: Allows searching and accessing specific images using the e621 API.

### 3.4 `img_gen` Module

- **Purpose**: Generates images.
- **Functionality**: Uses APIs or built-in algorithms to create images based on specified parameters.

### 3.5 `logger` Module

- **Purpose**: Maintains logs of bot actions.
- **Functionality**: Records and displays the history of bot operations for monitoring and analysis.

### 3.6 `manga` Module

- **Purpose**: Searches for manga data.
- **Functionality**: Allows searching and displaying information about manga, including title, description, and rating.

### 3.7 `music` Module

- **Purpose**: Streams music.
- **Functionality**: Supports streaming playback from platforms like YouTube.

### 3.8 `wishper` Module

- **Purpose**: Speech recognition.
- **Functionality**: Converts speech to text using the Whisper system.

-----

# 4. Configuration and Installation <a id='Configuration-and-Installation'></a>

**Prerequisites:**
- **Python 3.10+**: Ensure Python 3.10 or a newer version is installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: You'll need Git to clone the repository. Instructions for installing Git can be found at [git-scm.com](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- **Java Development Kit (JDK)** (for Lavalink): If you plan to use music features, a JDK (version 11 or newer, OpenJDK is recommended) is required to run Lavalink.

**Steps:**

1.  **Clone the Repository:**
    Open your terminal or command prompt and run:
    ```shell
    git clone <repository_url> 
    cd <repository_name> 
    ```
    (Replace `<repository_url>` with the actual URL of the Git repository and `<repository_name>` with the directory name created by git clone, usually the project name).

2.  **Create and Activate a Virtual Environment:**
    This isolates project dependencies.
    ```shell
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```
    *Note: On some systems, `python` might be `py` or `python3`. Use the command that points to your Python 3.10+ installation.*

3.  **Install Dependencies:**
    Install all required Python packages using pip and the `requirements.txt` file:
    ```shell
    pip install -r requirements.txt
    ```

4.  **Set Up Configuration:**
    Refer to the "[5. Configuration Details](#Configuration-Details)" section that follows. This is crucial for API keys, Lavalink settings (if used), and module configurations. You might need to run the bot once (Step 6) to be prompted for initial token setup if `tokken_setting.py` is used for this purpose.

5.  **Initialize Lavalink Server (Optional - for Music Functionality):**
    If you intend to use music streaming features:
    a.  Download the latest `Lavalink.jar` from [Lavalink's GitHub Releases](https://github.com/lavalink-devs/Lavalink/releases).
    b.  Create a directory for Lavalink (e.g., `~/lavalink/` or `C:\lavalink\`).
    c.  Place the downloaded `Lavalink.jar` into this directory.
    d.  Create or copy an `application.yml` file into the same directory as `Lavalink.jar`. Configure this file as detailed in the "[Lavalink Audio Server (`application.yml`)](#Configuration-Details)" part of the "5. Configuration Details" section.
    e.  Run Lavalink from its directory:
        ```shell
        java -jar Lavalink.jar
        ```
        Keep this terminal window open while Lavalink is in use.

6.  **Start the Bot:**
    Use the provided scripts to run the bot. These scripts typically execute the main Python file (e.g., `main.py` or `bot.py`).
    -   **Linux / macOS:**
        ```shell
        chmod +x start_linux.sh  # Ensure the script is executable (run once)
        ./start_linux.sh
        ```
    -   **Windows:**
        ```shell
        start_windows.bat
        ```
-----

# 5. Configuration Details <a id='Configuration-Details'></a>

Proper configuration is essential for the bot to function correctly. Below are the key configuration files and settings:

### API Keys and Tokens (`tokken_setting.py`)

API keys for various services integrated with the bot (like Discord and Naga AI/OpenAI) are managed through `tokken_setting.py`.
This script typically uses the `keyring` library to securely store and retrieve your tokens.
When you first run the bot or a module requiring a specific token, you might be prompted to enter it via the console.
- **Discord Token**: `discord_token()` function retrieves or prompts for the Discord bot token.
- **Naga AI/OpenAI Token**: `naga_ai_token()` function retrieves or prompts for the AI service token.
You can also use `set_discord_token(token)` and `set_naga_ai_token(token)` functions within a Python environment or by modifying the script if you need to update them manually, though using the prompts is the recommended way for initial setup.

### Lavalink Audio Server (`application.yml`)

The Lavalink server, used for music streaming capabilities, is configured via the `application.yml` file. This file is typically located in the same directory as your Lavalink server executable or configured to be loaded by it.
Key settings to pay attention to:
- `server.port`: The port on which Lavalink will listen (e.g., `43421`).
- `server.address`: The network address Lavalink will bind to (e.g., `127.0.0.1` for localhost).
- `lavalink.server.password`: The password clients (like this bot) will use to connect to Lavalink. Ensure this matches the password configured in the bot's music module settings if applicable.
- `lavalink.plugins`: This section allows you to define and configure Lavalink plugins, such as the YouTube plugin (`dev.lavalink.youtube:youtube-plugin`).
- `lavalink.server.sources`: Booleans to enable or disable various audio sources like YouTube, Bandcamp, Soundcloud, etc. Note that the default YouTube source is deprecated in favor of the plugin.
- `logging.level.root` and `logging.level.lavalink`: Configure the logging verbosity for Lavalink.

Ensure your Lavalink server is running and accessible with the settings defined in this file for music functionality to work.

### Module-Specific Settings (`modules.yaml`)

The `modules.yaml` file controls the activation and specific parameters for various bot modules. This allows you to customize the bot's behavior and features.
Example configurable parameters include:
- `enabled`: (e.g., `true` or `false`) for each module to turn it on or off.
- `default_search_count`: For modules like `book_search` and `manga`, this sets the default number of results to return.
- `max_tokens` and `model`: For the `chat_gpt` module, these control the AI's response length and the model used.
- `NSFW_filter`: For the `img_gen` module, to enable or disable NSFW content filtering.
- `time_to_delete`: For modules like `temp_channels` and `reports`.
- `sensitivity`, `message_limit`, `time_limit`, `whitelist`: For the `guard` module to configure its moderation behavior.

Review and adjust the settings in `modules.yaml` according to your preferences and the features you intend to use.

-----

# 6. User Guide <a id='User-Guide'></a>

The primary way to manage the bot's settings, enable/disable modules, and potentially view logs is through its web interface, built with Streamlit.

1.  **Ensure Prerequisites are Met:**
    - The bot's dependencies should be installed (see "4. Configuration and Installation").
    - For some WebUI features, the main bot might need to be running, especially if the UI interacts with the live bot state or its database. However, many configuration changes (like editing `modules.yaml` via the UI) can often be done with the bot offline.

2.  **Launch the Web Interface:**
    Navigate to the root directory of the project in your terminal (the directory containing the `webUI.py` file). Run the following command:
    ```shell
    streamlit run webUI.py
    ```

3.  **Access the Web Interface in Your Browser:**
    Once the command is executed, Streamlit will typically start a local web server. It should automatically open the WebUI in your default web browser.
    If it doesn't, the console output will display the local URL. This is usually:
    `http://localhost:8501`
    Copy and paste this URL into your browser's address bar.

4.  **Using the Web Interface:**
    The web interface is designed to be intuitive. You'll typically find options to:
    -   **Manage Modules:** Enable or disable different bot functionalities (e.g., `book_search`, `music`, `chat_gpt`).
    -   **Configure Module Settings:** Adjust parameters for active modules, such as default search counts, AI model preferences, NSFW filters, etc. These settings are often saved to `modules.yaml` or a similar configuration file.
    -   **API Key Management:** Some UIs might offer fields to input or update API keys, which would then be stored in `tokken_setting.py` or a related configuration.
    -   **View Logs:** If the `logger` module is integrated into the WebUI, you might be able to view recent bot activity or error messages.
    -   **System Status:** Potentially view the status of different components, like Lavalink connectivity.

    Navigate through the different sections or pages of the WebUI. Changes made in the UI that affect configuration files usually require a bot restart to take effect, unless the bot is designed to dynamically reload such configurations.

-----

# 7. Technical Requirements <a id='Technical-Requirements'></a>

- **Operating System**: Windows 10, Linux
- **Programming Language**: Python 3.10+
- **Dependencies**: Listed in `requirements.txt`

-----

# 8. Conclusion <a id='Conclusion'></a>

The project provides a wide range of tools for automating content search and generation in chats. Modules can be
adapted to specific tasks, making the bot a versatile tool for integration with messengers.

-----

# 9. Contributing <a id='Contributing'></a>

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
    or
    ```bash
    git checkout -b bugfix/issue-number
    ```
3.  **Make your changes** and commit them with clear and descriptive messages.
4.  **Push your changes** to your forked repository.
5.  **Create a Pull Request** to the `main` branch of the original repository.

Please ensure your code adheres to the project's coding style and includes tests if applicable.

-----

# 10. License <a id='License'></a>

This project is currently not licensed. Consider adding an open-source license like the [MIT License](https://opensource.org/licenses/MIT) to define how others can use, modify, and distribute your code.
If you choose to add a license, place the text in a `LICENSE` or `LICENSE.md` file in the root of the repository and update this section to link to it. For example:

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
