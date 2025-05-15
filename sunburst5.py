import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sunburst Chart: Màu Theo Phần Trăm (Tất cả khối, có Yes/No)")

uploaded_file = st.file_uploader("Upload the Excel file", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name='education_career_success')

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

    # Group
    sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
    total = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

    # Labels
    sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
        sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
    ) + '%)'

    sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + (
        sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
    ) + '%'

    sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

    # 🎯 Dùng Count để giữ cấu trúc, dùng Percentage để tô màu
    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
        values='Count',  # dùng count để node cha có giá trị
        color='Percentage',
        color_continuous_scale='RdBu',
        title='Sunburst Chart: Màu theo phần trăm (Yes/No cũng đổi màu)'
    )

    fig.update_coloraxes(cmin=0, cmax=100, colorbar_title="Percentage (%)")
    fig.update_traces(maxdepth=1, branchvalues="total", reversescale=True)

    st.plotly_chart(fig)
