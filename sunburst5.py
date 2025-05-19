if color_mode == "Color by Salary Group":
    # YES = Greens
    yes_fields = sunburst_data[sunburst_data['Entrepreneurship'] == 'Yes']['Field_of_Study'].unique()
    yes_colors = px.colors.sample_colorscale("Greens", [i / max(1, len(yes_fields) - 1) for i in range(len(yes_fields))])
    field_color_map = {('Yes', field): yes_colors[i] for i, field in enumerate(yes_fields)}

    # NO = custom red palette (from image)
    custom_red_palette = [
        "#F8B5B5", "#F78C8C", "#F65C5C", "#F43131", "#F20000",
        "#DB8A8A", "#DA6363", "#D63C3C", "#D11111", "#BD0000",
        "#B36C6C", "#B34646", "#B01F1F", "#9C0000", "#860000"
    ]
    no_fields = sunburst_data[sunburst_data['Entrepreneurship'] == 'No']['Field_of_Study'].unique()
    for i, field in enumerate(no_fields):
        field_color_map[('No', field)] = custom_red_palette[i % len(custom_red_palette)]

    # Assign blended color
    def assign_color(row):
        return field_color_map.get((row['Entrepreneurship'], row['Field_of_Study']), "#000000")  # fallback is black to catch error

    sunburst_data['Color_Assign'] = sunburst_data.apply(assign_color, axis=1)

    fig = px.sunburst(
        sunburst_data,
        path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
        values='Percentage',
        color='Color_Assign',
        color_discrete_map={c: c for c in sunburst_data['Color_Assign'].unique()},
        title='🌿 Color by Salary Group (Green for Yes, Red for No)'
    )
