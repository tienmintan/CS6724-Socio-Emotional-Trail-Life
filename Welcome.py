import streamlit as st

st.set_page_config(
    page_title="Welcome",  
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Analysis of the Socio-Emotional Journey of Long-distance Hikers on the Appalachian Trail")  
st.sidebar.success("Select a page above.")

col1, col22 = st.columns([1, 2])

with col1:
    st.header("Project Description")

with col2:
    st.write("""
    Emotional well-being is vital for individuals experiencing a life transition journey, 
    as it helps them maintain resilience, stay focused, and inform their decision-making. 

    Given the increasing integration of technology into everyday life, even in natural settings, 
    individuals share their experiences in online media, especially community-centered platforms. 

    For instance, Appalachian Trail long-distance hikers share their adventurous and emotional journey 
    through community blogs, necessitating an understanding of contributing factors to their emotions. 

    This project explores how social connections relate to hikers' emotional states amidst the uncertainties 
    of a dynamic socio-technical-natural system by leveraging AI-driven techniques and machine learning 
    algorithms on large-scale data.
    """)
    