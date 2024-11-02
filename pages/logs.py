import streamlit as st
import pandas as pd
from util.db_logic import ChatLogger
import datetime

# Initialize the database logger
db = ChatLogger()

# Set title for the Streamlit app
st.title('Logs')
col1, col2 = st.columns(2)


def main():
    with col1:
        table_name = st.selectbox('Select Table', ['deleted_messages', 'edited_messages'])
        server_id = 928238166341738536  # Replace with your actual server ID
        # Retrieve logs from the database
        log_data = db.get_logs(table_name, server_id)

        # Define column names and display columns based on the selected table
        if table_name == 'deleted_messages':
            columns = ['id', 'autor', 'message', 'deletion_data', 'server_id']
            display_columns = ['autor', 'message', 'deletion_data']
            search_columns = ['autor', 'message']
            date_column = 'deletion_data'
        elif table_name == 'edited_messages':
            columns = ['id', 'autor', 'original_message', 'edited_message', 'edited_date', 'server_id']
            display_columns = ['autor', 'original_message', 'edited_message', 'edited_date']
            search_columns = ['autor', 'original_message', 'edited_message']
            date_column = 'edited_date'

        # Convert logs to a DataFrame with the specified columns
        df = pd.DataFrame(log_data, columns=columns)

    with col2:
        # Create input fields for dynamic searching
        search_name = st.text_input('Search by Author or Message:')
        today = datetime.datetime.now().date()  # Get today's date

        # Create a date range picker for filtering
        try:
            date_range = st.date_input(
                'Select Date Range',
                value=(today, today),
                max_value=today
            )
        except Exception:
            st.error("Please select a valid date range")
            return

        # Apply filters based on search inputs
        if search_name:
            # Create a mask to filter based on search name
            mask = df[search_columns[0]].astype(str).str.contains(search_name, case=False, na=False)
            for col in search_columns[1:]:
                mask |= df[col].astype(str).str.contains(search_name, case=False, na=False)
            df = df[mask]

        # Handle date filtering
        try:
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
            else:
                start_date = end_date = date_range

            if start_date and end_date:
                # Convert dates to datetime objects for comparison
                df[date_column] = pd.to_datetime(df[date_column])

                # Create datetime objects for start and end of day
                start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
                end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

                # Filter the DataFrame for dates within the specified range
                df = df[
                    (df[date_column] >= start_datetime) &
                    (df[date_column] <= end_datetime)
                    ]

                # Convert back to string format for display
                df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')

        except Exception:
            st.warning(f'Enter a date range:')
            return

        # Display the filtered logs
        try:
            # Select only the columns to display
            view_columns = df[display_columns]

            # Check if the DataFrame is empty and display it
            if not view_columns.empty:
                st.dataframe(view_columns)
            else:
                st.warning('No logs found for the selected criteria.')
        except Exception as e:
            st.error(f'An error occurred while displaying logs: {str(e)}')


if __name__ == '__main__':
    main()