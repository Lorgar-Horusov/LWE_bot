import streamlit as st
import pandas as pd
from util.db_logic import ChatLogger

# Initialize the database logger
db = ChatLogger()

# Set title for the Streamlit app
st.title('Logs')

# Create a form for log retrieval
with st.form('logs_form'):
    table_name = st.selectbox('Select Table', ['deleted_messages', 'edited_messages'])
    server_id = 928238166341738536  # Replace with your actual server ID
    submitted = st.form_submit_button('Get Logs')

    # If the form is submitted, fetch and display the logs
    if submitted:
        try:
            # Retrieve logs from the database
            log_data = db.get_logs(table_name, server_id)

            # Convert logs to a DataFrame
            df = pd.DataFrame(log_data)

            # Check if the DataFrame is empty and display it
            if not df.empty:
                st.dataframe(df)
            else:
                st.warning('No logs found for the selected table and server ID.')
        except Exception as e:
            # Display an error message if something goes wrong
            st.error(f'An error occurred while fetching logs: {str(e)}')
