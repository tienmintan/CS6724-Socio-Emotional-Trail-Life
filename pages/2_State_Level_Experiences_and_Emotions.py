import streamlit as st

st.set_page_config(
     page_title="Visualizations",  
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded"
 )

import streamlit.components.v1 as components
import pandas as pd
import os
import geopandas as gpd
import folium
from shapely.geometry import Point
from streamlit_folium import st_folium

st.title("State Level Experiences and Emotions Maps")  

tab_titles = [
    "Most and Least Enjoyable Locations of the Trail in Each State",
    "Trail Magic Occurences by State",
    "Trail Magic Occurences per Mile in Each State",
    "Interactive Trail Magic per Mile by Year",     
    "Negative Emotions of NOBO Hikers Across the Trail",
    "Negative Emotions of SOBO Hikers Across the Trail",
]

tabs = st.tabs(tab_titles)

top_joy = pd.read_csv("best spots.csv")
top_negative = pd.read_csv("worst spots.csv")

with tabs[0]:
    st.header("Most and Least Enjoyable Locations of the Trail in Each State📍")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("best and worst spots.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

        legend_col, joy_col, neg_col = st.columns([0.65, 2, 2])

        with legend_col:
                    st.markdown(
            """
            <div style="margin-top:10px; padding:12px 16px; background-color:#2c2f33; border-radius:10px; color:white; font-size:14px;">
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

        with joy_col:
            st.markdown("**3 Most Enjoyable Spots in Each State** 🌟")
            st.dataframe(top_joy[['State', 'Destination', 'joy', 'Latitude', 'Longitude']], use_container_width=True)

        with neg_col:
            st.markdown("**3 Least Enjoyable Spots in Each State** ⚠️")
            st.dataframe(top_negative[['State', 'Destination', 'Negative Score', 'Latitude', 'Longitude']], use_container_width=True)
    
    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays the 3 most enjoyable and 3 least enjoyable campsites, hostels, or shelters to visit in each state of the Appalachian trail. Based on the emotional sentiment of journal entries recorded by hikers, the locations were measured and ranked by state for their total joy and negativity. Zoom into the map and click on the markers to see the most fearful or negative locations, denoted by the red markers, and the most joyful or positive locations, denoted by the blue markers.")

            st.subheader("Key Insights:")
            st.markdown("""
            - West Virginia does not have any location with a higher positive or "enjoyable" weight. New York only has 1, and Massachusetts has 2. This shows there is a need for better campsites or shelters within the state for hikers.
            - Overall, Virginia has the most highly rated locations for its 3 best locations and 3 least enjoyable locations in comparison to all other states. 
            - Pennsylvania has the highest joy rating for its top location at 0.9309. 
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - Hikers can plan their trip using this map to decide which hostels, campsites, and shelters would be the best to visit and which ones they should avoid. 
            - Trail Managers can investigate the least enjoyable locations for any needed repairs or additional assistance. 
            """)



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
            st.write("This map displays how much trail magic occurs in each of the 14 states on the trail. Trail magic refers to acts of kindness towards hikers, including finding food or shelters with the help of strangers or other hikers. Zoom into the map to view which states contain the most trail magic. The darker the blue, the more magical the state is!")

            st.subheader("Key Insights:")
            st.markdown("""
            - West Virginia has the least trail magic.
            - Virginia has the most trail magic.
            - The mid-atlantic states have consistent and similar trail magic counts.  
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - Trail angels can decide which states might be in more need of trail magic overall.  
            - High trail magic frequency can overlap with heavily trafficked or accessible areas. This helps planners understand where most hikers congregate with support available.
            """)


with tabs[2]:
    st.header("Trail Magic Occurences per Mile in Each State 💫")
    st.subheader("Click on the next tab to see the trail magic per mile for every year!")
    col1, col2 = st.columns([2,1])
    with col1:
        with open("trail_magic_per_mile_map.html", "r", encoding="utf-8") as file:
            map_html = file.read()
        components.html(map_html, height=600, scrolling=True)

    with col2:
        with st.container(border=True):
            st.subheader("Map Explanation:")
            st.write("This map displays how much trail magic occurs in each of the 14 states on the trail. Trail magic refers to acts of kindness towards hikers, including finding food or shelters with the help of strangers or other hikers. Zoom into the map to view which states contain the most trail magic per mile. The darker the blue, the more magical the state is! The markers provide information about the total trail mileage in each state, as well.")

            st.subheader("Key Insights:")
            st.markdown("""
            - West Virginia has the most trail magic per mile. There is only 4 miles on the trail, so it has a high ratio due to this. 
            - North Carolina has the second most trail magic per mile at 27.271, which is a better state to analyze since it has nearly 100 trail miles. 
            - The northern states have much less trail magic per mile, averaging between 5 and 6.  
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - A high per-mile trail magic ratio can reflect deep community support and easy accessibility to the trail via road crossings or town proximity, which can guide future trailhead or shelter development.
            - High trail magic frequency can overlap with heavily trafficked or accessible areas. This helps planners understand where most hikers congregate with support available.
            - Hikers can plan and prepare for their trip with necessary supplies knowing how much trail magic is available in each state. For example, northern states may require more supplies.
            """) 

with tabs[3]:
    st.header("Interactive Trail Magic per Mile by Year 🔄")

    selected_year = st.selectbox("Select a year", list(range(2013, 2024)), index=10)

    df = pd.read_csv('CLEANED_CS6724_data_2013_2023.csv', encoding='ISO-8859-1', low_memory=False,
                     usecols=['Destination', 'Unique Interactions', 'Latitude', 'Longitude', 'year'])

    df = df[df['year'] == selected_year]
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df[df['Unique Interactions'].astype(str).str.contains("'trail magic'", na=False)]

    trail_states = ["Georgia", "North Carolina", "Tennessee", "Virginia", "West Virginia",
                    "Maryland", "Pennsylvania", "New Jersey", "New York", "Connecticut",
                    "Massachusetts", "Vermont", "New Hampshire", "Maine"]

    trail_miles = {
        "Georgia": 79, "North Carolina": 96, "Tennessee": 293, "Virginia": 554, "West Virginia": 4,
        "Maryland": 41, "Pennsylvania": 229, "New Jersey": 72, "New York": 88, "Connecticut": 52,
        "Massachusetts": 90, "Vermont": 150, "New Hampshire": 161, "Maine": 282
    }

    states = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")
    states = states[states["name"].isin(trail_states)].copy()

    geometry = [Point(lon, lat) for lon, lat in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
    gdf = gpd.sjoin(gdf, states, how="left", predicate='within')
    df['State'] = gdf['name']
    df = df.dropna(subset=['State'])

    state_counts = df.groupby('State').size().reset_index(name='Trail Magic Count')
    state_counts["Trail Miles"] = state_counts["State"].map(trail_miles)
    state_counts["Trail Magic per Mile"] = state_counts["Trail Magic Count"] / state_counts["Trail Miles"]
    states = states.merge(state_counts, left_on='name', right_on='State', how='left')
    states["Trail Magic per Mile"] = states["Trail Magic per Mile"].fillna(0)

    m = folium.Map(location=[39.5, -77.5], zoom_start=5, tiles='OpenStreetMap')
    folium.Choropleth(
        geo_data=states.to_json(),
        name="Trail Magic per Mile",
        data=states,
        columns=["name", "Trail Magic per Mile"],
        key_on="feature.properties.name",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name="Trail Magic Events per Mile",
        highlight=True
    ).add_to(m)

    folium.GeoJson(
        states,
        tooltip=folium.GeoJsonTooltip(
            fields=["name", "Trail Magic Count", "Trail Miles", "Trail Magic per Mile"],
            aliases=["State: ", "Trail Magic Count: ", "Trail Miles: ", "Per Mile: "],
            localize=True
        )
    ).add_to(m)

    m.get_root().html.add_child(folium.Element(
        f"<h4 align='center' style='font-size:18px;'>Trail Magic per Mile in {selected_year}</h4>"
    ))

    st_data = st_folium(m, width=1000, height=600)



with tabs[4]:
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
            st.write("This map displays the negative emotions that have been recorded on the trail. It specifically maps sadess, disgust, anger, and fear, which were expressed via journal entries from the hikers. Zoom into the map to view the individual emotion markers. Hovering over a marker will provide which emotion it corresponds to since the trail is densely packed with markers. NOBO refers to north bound hikers.")

            st.subheader("Key Insights:")
            st.markdown("""
            - The most common negative emotion expressed on the trail seems to be fear.
            - There are clusters of sadness in the southern part of the trail. 
            - There is a lack of disgust and anger across the trail.   
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - Hikers can mentally prepare for more emotionally intensive areas of the trail. 
            - Hikers can aniticipate challenginering areas of the trail. 
            """) 



with tabs[5]:
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
            st.write("This map displays the negative emotions that have been recorded on the trail. It specifically maps sadess, disgust, anger, and fear, which were expressed via journal entries from the hikers. Zoom into the map to view the individual emotion markers. Hovering over a marker will provide which emotion it corresponds to since the trail is densely packed with markers. SOBO refers to south bound hikers.")

            st.subheader("Key Insights:")
            st.markdown("""
            - The most common negative emotions expressed on the trail are fear and sadness.
            - In comparison to the NOBO map, the emotions are much more varied.  
            - There is less amount of fearness among SOBO hikers than NOBO hikers.  
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - Hikers can mentally prepare for more emotionally intensive areas of the trail. 
            - Hikers can aniticipate challenginering areas of the trail. 
            """) 
