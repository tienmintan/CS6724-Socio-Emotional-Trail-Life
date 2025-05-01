import streamlit as st

st.set_page_config(
     layout="wide",
     initial_sidebar_state="expanded"
 )

import streamlit.components.v1 as components

st.title("Socialness Visualizations")  

tab_titles = [
    "Social Interactions on hiking trails ",
    "Social Interactions by Year and Month",
    "Monthly Distribution of Social Interactions"
]

tabs = st.tabs(tab_titles)

with tabs[0]:
    st.header("Social Interactions on hiking trails📍")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("social_interactions_density.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=700, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the 4 socialness groups and their density on on the Appalachian trail. Socialness is recorded by the hikers in their journal entries. The density is measured by the weighted score given for each socialness group.")

            st.subheader("Key Insights:")
            st.write("""
                Warmer colors indicate hotspots with frequent social interactions.  
                Group hikes, meetups, and trail magic are among the most commonly observed interactions.  
                Locations with higher weight values represent stronger social bonds, such as family hikes.  

                **Fulltilt** ranks as the top hiking trail for **Socialness Group 1** (Campfire, Conversation, Share, Meet, Call, Together) and **Group 3** (Magic, Trail Magic, Trail Angel).  
                **Sev** is the top trail for **Socialness Group 2** (Couple, Family, Friend, Pet),  
                while **Valley Forge** leads for **Group 4** (Fest, Festival, Event, Community, Trail Town).
                """)
            
            st.subheader("Use Cases:")
            st.write("""  
                - An outdoor brand or guided tour company wants to design social experience-based hiking packages, they can offer curated group hiking experiences on Fulltilt, which ranks highest for social interactions like conversation, meeting new people, and trail magic. 
                - Socially motivated hikers are recommended to use the heatmap data to identify and suggest hotspot areas for scenic breaks, pet rest areas, or couple-friendly lookout points.  
                - A regional tourism board wants to drive foot traffic and engagement through local events and host community events around Valley Forge, the top trail for keywords like fest, event, and community.
 
                """)


with tabs[1]:
    st.header("Social Interactions by Year and Month 🪄")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("bar_chart_socialness.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=700, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("This map displays total unique social interactions by year (2020 till 2023) and stacked by month in order.Each year’s bar is divided into 12 colored segments, representing different months")

            st.subheader("Key Insights:")
            st.write("""
                **Interaction Trends Over Time:**  
                - 2020 had the lowest total interactions, while 2023 had the highest.  
                - **June and July** have the highest interaction counts, while **December and January** have the lowest.  
                - This suggests that social interactions peak during the summer, making it the best time for activities like hiking.
 
                """)
            st.subheader("Use Cases:")
            st.write("""  
                - An outdoor gear or apparel brand wants to launch a targeted summer campaign, •  during June and July, capitalizing on the peak in social interactions and trail usage. 
                - A parks department wants to maximize turnout for guided hikes or trail events, can schedule community hikes during June and July, aligning with peak interaction periods. 
 
                """)
            

          

            


with tabs[2]:
    st.header("Monthly Distribution of Social Interactions ☀️")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("line_chart_socialness.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=700, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Chart Explanation:")
            st.write("This line chart displays the monthly distribution of unique social interactions from 2020 to 2023. Each line represents a different interaction type—such as couple, friend, trail magic, or event—plotted across the months from January to December. The chart captures seasonal patterns in trail behavior.")

            st.subheader("Key Insights:")
            st.write("""
                **Interaction Trends Over Time:**  
                - Social interactions peak during the summer, making it the best time for activities like hiking.  
                - Interactions start increasing from April (spring), peaking in June & July (summer). A decline begins in September, reaching the lowest levels in December & January (winter).
                - Couples have the highest interaction levels, followed by families. Fest has the lowest social interaction levels across all months.
 
                """)
            st.subheader("Use Cases:")
            st.write("""  
                - A travel agency or hiking tour group wants to cater to couples and families looking for outdoor getaways, can design “Spring to Summer Romance” and “Family Trail Time” packages starting in April, peaking with special offers in June and July.
                - An app developer wants to create a personalized user experience that adapts to social trends, from April to July, highlight trails that attract couples or families and push community features (e.g., create hike groups, share experiences). 
 
                """)
