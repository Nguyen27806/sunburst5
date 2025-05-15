import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Sunburst Chart: Entrepreneurship → Field → Salary (Color by % and Show Root %)")

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

    # Group and count
    sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')

    # Tính tổng để chia phần trăm
    total_count = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total_count * 100).round(2)

    # Tính phần trăm gắn vào nhãn Entrepreneurship (Yes/No)
    root_percent = sunburst_data.groupby('Entrepreneurship')['Count'].sum().reset_index()
    root_percent['Percent'] = (root_percent['Count'] / total_count * 100).round(1).astype(str) + '%'
    label_map = dict(zip(root_percent['Entrepreneurship'], root_percent['Entrepreneurship'] + ' (' + root_percent['Percent'] + ')'))
    sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'].map(label_map)

    # Vẽ biểu đồ màu theo phần trăm
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_of_Study', 'Salary_Group'],
        values='Percentage',
        color='Percentage',
        color_continuous_scale='RdBu',
        title='Entrepreneurship → Field → Salary (by Percentage)'
    )

    # Ban đầu chỉ hiện vòng 1
    fig.update_traces(maxdepth=1)

    # Hiển thị biểu đồ
    st.plotly_chart(fig)
