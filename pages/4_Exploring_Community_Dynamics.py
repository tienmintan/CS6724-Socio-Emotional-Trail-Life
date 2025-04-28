import streamlit as st

st.set_page_config(
     layout="wide",
     initial_sidebar_state="expanded"
 )

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
from pyvis.network import Network
import streamlit.components.v1 as components

st.title("Exploring Community Dynamics")  

tab_titles = [
    "Animations",
    "Statistics",
    "Louvain Community Clusters",
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
with tabs[2]:

    col1, col2 = st.columns([2,1])
    with col1:
        @st.cache_data
        def load_cleaned_hiker_relations():
            df = pd.read_csv("cleaned_yearly_hiker_relations.csv")
            df["Mentioned Hikers"] = df["Mentioned Hikers"].fillna("")

            yearly_relations = {}
            for year in sorted(df["Year"].unique()):
                year_df = df[df["Year"] == year]
                G = {}
                for _, row in year_df.iterrows():
                    hiker = row["Hiker"].strip().lower()
                    mentions = [m.strip().lower() for m in row["Mentioned Hikers"].split(",") if m.strip()]
                    G[hiker] = mentions
                yearly_relations[year] = G
            return yearly_relations

        def build_graph(hiker_mentions_dict):
            G = nx.Graph()
            for hiker, mentions in hiker_mentions_dict.items():
                G.add_node(hiker)
                for mention in mentions:
                    G.add_edge(hiker, mention)
            return G

        def show_pyvis_graph(G, partition):
            net = Network(height="600px", width="100%", notebook=False)
            net.barnes_hut()

            # Map hiker names to anonymized labels
            mapping = {name: f"Hiker {i+1}" for i, name in enumerate(G.nodes)}
            G = nx.relabel_nodes(G, mapping)
            partition = {mapping[k]: v for k, v in partition.items()}

            for node in G.nodes:
                net.add_node(node, label=node, group=partition.get(node, 0))

            for edge in G.edges:
                net.add_edge(edge[0], edge[1])

            net.set_options("""
            var options = {
            "nodes": {
                "font": {
                "size": 16,
                "face": "Arial"
                }
            },
            "edges": {
                "color": {
                "inherit": true
                },
                "smooth": false
            },
            "physics": {
                "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.3,
                "springLength": 95
                },
                "minVelocity": 0.75
            }
            }
            """)

            net.save_graph("pyvis_graph.html")
            HtmlFile = open("pyvis_graph.html", "r", encoding="utf-8")
            components.html(HtmlFile.read(), height=650)

        # Streamlit UI
        st.title("Hiker Communities with Louvain Detection")
        yearly_relations = load_cleaned_hiker_relations()
        selected_year = st.selectbox("Select Year", list(yearly_relations.keys()))

        if selected_year:
            G = build_graph(yearly_relations[selected_year])
            if G.number_of_nodes() > 0:
                partition = community_louvain.best_partition(G, random_state=42)
                show_pyvis_graph(G, partition)
            else:
                st.warning("No data available for the selected year.")


    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.markdown("""
            - **Louvain Community Graphs (Yearly):** Each graph visualizes the hiker social networks discovered through journal mentions, clustered into communities.
            - **Node Colors Represent Communities:** Each color indicates a different social group detected by the Louvain algorithm.
            - **Node Size and Connections:** Node size is uniform for anonymity; edges represent social mentions between hikers, with denser clusters indicating tighter social cohesion.
            - **Year-to-Year Changes:** Visual density, number of isolated nodes, and group sizes shift noticeably across years, reflecting changes in hiker social dynamics.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **2019:** High connectivity and large, dense communities; most hikers belong to a few interconnected groups.
            - **2020:** Sparse network with many isolated hikers; very limited social clustering, likely due to pandemic disruptions.
            - **2021:** Recovery begins — one larger central group emerges alongside scattered smaller communities.
            - **2022–2023:** Communities remain more fragmented than 2019, but smaller clusters of hikers form stronger bonds within their groups.
            - **Overall Trend:** Trail social dynamics have shifted from large interconnected communities toward smaller, more self-contained clusters.
            """)

            st.subheader("Use Cases:")
            st.markdown("""
            - **Trail Managers:** Understand when hikers are more socially isolated vs. when support infrastructure (e.g., shelters, group camps) might be needed.
            - **Mental Health & Well-being Research:** Smaller, fragmented groups could indicate potential increases in hiker loneliness or decreased trail camaraderie after 2020.
            - **Sociological Studies:** Track how major societal disruptions (like the COVID-19 pandemic) ripple into outdoor social behavior and trail communities.
            - **Future Trail Planning:** Design strategies for fostering community among hikers during years of reduced natural interaction.
            """)
