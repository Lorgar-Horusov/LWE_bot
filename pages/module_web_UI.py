import streamlit as st
import importlib
import main
from load_modules import load_config, save_config


st.title('Module config')
module_config = load_config()
updated_config = {}

for module, status in module_config.items():
    updated_config[module] = st.checkbox(f'Modules: {module}', value=status)

if st.button('Save'):
    save_config(updated_config)
    st.success('Config updated successfully!')

if st.button('Reload bot', disabled=False):
    importlib.reload(main)
    st.info('Bot is reloading...')
    # main.stop()
    main.start()