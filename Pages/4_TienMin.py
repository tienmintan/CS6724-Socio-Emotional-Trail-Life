import streamlit as st
st.set_page_config(page_title="Hiker Community Animations", layout="wide")

# st.set_page_config(
#     page_title="Visualizations",  
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

st.title("Visualizations")  



import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import numpy as np
import networkx as nx
import community
from geopy.distance import geodesic
from scipy.interpolate import interp1d
from io import BytesIO
import tempfile
import json

# Your cleaned_yearly_hiker_relations and df should be preloaded
# Example:
df = pd.read_csv("CLEANED_CS6724_data_2013_2023.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Load cleaned CSV
with open("cleaned_yearly_hiker_relations.json", "r") as f:
    cleaned_yearly_hiker_relations = json.load(f)

def filter_large_jumps(df, threshold_km=300):
    if len(df) < 2:
        return df
    filtered = [df.iloc[0]]
    for i in range(1, len(df)):
        dist = geodesic((filtered[-1]["Latitude"], filtered[-1]["Longitude"]),
                        (df.iloc[i]["Latitude"], df.iloc[i]["Longitude"])).km
        if dist <= threshold_km:
            filtered.append(df.iloc[i])
    return pd.DataFrame(filtered)

def generate_animation(year, df, cleaned_yearly_hiker_relations):
    partition = community.best_partition(nx.Graph(
        [(h, m) for h, ms in cleaned_yearly_hiker_relations[year].items() for m in ms]),
        random_state=42)

    groups = sorted(set(partition.values()))
    calendar_dates = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="3D")

    fig, axs = plt.subplots(
        nrows=1, ncols=len(groups),
        figsize=(5 * len(groups), 5),
        subplot_kw={"projection": ccrs.PlateCarree()}
    )

    if len(groups) == 1:
        axs = [axs]

    scatter_plots = []

    df["normalized_name"] = df["Hiker trail name"].str.strip().str.lower().str.replace(r"[^a-z]", "", regex=True)
    df_year = df[df["date"].dt.year == year].copy()
    df_year["month_day"] = df_year["date"].dt.strftime("%m-%d")

    for col, group_id in enumerate(groups):
        ax = axs[col]
        ax.set_extent([-90, -65, 25, 50])
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.STATES)

        hikers_in_group = {h for h, cid in partition.items() if cid == group_id}
        df_group = df_year[df_year["normalized_name"].isin(hikers_in_group)].copy()

        interpolated_records = []

        hikers = df_group["normalized_name"].unique()
        color_map = cm.get_cmap("tab20", len(hikers))
        hiker_colors = {hiker: color_map(i) for i, hiker in enumerate(hikers)}

        for hiker in hikers:
            hiker_df = df_group[df_group["normalized_name"] == hiker][["month_day", "Latitude", "Longitude"]].copy()
            hiker_df = hiker_df.drop_duplicates("month_day").sort_values("month_day")
            hiker_df = filter_large_jumps(hiker_df)

            if len(hiker_df) < 2:
                continue

            dates = pd.to_datetime(f"{year}-" + hiker_df["month_day"])
            date_nums = (dates - pd.Timestamp(f"{year}-01-01")).dt.days  

            try:
                lat_interp = interp1d(date_nums, hiker_df["Latitude"], bounds_error=False, fill_value=np.nan)
                lon_interp = interp1d(date_nums, hiker_df["Longitude"], bounds_error=False, fill_value=np.nan)

                for day in range(0, 365, 3):
                    lat = lat_interp(day)
                    lon = lon_interp(day)
                    if np.isnan(lat) or np.isnan(lon):
                        continue
                    interpolated_records.append({
                        "date": pd.Timestamp(f"{year}-01-01") + pd.Timedelta(days=day),
                        "Latitude": float(lat),
                        "Longitude": float(lon),
                        "normalized_name": hiker
                    })
            except Exception:
                continue

        if not interpolated_records:
            ax.axis("off")
            scatter_plots.append(None)
            continue

        df_interp = pd.DataFrame(interpolated_records)
        scat = ax.scatter([], [], s=20, transform=ccrs.PlateCarree())
        ax.set_title(f"{year} - Group {group_id}", fontsize=10)

        scatter_plots.append((scat, df_interp, hiker_colors))

    date_text = fig.text(0.5, 0.96, '', ha='center', fontsize=16, weight='bold')

    def update(frame):
        date = calendar_dates[frame]
        date_text.set_text(date.strftime("Date: %B %d"))
        for idx, item in enumerate(scatter_plots):
            if item is None:
                continue
            scat, df_interp, hiker_colors = item
            active = df_interp[df_interp["date"] == date]
            scat.set_offsets(np.c_[active["Longitude"], active["Latitude"]])
            scat.set_color([hiker_colors[h] for h in active["normalized_name"]])
        return [s[0] for s in scatter_plots if s] + [date_text]

    ani = FuncAnimation(fig, update, frames=len(calendar_dates), interval=100, blit=False)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
        temp_video_path = tmpfile.name

    writer = FFMpegWriter(fps=10, metadata=dict(artist='AT Viz'), bitrate=1800)
    ani.save(temp_video_path, writer=writer)
    plt.close(fig)

    video_buffer = BytesIO()
    with open(temp_video_path, 'rb') as f:
        video_buffer.write(f.read())
    video_buffer.seek(0)
    return video_buffer

st.title("🎞️ Appalachian Trail Community Movements by Year")

year_options = sorted(cleaned_yearly_hiker_relations.keys())
selected_year = st.selectbox("Select a year", options=year_options)

if st.button("Generate Animation"):
    with st.spinner(f"Rendering animation for {selected_year}..."):
        video = generate_animation(selected_year, df, cleaned_yearly_hiker_relations)
        st.video(video)
