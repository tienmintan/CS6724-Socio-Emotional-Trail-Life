import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from pathlib import Path
import pandas as pd
import numpy as np
import json
import re
import networkx as nx
from collections import defaultdict
from pathlib import Path
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os
import plotly.express as px


st.set_page_config(
    page_title="Visualizations",  
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploring Community Dynamics")  

tab_titles = [
    "Animations",
    "Statistics",
]

tabs = st.tabs(tab_titles)

with tabs[0]:
    st.header("Hiker Community Movements")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("## Select Year and Group")
        years = list(range(2019, 2024)) 
        groups = list(range(10))         

        col1a, col2a = st.columns(2)
        selected_year = col1a.selectbox("Year", years)
        selected_group = col2a.selectbox("Group ID", groups)

        video_path = Path(f"static_mp4s/Group_{selected_group}_{selected_year}.mp4")
        st.markdown("<h3 style='text-align: center;'>Group Movement Animation</h3>", unsafe_allow_html=True)

        if video_path.exists():
            _, middle, _ = st.columns([1, 10, 1]) 

            with middle:
                st.video(str(video_path))
        else:
            st.warning("No animation found for this group and year.")
    
    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("""These visualizations animate the movement patterns of long-distance hikers along the Appalachian Trail over multiple years and shows the spatial dynamics of trail communities. The visualization was built using geospatial data and hiker journal entries, clustered into social groups using community detection algorithms, and interpolated to produce smooth animations.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Group Formations:** The animation shows hiker groups forming tightly at the beginning of the year—especially in southern regions like Georgia—then gradually dispersing northward. Some groups appear highly cohesive throughout the year, while others fragment or fade, which can be explained by dropouts, variable pace, or social drift.
            - **Geographical Consistency:** The movements closely trace the route from Georgia to Maine, confirming that the data aligns with the physical trail. Bottlenecks and slowdowns are visible near trail towns and popular rest points, suggesting logistical or social pauses.
            - **Group Size and Trail Progression:** Early in the season, some groups are large, dense, or both. However, over time, many hikers either speed ahead or lag behind, leading to sparse or vanished group representations by fall. Some groups make very erratic movements, large geographic jumps, or disappear mid-way—potentially highlighting diversions or logging inconsistencies.
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - **Trail Policy and Infrastructure Planning:** Park managers can identify when and where trail segments face the most pressure, helping prioritize shelter repairs, water resource checks, and waste management systems seasonally.
            - **Group Dynamics Analysis:** Behavioral researchers can use this visualization to examine how loosely or tightly human groups form and evolve in isolation, particularly in endurance activities.
            - **Emergency Response Training:** Rescue teams could use past data of group movement trends to simulate likely locations of missing hikers based on the time of the year and typical group movement paths.
            """)



with tabs[1]:
    st.header("Hiker Community Statistics\n")

    col1, col2 = st.columns([2, 1])
    with col1:
        # === Load data ===
        df = pd.read_csv("CLEANED_CS6724_data_2013_2023.csv")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df[df["date"].notna()]
        df["normalized_name"] = df["Hiker trail name"].astype(str).str.strip().str.lower().str.replace(r"[^a-z]", "", regex=True)

        with open("cleaned_yearly_hiker_relations.json") as f:
            cleaned_yearly_hiker_relations = json.load(f)

        # Containers
        community_sizes_by_year = {}
        community_count_by_year = {}
        community_activeness_by_year = {}

        # Calculate community data
        years = sorted([str(y) for y in cleaned_yearly_hiker_relations.keys()])
        for year in years:
            year_int = int(year)
            relations = cleaned_yearly_hiker_relations[year]

            G = nx.Graph([(h, m) for h, ms in relations.items() for m in ms])
            partition = community_louvain.best_partition(G, random_state=42)

            community_hikers = defaultdict(set)
            for hiker, cid in partition.items():
                community_hikers[cid].add(hiker)

            sizes = [len(members) for members in community_hikers.values()]
            community_sizes_by_year[year] = sizes
            community_count_by_year[year] = len(sizes)

            df_year = df[df["date"].dt.year == year_int].copy()
            community_activeness = []
            for cid, hikers in community_hikers.items():
                entry_count = df_year[df_year["normalized_name"].isin(hikers)].shape[0]
                community_activeness.append(entry_count)

            community_activeness_by_year[year] = community_activeness

        # 1. Number of Communities per Year
        num_communities = [community_count_by_year[y] for y in years]
        fig1 = px.bar(
            x=years,
            y=num_communities,
            labels={'x': 'Year', 'y': '# of Communities'},
            title="Number of Communities per Year"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Distribution of Community Sizes
        data2 = [(y, size) for y in years for size in community_sizes_by_year[y]]
        df_size = pd.DataFrame(data2, columns=["Year", "Community Size"])
        fig2 = px.box(
            df_size,
            x="Year",
            y="Community Size",
            title="Distribution of Community Sizes per Year"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 3. Distribution of Community Activeness
        data3 = [(y, act) for y in years for act in community_activeness_by_year[y]]
        df_act = pd.DataFrame(data3, columns=["Year", "Journal Entries"])
        fig3 = px.box(
            df_act,
            x="Year",
            y="Journal Entries",
            title="Community Activeness per Year"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # 4. Mean Activeness Over Time
        df_avg_activeness = pd.DataFrame({
            "Year": [str(y) for y in years],
            "Average Journal Entries": [np.mean(community_activeness_by_year[y]) for y in years]
        })

        df_avg_activeness["Year"] = pd.to_numeric(df_avg_activeness["Year"])

        df_avg_activeness = df_avg_activeness.sort_values("Year")

        fig = px.line(
            df_avg_activeness,
            x="Year",
            y="Average Journal Entries",
            markers=True,
            title="Average Community Activeness Over Time"
        )

        fig.update_traces(mode="lines+markers", line=dict(color="lightblue"))
        fig.update_layout(
            xaxis=dict(title="Year"),
            yaxis=dict(title="Average Journal Entries")
        )

        st.plotly_chart(fig, use_container_width=True)

        # 5. Hikers in Each Community
        data5 = []
        for year in years:
            sizes = community_sizes_by_year[year]
            for i, size in enumerate(sizes):
                data5.append({"Year": int(year), "Group": i, "Size": size})

        df_sizes = pd.DataFrame(data5)
        df_sizes["Label"] = df_sizes["Year"].astype(str) + "_G" + df_sizes["Group"].astype(str)
        fig5 = px.bar(
            df_sizes.sort_values("Size", ascending=False),
            x="Label",
            y="Size",
            title="Number of Hikers in Each Community",
            labels={"Label": "Community (Year_GroupID)", "Size": "# of Hikers"}
        )
        fig5.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.subheader("Statistic Explanation:")
            st.markdown("""
            - **Number of Communities per Year:** Shows how many unique hiker communities formed each year. Peaks in 2019, then remains steady with a slight dip post-2020.
            - **Distribution of Community Sizes per Year:** A boxplot visualizing how large the hiker communities were each year. 2019 has both the largest and most varied group sizes, while later years show smaller, more consistent communities.
            - **Community Activeness per Year:** Depicts how active each community was in terms of journal entries. 2019 communities were highly active, while 2020 had minimal activity.
            - **Average Community Activeness Over Time:** A dot plot showing year-over-year trends in average journal entries per community. Strong drop in 2020, with gradual recovery through 2023.
            - **Number of Hikers in Each Community:** Bar chart ranking all communities (by year and group ID) by number of hikers. 2019 groups dominate the top with the largest sizes.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - 2019 was a standout year with the highest number of communities, most diverse group sizes, and significantly higher activity levels.
            - 2020 saw a sharp decline in both the number and activeness of communities, likely influenced by global travel restrictions and trail access limitations.
            - Post-2020 communities tend to be smaller and more uniform in size, potentially reflecting changes in trail usage or how groups formed.
            - Journal activity rebounded after 2020, but has not yet reached the levels observed in 2019 — possibly suggesting ongoing shifts in hiker engagement or documentation.
            - The most populous communities are concentrated in 2019, while recent years feature smaller but consistently sized groups.
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - Researchers and sociologists can explore how external events (e.g., the pandemic) influenced outdoor social behavior and community dynamics on long trails.
            - Trail planners and conservancy groups can use community size and activeness data to determine which years need more support infrastructure or outreach.
            - App developers and social platforms targeting hikers can identify the years and groups with the highest engagement for further community building or feedback collection.
            - Historians and writers documenting Appalachian Trail culture can focus on 2019 as a pivotal year for community formation and trail engagement.
            """)
