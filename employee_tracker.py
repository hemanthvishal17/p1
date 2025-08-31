import streamlit as st
import pandas as pd

st.title("Employee Task Tracker and Analytics")

# Initialize session state DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Employee', 'Tasks Assigned', 'Tasks Completed'])

# Form to add or update employee data
with st.form("add_employee_form", clear_on_submit=True):
    st.subheader("Add / Update Employee Task Data")
    employee_name = st.text_input("Employee Name")
    tasks_assigned = st.number_input("Tasks Assigned", min_value=0, step=1)
    tasks_completed = st.number_input("Tasks Completed", min_value=0, step=1)
    submitted = st.form_submit_button("Add / Update Employee")

    if submitted:
        df = st.session_state.df
        if employee_name in df['Employee'].values:
            idx = df.index[df['Employee'] == employee_name][0]
            df.at[idx, 'Tasks Assigned'] = tasks_assigned
            df.at[idx, 'Tasks Completed'] = tasks_completed
            st.success(f"Updated data for {employee_name}")
        else:
            new_row = {'Employee': employee_name, 'Tasks Assigned': tasks_assigned, 'Tasks Completed': tasks_completed}
            st.session_state.df = df.append(new_row, ignore_index=True)
            st.success(f"Added new employee {employee_name}")

# Calculate success rate
def calculate_success_rate(row):
    if row['Tasks Assigned'] == 0:
        return 0
    return round((row['Tasks Completed'] / row['Tasks Assigned']) * 100, 1)

st.session_state.df['Success Rate (%)'] = st.session_state.df.apply(calculate_success_rate, axis=1)

st.subheader("Employee Success Rate Analytics")
st.table(st.session_state.df)

# Optionally allow downloading as CSV
csv = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Analytics Data as CSV",
    data=csv,
    file_name='employee_task_analytics.csv',
    mime='text/csv',
)
