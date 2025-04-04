import streamlit as st
import folium
from streamlit_folium import st_folium

# Load your pre-generated Folium map
map_path = "social_interactions_density.html"

st.title("📍 Social Interactions Heatmap")
st.write("Visualizing social interactions on hiking trails.")

# Brief Explanation of the Graph
st.markdown(
    """
    ### 🏕️ **What This Map Shows**
    - **Heatmap:** Warmer colors indicate higher densities of social interactions.
    - **Markers:** Represent specific interactions, color-coded by interaction type.
    - **Legend:** Displays interaction categories and their associated colors.
    
    Use this map to explore how social interactions vary across different hiking trails.
    """
)

# Insights Section
st.markdown("""
## 🔍 **Key Insights from the Visualization**
1️⃣ **High-Activity Zones:** Warmer colors indicate hotspots with frequent social interactions.  
2️⃣ **Common Social Activities:** Group hikes, meetups, and trail magic are the most observed interactions.  
3️⃣ **Trends Over Time:** Seasonal variations in social interactions can be explored using Interaction trends.  
4️⃣ **Isolated Points:** Some markers are distant from main trails, indicating either unique events or data anomalies.  
5️⃣ **Social Weight Impact:** Locations with higher weight values indicate stronger social bonds, such as family hikes.  

### 🥾 **Top Hiking Trails by Interaction Group**
**Group 1 (Campfire, Conversation, Share, Meet, Call, Together):**  
🥇 **Fulltilt** (624 interactions)  
🥈 **Skipper** (474 interactions)  
🥉 **Valley Forge** (456 interactions)  

**Group 2 (Couple, Family, Friend, Pet):**  
🥇 **Sev** (356 interactions)  
🥈 **Fulltilt** (312 interactions)  
🥉 **Finder** (308 interactions)  

**Group 3 (Magic, Trail Magic, Trail Angel):**  
🥇 **Fulltilt** (312 interactions)  
🥈 **Sev** (267 interactions)  
🥉 **MoJoe** (249 interactions)  

**Group 4 (Fest, Festival, Event, Community, Trail Town):**  
🥇 **Valley Forge** (304 interactions)  
🥈 **Sev** (267 interactions)  
🥉 **MoJoe** (249 interactions)  
""")

# Footer
st.markdown("📊 **Data Source:** Hiking Trail Social Interactions Dataset (2013-2023)")

# Embed the Folium map
with open(map_path, "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=600, scrolling=True)
