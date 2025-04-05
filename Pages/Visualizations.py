import streamlit as st

st.set_page_config(
    page_title="Visualizations",  
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Visualizations Made By Our Team")  

tab_titles = [
    "Afreen",
    "Shamsia",
    "Emily",
    "Krish",
    "Tien Man"
]

selected_tab = st.sidebar.radio("Select a Team Member", tab_titles)

if selected_tab == "Afreen":
    st.markdown("## **Content for Afreen**")
elif selected_tab == "Shamsia":
    st.markdown("## **Content for Shamsia**")
elif selected_tab == "Emily":
    st.markdown("## **Content for Emily**")
elif selected_tab == "Krish":
    st.markdown("## **Content for Krish**")
elif selected_tab == "Tien Man":
    st.markdown("## **Content for Tien Man**")