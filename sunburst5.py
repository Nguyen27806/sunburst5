import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Title
st.title("Sunburst Chart: Entrepreneurship → Field → Salary (with % for Yes/No)")

# Upload file
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

    # Total for percentage
    total_root = sunburst_data['Count'].sum()

    # Tính % cho từng nhóm Yes/No
    root_percent = sunburst_data.groupby('Entrepreneurship')['Count'].sum().reset_index()
    root_percent['Percent'] = (root_percent['Count'] / total_root * 100).round(1).astype(str) + '%'

    # Gộp vào label mới
    label_map = dict(zip(root_percent['Entrepreneurship'], root_percent['Entrepreneurship'] + ' (' + root_percent['Percent'] + ')'))
    sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'].map(label_map)

    # Color theo Salary_Group
    salary_color_map = {
        '<30K': '#1f77b4',
        '30K–50K': '#aec7e8',
        '50K–70K': '#ffbb78',
        '70K+': '#d62728'
    }

    # Vẽ sunburst với nhãn đã thêm %
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_of_Study', 'Salary_Group'],
        values='Count',
        color='Salary_Group',
        color_discrete_map=salary_color_map,
        title='Entrepreneurship → Field → Salary (with % at Root Level)'
    )

    fig.update_traces(maxdepth=2)

    st.plotly_chart(fig)
