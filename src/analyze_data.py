import pandas as pd
import folium
import matplotlib.pyplot as plt
import random

# 1️⃣ 读取数据
csv_path = "data/processed/ebird_cleaned.csv"
df = pd.read_csv(csv_path)


# 随机取样 (为了地图加载更快)
sample_df = df.sample(min(300, len(df)))

# 为每个鸟种分配不同颜色
species = sample_df["common_name"].unique()
colors = plt.cm.get_cmap('tab20', len(species))  # 使用 matplotlib 的配色方案
color_map = {species[i]: f"#{int(colors(i)[0]*255):02x}{int(colors(i)[1]*255):02x}{int(colors(i)[2]*255):02x}" for i in range(len(species))}

# 创建 folium 地图
m = folium.Map(location=[df["lat"].mean(), df["lng"].mean()], zoom_start=6, tiles="cartodb positron")

# 为每个观测点添加带图片 popup 的标记
for _, row in sample_df.iterrows():
    bird = row["common_name"]
    color = color_map.get(bird, "gray")

    # eBird 图片 API (简易方式：从 Wikimedia 取图，或你可以手动替换)
    bird_query = bird.replace(" ", "_")
    image_url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/{bird_query}.jpg/240px-{bird_query}.jpg"

    html = f"""
    <b>{bird}</b><br>
    <i>{row['scientific_name']}</i><br>
    🧮 Count: {int(row['howMany']) if not pd.isna(row['howMany']) else 'N/A'}<br>
    📍 Location: {row['locName']}<br>
    <img src="{image_url}" width="200"><br>
    """

    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=5,
        popup=folium.Popup(html, max_width=250),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 添加图例
legend_html = """
<div style="position: fixed; 
     bottom: 30px; left: 30px; width: 250px; height: auto; 
     border:2px solid grey; z-index:9999; font-size:12px;
     background-color:white; padding:10px;">
     <b>Bird Species Colors</b><br>
"""
for sp, col in color_map.items():
    legend_html += f'<span style="color:{col};">&#9679;</span> {sp}<br>'
legend_html += "</div>"
m.get_root().html.add_child(folium.Element(legend_html))

# 保存地图
m.save("bird_map_color.html")
print("✅ Colorful map saved as bird_map_color.html — open it in browser!")

