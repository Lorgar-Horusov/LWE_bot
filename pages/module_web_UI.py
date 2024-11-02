import streamlit as st
import importlib
import main
from load_modules import load_config, save_config
import pandas as pd

st.title('Module Config')

module_config = load_config()

modules = []
status = []

for module, stat in module_config.items():
    modules.append(module)
    status.append(stat)

data_fr = pd.DataFrame({'Modules': modules, 'Status': status})

updated_data = st.data_editor(data_fr, use_container_width=True, hide_index=True, disabled=['Modules'])

if st.button('Reload Bot', disabled=False):
    updated_config = {row['Modules']: row['Status'] for _, row in updated_data.iterrows()}
    save_config(updated_config)
    importlib.reload(main)
    st.info('Bot is reloading...')
    main.start()
