# Define base colors for Yes/No
base_colors = {
    'Yes': '#6BBF59',  # light green
    'No': '#F08080'    # light red
}

# Chuyển mã hex sang chuỗi 'rgb(r,g,b)' để tương thích Plotly
def hex_to_rgb_str(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgb({r},{g},{b})'

# Field-based color (use valid colorscale)
field_unique = sunburst_data['Field_of_Study'].unique()
field_palette = px.colors.sample_colorscale("Tealrose", [i / len(field_unique) for i in range(len(field_unique))])
field_color_map = dict(zip(field_unique, field_palette))

# Kết hợp màu ngành (base) + Yes/No (overlay)
def generate_combined_color(row):
    ent = row['Entrepreneurship']
    field = row['Field_of_Study']
    base_hex = field_color_map.get(field, "#CCCCCC")
    overlay_hex = base_colors.get(ent, "#999999")
    base = hex_to_rgb_str(base_hex)
    overlay = hex_to_rgb_str(overlay_hex)
    return pc.find_intermediate_color(base, overlay, 0.5, colortype='rgb')

sunburst_data['Custom_Color'] = sunburst_data.apply(generate_combined_color, axis=1)

# Vẽ biểu đồ với custom color
fig = px.sunburst(
    sunburst_data,
    path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
    values='Percentage',
    color=sunburst_data['Custom_Color'],
    color_discrete_map=dict(zip(sunburst_data['Custom_Color'], sunburst_data['Custom_Color'])),
    title='🌿 Field + Yes/No Colored Sunburst Chart'
)
