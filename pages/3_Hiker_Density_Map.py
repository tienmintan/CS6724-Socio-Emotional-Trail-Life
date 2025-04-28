import streamlit as st

st.set_page_config(
     layout="wide",
     initial_sidebar_state="expanded"
 )

import streamlit.components.v1 as components
import os

st.title("📍 Hiker Density Interactive Heatmap")

# === Layout the map and sidebar ===
col1, col2 = st.columns([2, 1])

with col1:
    # Load the HTML map
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "interactive_hikers_map.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=600, scrolling=True)

    # Legend stays below the map
    st.markdown(
        """
        <div style="margin-top:20px; padding:12px 16px; background-color:#2c2f33; border-radius:10px; color:white; font-size:14px; width: 300px;">
            <div style="font-weight:600; font-size:15px; margin-bottom:8px;">Heatmap Legend</div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:20px; height:12px; background-color:blue; margin-right:10px;"></span>
                Low
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:20px; height:12px; background-color:lime; margin-right:10px;"></span>
                Medium
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:20px; height:12px; background-color:orange; margin-right:10px;"></span>
                High
            </div>
            <div style="margin:4px 0 12px 0;">
                <span style="display:inline-block; width:20px; height:12px; background-color:red; margin-right:10px;"></span>
                Very High
            </div>
            <div style="font-weight:600; font-size:15px; margin-bottom:8px;">Sentiment Color</div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:green; border-radius:50%; margin-right:10px;"></span>
                Positive
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:red; border-radius:50%; margin-right:10px;"></span>
                Negative
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:blue; border-radius:50%; margin-right:10px;"></span>
                Neutral
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    with st.container(border=True):
        st.subheader("Map Explanation:")
        st.write("This map displays hiker activity and emotional sentiment across the Appalachian Trail from 2021–2023. The data is based on journal entries and reveals trail density through heat intensity and emotions via colored markers.")

        st.subheader("Key Insights:")
        st.markdown("""
        - Hikers in dense areas tend to have better experiences, shown by green (positive) and blue (neutral) sentiment markers.  
        - High traffic areas promote friendliness and shared experiences, often described as "trail magic."  
        - Red markers (negative sentiment) are more frequent in sparse, northern areas (e.g., New York, Massachusetts).  
        - These regions may feel tougher, lonelier, and have fewer facilities, leading to harsher reviews.  
        - More activity = more sentiment data, showing higher engagement where trails are busy.
        """)

        st.subheader("Use Cases:")
        st.markdown("""
        - Trip Planning  
        - Park Management  
        - Studying the Relationship Between Emotions and Hiker Density
        """)
