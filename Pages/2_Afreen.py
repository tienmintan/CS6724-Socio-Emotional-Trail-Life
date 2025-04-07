import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Visualizations",  
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Visualizations Made By Afreen")  

tab_titles = [
    "Best and Worst Spots in Each State",
    "Trail Magic Occurences by State",
    "Negative Emotions Across the Trail"
]

tabs = st.tabs(tab_titles)


with tabs[0]:
    st.header("Best and Worst Spots in Each State📍")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("best and worst spots.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the 3 best and worst 3 campsites, hostels, or shelters to visit on the Appalachian trail. Based on the emotional sentiment of journal entries recorded by hikers, the locations were measured and ranked by state for their total joy and negativity.")

            st.subheader("Key Insights:")
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
    st.header("Negative Emotions Across the Trail 👎")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("negative emotions map.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the negative emotions that have been recorded on the trail. It specifically maps sadess, disgust, anger, and fear, which were expressed via journal entries from the hikers.")

            st.subheader("Key Insights:")
            st.write("Zoom into the map to view the individual emotion markers. Hovering over a marker will provide which emotion it corresponds to since the trail is densely packed with markerts. The most common negative emotion expressed on the trail seems to be fear, with sadness as a close second.")
