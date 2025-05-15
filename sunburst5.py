import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Sunburst Chart: Entrepreneurship → Field → Salary (Full % Labels + Fixed Color Scale)")

# Upload file
uploaded_file = st.file_uploader("Upload the Excel file", type="xlsx")

if uploaded_file is not None:
    # Đọc dữ liệu
    df = pd.read_excel(uploaded_file, sheet_name='education_career_success')

    # Phân loại mức lương
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

    # Gom nhóm dữ liệu
    sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')

    # Tính phần trăm trên tổng
    total = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

    # ======= Gắn nhãn có phần trăm cho từng vòng ========

    # Vòng 1: Entrepreneurship (1 dòng)
    sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
        sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
    ) + '%)'

    # Vòng 2: Field (2 dòng)
    sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + (
        sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
    ) + '%'

    # Vòng 3: Salary_Group (2 dòng)
    sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

    # ======= Vẽ biểu đồ ========
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
        values='Percentage',
        color='Percentage',
        color_continuous_scale='RdBu',
        title='Entrepreneurship → Field → Starting Salary (with % Labels)'
    )

    # Cố định scale màu từ 0 đến 100
    fig.update_coloraxes(cmin=0, cmax=100, colorbar_title="Percentage (%)")

    # Ban đầu chỉ hiển thị vòng đầu
    fig.update_traces(maxdepth=1)

    # Hiển thị biểu đồ
    st.plotly_chart(fig)
