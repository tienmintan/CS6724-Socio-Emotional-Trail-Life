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
    
