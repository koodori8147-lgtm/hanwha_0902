import streamlit as st
import numpy as np
import pandas as pd

def show_map():
    st.title("지도")

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            np.random.randn(20,2),
            columns=["x", "y"])

    color = st.color_picker("Color", "#FF0000")

    st.scatter_chart(st.session_state.df, x="x", y="y", color=color)