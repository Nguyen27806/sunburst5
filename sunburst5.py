import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Sunburst Chart: Entrepreneurship → Field → Starting Salary")

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

    # Group data
    sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')

    # Create sunburst chart with color scale
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship', 'Field_of_Study', 'Salary_Group'],
        values='Count',
        color='Count',  # use Count to apply color scale
        color_continuous_scale='RdBu',
        title='Entrepreneurship → Field → Starting Salary'
    )

    # Show only first level initially
    fig.update_traces(maxdepth=2)

    # Display the chart
    st.plotly_chart(fig)
