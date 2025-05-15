import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Explore Starting Salary by Field and Entrepreneurship")

# Upload Excel file
uploaded_file = st.file_uploader("Upload the Excel file", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name='education_career_success')

    # Categorize salary
    def categorize_salary(salary):
        if salary < 30000:
            return '<30K'
        elif salary < 50000:
            return '30K–50K'
        elif salary < 70000:
            return '50K–70K'
        else:
            return '70K+'

    df['Salary_Group'] = df['Starting_Salary'].apply(categorize_salary)

    # Step 1: Select Field
    selected_field = st.selectbox("Choose a Field of Study", sorted(df['Field_of_Study'].unique()))

    # Filter for selected field
    filtered_df = df[df['Field_of_Study'] == selected_field]

    # Step 2: Select Entrepreneurship Option
    selected_entrepreneurship = st.selectbox(
        "Choose Entrepreneurship Status",
        sorted(filtered_df['Entrepreneurship'].unique())
    )

    # Filter again
    final_df = filtered_df[filtered_df['Entrepreneurship'] == selected_entrepreneurship]

    # Group data for sunburst (last layer only: Salary Group)
    sunburst_data = final_df.groupby(['Field_of_Study', 'Entrepreneurship', 'Salary_Group']).size().reset_index(name='Count')

    # Create sunburst chart (now show all 3 levels)
    fig = px.sunburst(
        sunburst_data,
        path=['Field_of_Study', 'Entrepreneurship', 'Salary_Group'],
        values='Count',
        title=f"{selected_field} → {selected_entrepreneurship} → Starting Salary"
    )

    st.plotly_chart(fig)
