import streamlit as st

st.title('LWE bot dashboard')
st.page_link('webUI.py',  label='home', icon='🏠')
st.page_link('pages/module_web_UI.py',  label='module setting', icon='⚙️')
st.page_link('pages/setting_API.py',  label='API setting', icon='⚙️')