import streamlit as st

from test3 import show_home
from test import show_data
from test2 import show_map

page1 = st.Page(show_home, title="홈", default=True)
page2 = st.Page(show_data, title="데이터")
page3 = st.Page(show_map, title="지도")

pg = st.navigation([page1, page2, page3])

pg.run()