import streamlit as st
import importlib
import main
from load_modules import load_config, save_config

# Установим заголовок страницы
st.title('Настройки модулей бота')

# Загружаем текущую конфигурацию модулей
module_config = load_config()

# Проходим по всем модулям в конфигурации и создаем интерфейс
for module, config in module_config.items():
    with st.expander(f"Настройки для {module}"):
        # Чекбокс для включения/выключения модуля
        new_status = st.checkbox(f"Включить {module}", value=config['enabled'])
        module_config[module]['enabled'] = new_status

        # Динамически создаем поля для параметров модуля
        for param, value in config.items():
            if param != 'enabled':  # Игнорируем поле 'enabled', так как оно уже обработано
                if isinstance(value, bool):
                    # Для boolean параметров отображаем checkbox
                    new_value = st.checkbox(f"{param} для {module}", value=value)
                elif isinstance(value, int):
                    # Для числовых параметров отображаем number_input
                    new_value = st.number_input(f"{param} для {module}", value=value, min_value=1)
                elif isinstance(value, str):
                    # Для строковых параметров отображаем text_input
                    new_value = st.text_input(f"{param} для {module}", value=value)
                else:
                    new_value = value  # Если тип не распознан, просто оставляем значение

                # Обновляем значение в конфигурации
                module_config[module][param] = new_value

# Кнопка для сохранения настроек
if st.button('Сохранить настройки'):
    save_config(module_config)  # Сохраняем конфигурацию в файл
    importlib.reload(main)  # Перезагружаем бота
    st.success('Настройки успешно обновлены!')

    # Перезапуск бота
    main.start()
