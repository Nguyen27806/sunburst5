import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Sunburst Chart: Entrepreneurship → Field → Salary (Show % on All Levels)")

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

    # Group and count
    sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')

    # Tính % toàn bộ
    total = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

    # Gán nhãn có % cho tất cả các cấp
    sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
        sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
    ) + '%)'

    sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + ' (' + (
        sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
    ) + '%)'

    sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + ' (' + sunburst_data['Percentage'].astype(str) + '%)'

    # Tạo biểu đồ sunburst
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
        values='Percentage',
        color='Percentage',
        color_continuous_scale='RdBu',
        title='Entrepreneurship → Field → Starting Salary (All % Visible)'
    )

    fig.update_traces(maxdepth=2)

    # Hiển thị biểu đồ
    st.plotly_chart(fig)
