import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc

# App Title
st.set_page_config(page_title="Sunburst Chart", layout="wide")
st.title("🌿 Sunburst Chart: Entrepreneurship → Field → Salary")

# Upload Excel file
uploaded_file = st.file_uploader("📤 Upload your Excel file (`education_career_success.xlsx`)", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name='education_career_success')
    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
    else:
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
        total = sunburst_data['Count'].sum()
        sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

        # Labels for chart levels
        sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
            sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%)'

        sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + (
            sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%'

        sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

        # ========== Custom Coloring ==========
        # Define base colors
        base_colors = {
            'Yes': '#6BBF59',  # greenish
            'No': '#F08080'    # light red
        }

        # Convert HEX to RGB string
        def hex_to_rgb_str(hex_color):
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f'rgb({r},{g},{b})'

        # Assign a soft pastel tone to each field
        fields = sunburst_data['Field_of_Study'].unique()
        field_palette = px.colors.sample_colorscale("Tealrose", [i / len(fields) for i in range(len(fields))])
        field_color_map = dict(zip(fields, field_palette))

        # Blend industry tone + Yes/No overlay
        def generate_combined_color(row):
            ent = row['Entrepreneurship']
            field = row['Field_of_Study']
            base_hex = field_color_map.get(field, "#CCCCCC")
            overlay_hex = base_colors.get(ent, "#999999")
            base = hex_to_rgb_str(base_hex)
            overlay = hex_to_rgb_str(overlay_hex)
            return pc.find_intermediate_color(base, overlay, 0.5, colortype='rgb')

        sunburst_data['Custom_Color'] = sunburst_data.apply(generate_combined_color, axis=1)

        # Plot Sunburst
        fig = px.sunburst(
            sunburst_data,
            path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
            values='Percentage',
            color=sunburst_data['Custom_Color'],
            color_discrete_map=dict(zip(sunburst_data['Custom_Color'], sunburst_data['Custom_Color'])),
            title='🎓 Salary Outcomes by Field & Entrepreneurship'
        )

        fig.update_traces(maxdepth=2, branchvalues="total")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 Please upload a valid Excel file with the sheet `education_career_success`.")
