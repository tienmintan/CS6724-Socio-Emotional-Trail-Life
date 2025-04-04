import streamlit as st
import folium
from streamlit_folium import st_folium

# Path to the pre-generated Folium map
MAP_PATH = "bar_chart.html"

# App Title
st.title("📍 Social Interactions by Year and Month")
st.subheader("📊 Stacked Bar Chart & Line Chart")
st.write("Visualizing social interactions across different years and months.")

# Explanation of the Graph
st.markdown("""
### 📌 **What This Visualization Shows**
- **Stacked Bar Chart:** Each year’s bar is divided into 12 colored segments, representing different months.
- **Legend:** Shows the colors corresponding to each month.
- **Trends:** Helps in analyzing how social interactions vary across different months and years.
""")

# Key Insights
st.markdown("""
## 🔍 **Key Insights from the Data**
1️⃣ **Interaction Trends Over Time:**  
   - 2020 had the lowest total interactions, while 2023 had the highest.  
   - **June and July** have the highest interaction counts, while **December and January** have the lowest.  
   - This suggests that social interactions peak during the summer, making it the best time for activities like hiking.

2️⃣ **Monthly Interaction Trends:**  
   - Interactions start increasing from **April (spring)**, peaking in **June & July (summer)**.  
   - A decline begins in **September**, reaching the lowest levels in **December & January** (winter).  

3️⃣ **Category-Based Social Interactions:**  
   - **Couples** have the highest interaction levels, followed by **families**.  
   - **Fest** has the lowest social interaction levels across all months.  
""")

# Data Source
st.markdown("📊 **Data Source:** Hiking Trail Social Interactions Dataset (2020-2024)")

# Load and display the Folium map
with open(MAP_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=600, scrolling=True)
