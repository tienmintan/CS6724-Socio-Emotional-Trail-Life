import streamlit as st

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
    st.header("Best and Worst Spots in Each State")
    st.write("📍 ")

with tabs[1]:
    st.header("Trail Magic Occurences by State")
    st.write("🎒 ")

with tabs[2]:
    st.header("Negative Emotions Across the Trail")
    st.write("😞 ")
