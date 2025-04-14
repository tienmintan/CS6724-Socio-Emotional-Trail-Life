import streamlit as st

st.set_page_config(
    page_title="Welcome",  
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Analysis of the Socio-Emotional Journey of Long-distance Hikers on the Appalachian Trail")  
st.sidebar.success("Select a page above.")

# Emotional Journey Intro + Map Thumbnails
st.markdown("<h2 style='text-align: center;'>🥾 Welcome to the Emotional Landscape of the Appalachian Trail</h2>", unsafe_allow_html=True)

st.markdown("""
> *“Thousands of miles, countless steps, and a rollercoaster of emotions.”*

The Appalachian Trail is more than a physical journey—it's an emotional odyssey through forests, friendships, and fatigue. 
Long-distance hikers often share their stories online, posting blog entries that capture their mental highs and lows across the 2,190+ mile trek.

In this project, we explore how emotional well-being is shaped by **social interactions**, **geographical locations**, and **trail conditions**. 
By using **AI-driven sentiment analysis** on a decade of hiker journal entries, we uncover where hikers felt joy, where they struggled, 
and how “trail magic”—unexpected kindness—lifted spirits along the way.
""", unsafe_allow_html=True)

# What You Can Explore
st.markdown("### 🔍 What You’ll Find Inside")
st.markdown("""
- 🗺️ **Emotion Maps**: Visuals showing emotional highs and lows across the trail  
- ✨ **Trail Magic Maps**: Acts of kindness, by location and per mile  
- 📊 **Best Campsites**: The most and least enjoyable places to rest  
- 🔄 **Direction Matters**: How NOBO vs SOBO hikers experience the trail differently  
""")

# Preview Thumbnails or Example Visuals
col3, col4 = st.columns(2)
with col3:
    st.image("emotion_map_thumn.png", caption="Trail Magic along the way", use_container_width=True)
with col4:
    st.image("inter_dist.png", caption="Social interactions distribution", use_container_width=True)

# Project Description Section
st.markdown("---")
cont1 = st.container()
cont1.header("Project Description")

cont2 = st.container(border=True)
with cont2:
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://images.unsplash.com/photo-1558483754-4618fc25fe5e?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)

    with col2:
        st.markdown(
        """
        <div style="font-size: 20px;">
        Emotional well-being is vital for individuals experiencing a life transition journey, 
        as it helps them maintain resilience, stay focused, and inform their decision-making. 

        Given the increasing integration of technology into everyday life, even in natural settings, 
        individuals share their experiences in online media, especially community-centered platforms. 

        For instance, Appalachian Trail long-distance hikers share their adventurous and emotional journey 
        through community blogs, necessitating an understanding of contributing factors to their emotions. 

        This project explores how social connections relate to hikers' emotional states amidst the uncertainties 
        of a dynamic socio-technical-natural system by leveraging AI-driven techniques and machine learning 
        algorithms on large-scale data.
        </div>
        """, unsafe_allow_html=True
    )

# Optional CTA or Footer
st.markdown("---")
st.markdown("<h4 style='text-align:center;'>🌄 Dive in to explore the hidden emotional patterns of the Appalachian Trail</h4>", unsafe_allow_html=True)
