import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sunburst Chart", layout="wide")
st.title("🌞 Sunburst Chart – Salary, Field, and Entrepreneurship")

uploaded_file = st.file_uploader("📤 Upload the Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name='education_career_success')
    except Exception as e:
        st.error(f"❌ Error loading Excel sheet: {e}")
    else:
        # Chọn chế độ tô màu sau khi tải file thành công
        color_mode = st.radio("🎨 Choose color mode:", ("Color by Salary Group", "Color by Percentage"))

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
            # YES = xanh lá cây
            yes_fields = sunburst_data[sunburst_data['Entrepreneurship'] == 'Yes']['Field_of_Study'].unique()
            yes_colors = px.colors.sample_colorscale("Greens", [i / max(1, len(yes_fields) - 1) for i in range(len(yes_fields))])
            field_color_map = {('Yes', field): yes_colors[i] for i, field in enumerate(yes_fields)}

            # NO = bảng màu đỏ tùy chỉnh
            custom_red_palette = [
                "#F8B5B5", "#F78C8C", "#F65C5C", "#F43131", "#F20000",
                "#DB8A8A", "#DA6363", "#D63C3C", "#D11111", "#BD0000",
                "#B36C6C", "#B34646", "#B01F1F", "#9C0000", "#860000"
            ]
            no_fields = sunburst_data[sunburst_data['Entrepreneurship'] == 'No']['Field_of_Study'].unique()
            for i, field in enumerate(no_fields):
                field_color_map[('No', field)] = custom_red_palette[i % len(custom_red_palette)]

            # Gán màu theo từng ngành + nhóm Yes/No
            def assign_color(row):
                return field_color_map.get((row['Entrepreneurship'], row['Field_of_Study']), "#000000")

            sunburst_data['Color_Assign'] = sunburst_data.apply(assign_color, axis=1)

            fig = px.sunburst(
                sunburst_data,
                path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
                values='Percentage',
                color='Color_Assign',
                color_discrete_map={c: c for c in sunburst_data['Color_Assign'].unique()},
                title='🌿 Color by Salary Group (Green for Yes, Red for No)'
            )

        else:
            # Chế độ tô màu theo phần trăm
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
        st.plotly_chart(fig, use_container_width=True)
