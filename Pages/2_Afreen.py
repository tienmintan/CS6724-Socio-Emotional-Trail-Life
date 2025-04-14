import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

st.set_page_config(
    page_title="Visualizations",  
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Visualizations Made By Afreen")  

tab_titles = [
    "Most and Least Enjoyable Locations of the Trail in Each State",
    "Trail Magic Occurences by State",
    "Trail Magic Occurences per Mile in Each State",
    "Negative Emotions of NOBO Hikers Across the Trail",
    "Negative Emotions of SOBO Hikers Across the Trail",
    "dataset trail"
]

tabs = st.tabs(tab_titles)


with tabs[0]:
    st.header("Most and Least Enjoyable Locations of the Trail in Each State📍")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("best and worst spots.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

        st.markdown(
        """
        <div style="margin-top:20px; padding:12px 16px; background-color:#2c2f33; border-radius:10px; color:white; font-size:14px; width: 300px;">
            <div style="font-weight:600; font-size:15px; margin-bottom:8px;">Marker Legend</div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:20px; height:12px; background-color:skyblue; margin-right:10px;"></span>
                Most Enjoyable
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:20px; height:12px; background-color:red; margin-right:10px;"></span>
                Least Enjoyable
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the 3 best and worst 3 campsites, hostels, or shelters to visit on the Appalachian trail. Based on the emotional sentiment of journal entries recorded by hikers, the locations were measured and ranked by state for their total joy and negativity.")

            st.subheader("Key Insights:")
            st.write("Zoom into the map and click on the markers to see the worst locations, denoted by the red markers, and the best locations, denoted by the blue markers.")
            st.markdown("""
            -  West Virginia does not have any location with a higher positive or "enjoyable" weight, so it only has no good visitation sites. This shows there is a need for better campsites or shelters within the state for hikers.
            - 
            """)
            
            st.subheader("Use Cases:")
            st.write("Zoom into the map and click on the markers to see the worst locations, denoted by the red markers, and the best locations, denoted by the blue markers. West Virginia only had one location that had a higher positive weight, so it only has one good visitation site. This shows there is a need for better campsites or shelters within the state for hikers.")



with tabs[1]:
    st.header("Trail Magic Occurences by State 🪄")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("trail magic state map.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays how much trail magic occurs in each of the 14 states on the trail. Trail magic refers to acts of kindness towards hikers, including finding food or shelters with the help of strangers or other hikers.")

            st.subheader("Key Insights:")
            st.write("Zoom into the map to view which states contain the most trail magic. The darker the blue, the more magical the state is! Virginia has the most trail magic, while West Virginia has the least. This corresponds to our first map with WV's lack of good locations.")



with tabs[2]:
    st.header("Trail Magic Occurences per Mile in Each State 💫")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("trail_magic_per_mile_map.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays how much trail magic occurs in each of the 14 states on the trail. Trail magic refers to acts of kindness towards hikers, including finding food or shelters with the help of strangers or other hikers.")

            st.subheader("Key Insights:")
            st.write("Zoom into the map to view which states contain the most trail magic. The darker the blue, the more magical the state is! Virginia has the most trail magic, while West Virginia has the least. This corresponds to our first map with WV's lack of good locations.")



with tabs[3]:
    st.header("Negative Emotions of NOBO Hikers Across the Trail 👎⬆️")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("neg_emotions_markers_NOBO.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

        st.markdown(
        """
        <div style="margin-top:20px; padding:12px 16px; background-color:#2c2f33; border-radius:10px; color:white; font-size:14px; width: 300px;">
            <div style="font-weight:600; font-size:15px; margin-bottom:8px;">Sentiment Legend</div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:blue; border-radius:50%; margin-right:10px;"></span>
                Sadness
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:green; border-radius:50%; margin-right:10px;"></span>
                Disgust
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:orange; border-radius:50%; margin-right:10px;"></span>
                Anger
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:red; border-radius:50%; margin-right:10px;"></span>
                Fear
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the negative emotions that have been recorded on the trail. It specifically maps sadess, disgust, anger, and fear, which were expressed via journal entries from the hikers.")

            st.subheader("Key Insights:")
            st.write("Zoom into the map to view the individual emotion markers. Hovering over a marker will provide which emotion it corresponds to since the trail is densely packed with markerts. The most common negative emotion expressed on the trail seems to be fear, with sadness as a close second.")



with tabs[4]:
    st.header("Negative Emotions of SOBO Hikers Across the Trail 👎⬇️")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("neg_emotions_markers_SOBO.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

        st.markdown(
        """
        <div style="margin-top:20px; padding:12px 16px; background-color:#2c2f33; border-radius:10px; color:white; font-size:14px; width: 300px;">
            <div style="font-weight:600; font-size:15px; margin-bottom:8px;">Sentiment Legend</div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:blue; border-radius:50%; margin-right:10px;"></span>
                Sadness
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:green; border-radius:50%; margin-right:10px;"></span>
                Disgust
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:orange; border-radius:50%; margin-right:10px;"></span>
                Anger
            </div>
            <div style="margin:4px 0;">
                <span style="display:inline-block; width:12px; height:12px; background-color:red; border-radius:50%; margin-right:10px;"></span>
                Fear
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the negative emotions that have been recorded on the trail. It specifically maps sadess, disgust, anger, and fear, which were expressed via journal entries from the hikers.")

            st.subheader("Key Insights:")
            st.write("Zoom into the map to view the individual emotion markers. Hovering over a marker will provide which emotion it corresponds to since the trail is densely packed with markerts. The most common negative emotion expressed on the trail seems to be fear, with sadness as a close second.")

with tabs[5]:
    st.header("trying to display dataframe")
    df = pd.read_csv('CLEANED_CS6724_data_2013_2023.csv')
    st.write("### Dataset Header")
    st.write(df.head()) 

