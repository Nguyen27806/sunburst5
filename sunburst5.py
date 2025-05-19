import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc

# Title
st.title("🌿 Sunburst Chart Colored by Field & Yes/No Status")

# Upload file
uploaded_file = st.file_uploader("📤 Upload the Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name='education_career_success')
    except Exception as e:
        st.error(f"❌ Error loading Excel sheet: {e}")
    else:
        # Salary grouping
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

        # Create chart data
        sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
        total = sunburst_data['Count'].sum()
        sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

        # Labels for each level
        sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
            sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%)'

        sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + (
            sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%'

        sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

        # Màu riêng cho Yes (xanh lá), No (đỏ nhẹ), Field (ombre tone)
        base_colors = {
            'Yes': '#6BBF59',  # xanh lá nhạt
            'No': '#F08080'    # đỏ nhạt
        }

        field_unique = sunburst_data['Field_of_Study'].unique()
        field_palette = px.colors.sample_colorscale("Pastel", [i/len(field_unique) for i in range(len(field_unique))])
        field_color_map = dict(zip(field_unique, field_palette))

        # Tạo chuỗi màu cuối cùng kết hợp Yes/No với ngành
        def generate_combined_color(row):
            ent = row['Entrepreneurship']
            field = row['Field_of_Study']
            base = field_color_map.get(field, "#CCCCCC")
            overlay = base_colors.get(ent, "#999999")
            # blend màu nhẹ nhàng giữa base (ngành) và overlay (yes/no)
            return pc.find_intermediate_color(base, overlay, 0.5, colortype='rgb')

        sunburst_data['Custom_Color'] = sunburst_data.apply(generate_combined_color, axis=1)

        # Tạo biểu đồ với custom color
        fig = px.sunburst(
            sunburst_data,
            path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
            values='Percentage',
            title='🌿 Field + Yes/No Colored Sunburst Chart',
            color=sunburst_data['Custom_Color'],  # dùng field để giữ mapping
            color_discrete_map=dict(zip(sunburst_data['Custom_Color'], sunburst_data['Custom_Color']))
        )

        fig.update_traces(maxdepth=2, branchvalues="total")
        st.plotly_chart(fig)
