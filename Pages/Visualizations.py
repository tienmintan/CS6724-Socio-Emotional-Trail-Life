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
    st.markdown("# **Content for Afreen**")
    st.write("Afreen's detailed information here.")
elif selected_tab == "Shamsia":
    st.markdown("# **Content for Shamsia**")
    st.write("Shamsia's detailed information here.")
elif selected_tab == "Emily":
    st.markdown("# **Content for Emily**")
    st.write("Emily's detailed information here.")
elif selected_tab == "Krish":
    st.markdown("# **Content for Krish**")
    st.write("Krish's detailed information here.")
elif selected_tab == "Tien Man":
    st.markdown("# **Content for Tien Man**")
    st.write("Tien Man's detailed information here.")