import streamlit as st

from test2 import show_map
from test import show_data
from test3 import show_home

menu=st.sidebar.selectbox(
    "메뉴 선택",
    ["홈", "데이터", "지도"]
)

if menu == "홈":
    show_home()

elif menu == "데이터":
    show_data()

elif menu == "지도":
    show_map()