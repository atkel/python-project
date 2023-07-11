import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title = "Heart Disease project",
                   page_icon = ":anatomical_heart:",
                   layout = "centered")

st.title("Heart Disease Dataset Analysis")
st.subheader("Group 3 - Instructor: Dr. Do Duc Tan")


# ----- Group member
col1, col2 = st.columns(2)
with col1:
    st.markdown("##")
    st.header("Group member:")
    st.write("Nguyen Yen Mai - 10622024")
    st.write("Vuong Binh Nguyen - 10322015")         
    st.write("Nguyen Phan Hoang Nhi - 10622030")        
    st.write("Nghiem Lam Thuy - 10622040")
    st.write("Duong Anh Thy - 10322029")
# ----- Animation
with col2:
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_data = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_49rdyysj.json")
    st_lottie(lottie_data, loop = True)