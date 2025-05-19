import plotly.colors as pc  # thêm ở đầu file nếu chưa có

# Define base colors for Yes/No
base_colors = {
    'Yes': '#6BBF59',  # xanh lá nhẹ
    'No': '#F08080'    # đỏ nhẹ
}

# Hàm chuyển hex -> 'rgb(r,g,b)' (để blend)
def hex_to_rgb_str(hex_color):
    if hex_color.startswith('rgb'):
        return hex_color
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return 'rgb(200,200,200)'
    try:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgb({r},{g},{b})'
    except:
        return 'rgb(200,200,200)'

# Ánh xạ màu theo ngành học (ombre tone)
fields = sunburst_data['Field_of_Study'].unique()
field_palette = px.colors.sample_colorscale("Tealrose", [i / len(fields) for i in range(len(fields))])
field_color_map = dict(zip(fields, field_palette))

# Kết hợp màu ngành + Yes/No
def generate_custom_color(row):
    field = row['Field_of_Study']
    ent = row['Entrepreneurship']
    base_hex = field_color_map.get(field, "#CCCCCC")
    overlay_hex = base_colors.get(ent, "#999999")
    base = hex_to_rgb_str(base_hex)
    overlay = hex_to_rgb_str(overlay_hex)
    return pc.find_intermediate_color(base, overlay, 0.5, colortype='rgb')

sunburst_data['Custom_Color'] = sunburst_data.apply(generate_custom_color, axis=1)

# Tạo biểu đồ với custom color
fig = px.sunburst(
    sunburst_data,
    path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
    values='Percentage',
    color=sunburst_data['Custom_Color'],
    color_discrete_map=dict(zip(sunburst_data['Custom_Color'], sunburst_data['Custom_Color'])),
    title='🌈 Color by Salary Group (with Custom Field + Yes/No Colors)'
)
