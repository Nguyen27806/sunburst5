import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Career Path Sunburst",
    layout="wide",
    page_icon="🌞"
)

st.title("🌞 Career Path Sunburst")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

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

# Tính toán tổng thể cho sunburst
sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
total_count = sunburst_data['Count'].sum()

# Chuẩn bị dữ liệu theo cấu trúc hierachy cho go.Sunburst
labels = []
parents = []
values = []
text_colors = []

# Tạo mapping cho màu chữ riêng Field_of_Study
white_fields_no = ['Business', 'Engineering', 'Mathematics']
white_fields_yes = ['Medicine', 'Arts']

# Vòng 1: Entrepreneurship
for ent in sunburst_data['Entrepreneurship'].unique():
    ent_total = sunburst_data[sunburst_data['Entrepreneurship'] == ent]['Count'].sum()
    labels.append(ent)
    parents.append("")
    values.append(ent_total)
    text_colors.append("black")  # Vòng 1 luôn đen

    # Vòng 2: Field of Study
    sub_df = sunburst_data[sunburst_data['Entrepreneurship'] == ent]
    for field in sub_df['Field_of_Study'].unique():
        field_total = sub_df[sub_df['Field_of_Study'] == field]['Count'].sum()
        labels.append(field)
        parents.append(ent)
        values.append(field_total)

        if (ent == 'Yes' and field in white_fields_yes) or (ent == 'No' and field in white_fields_no):
            text_colors.append("white")
        else:
            text_colors.append("black")

        # Vòng 3: Salary Group
        sub_sub_df = sub_df[sub_df['Field_of_Study'] == field]
        for _, row in sub_sub_df.iterrows():
            salary = row['Salary_Group']
            count = row['Count']
            labels.append(salary)
            parents.append(field)
            values.append(count)
            text_colors.append("black")  # Vòng ngoài giữ nguyên: đen hết

# Tạo biểu đồ bằng go.Sunburst
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    insidetextorientation='radial',
    textfont=dict(color=text_colors),
    hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
))

fig.update_layout(
    title='Career Path Insights: Education, Salary & Entrepreneurship',
    width=600,
    height=600,
    margin=dict(t=50, l=0, r=0, b=0)
)

# Streamlit display
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💡 How to use")
    st.markdown(
        """
- The chart displays three layers:
  - *Entrepreneurship* (center)
  - *Field of Study* (middle ring)
  - *Salary Group* (outer ring)
- Labels are mostly black for readability.
- **Exceptions (white text):**
  - No: Business, Engineering, Mathematics
  - Yes: Medicine, Arts
        """
    )
