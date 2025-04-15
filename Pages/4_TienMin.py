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
import community as community_louvain
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os


st.set_page_config(
    page_title="Visualizations",  
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Visualizations Made By Tien Min")  

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


    # Define plot files with optional widths
    plots = [
         ("Number of Hikers in Each Community", "plots/hiker_community_sizes.png", 2000),
        ("Number of Communities per Year", "plots/num_communities_per_year.png", 2000),
        ("Distribution of Hikers per Community", "plots/hikers_per_community_boxplot.png", 2000),
        ("Distribution of Community Activeness", "plots/community_activeness_boxplot.png", 2000),
        ("Average Activeness Over Time", "plots/activeness_trend.png", 2000),
       
    ]

    # Display all visualizations
    for title, path, width in plots:
        _, middle, _ = st.columns([1, 2, 1]) 
        with middle:
            st.markdown(f"<h3 style='text-align: center;'>{title}</h3>", unsafe_allow_html=True)
            if os.path.exists(path):
                st.image(Image.open(path), width=width)
            else:
                st.warning(f"Image not found: {path}")
            st.markdown(f"<h3 style='text-align: center;'>\n\n\n</h3>", unsafe_allow_html=True)


