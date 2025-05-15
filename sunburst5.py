import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Sunburst Chart: Entrepreneurship → Field → Salary (All Levels Colored by %)")

# Upload file
uploaded_file = st.file_uploader("Upload the Excel file", type="xlsx")

if uploaded_file is not None:
    # Load data
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

    # Tổng tất cả
    total = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

    # Tính % cho từng node cha (Yes/No + Field)
    root_percent = sunburst_data.groupby('Entrepreneurship')['Count'].sum().reset_index()
    root_percent['Root_Percentage'] = (root_percent['Count'] / total * 100).round(2)

    field_percent = sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].sum().reset_index()
    field_percent['Field_Percentage'] = (field_percent['Count'] / total * 100).round(2)

    # Merge vào dataframe
    sunburst_data = sunburst_data.merge(root_percent[['Entrepreneurship', 'Root_Percentage']], on='Entrepreneurship')
    sunburst_data = sunburst_data.merge(field_percent, on=['Entrepreneurship', 'Field_of_Study'])

    # Label
    sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + sunburst_data['Root_Percentage'].astype(str) + '%)'
    sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + sunburst_data['Field_Percentage'].astype(str) + '%'
    sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

    # Gán color thủ công (ưu tiên leaf → field → root)
    sunburst_data['Color_Value'] = sunburst_data['Percentage']

    # Tạo sunburst
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
        values='Percentage',
        color='Color_Value',
        color_continuous_scale='RdBu',
        title='Entrepreneurship → Field → Salary (All Colored by Percentage)'
    )

    fig.update_coloraxes(cmin=0, cmax=100, colorbar_title="Percentage (%)")
    fig.update_traces(maxdepth=2)

    st.plotly_chart(fig)
