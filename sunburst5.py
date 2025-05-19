import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("🌞 Sunburst Chart – Salary, Field, and Entrepreneurship")

# Upload file
uploaded_file = st.file_uploader("📤 Upload the Excel file", type="xlsx")

# Color mode selection
color_mode = st.radio("🎨 Choose color mode:", ("Color by Salary Group", "Color by Percentage"))

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name='education_career_success')
    except Exception as e:
        st.error(f"❌ Error loading Excel sheet: {e}")
    else:
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

        sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
        total = sunburst_data['Count'].sum()
        sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

        sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
            sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%)'

        sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + (
            sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%'

        sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

        if color_mode == "Color by Salary Group":
            fig = px.sunburst(
                sunburst_data,
                path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
                values='Percentage',
                color='Salary_Group',
                color_discrete_sequence=px.colors.qualitative.Set3,
                title='🌈 Color by Salary Group'
            )
        else:  # Color by Percentage
            fig = px.sunburst(
                sunburst_data,
                path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
                values='Percentage',
                color='Percentage',
                color_continuous_scale='Turbo',
                title='🌈 Color by Percentage of Total'
            )
            fig.update_coloraxes(cmin=0, cmax=100, colorbar_title="Percentage (%)")

        fig.update_traces(maxdepth=2, branchvalues="total")
        st.plotly_chart(fig)
