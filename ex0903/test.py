import streamlit as st
import numpy as np
import pandas as pd

def show_data():
    st.title("데이터")

    dataframe = pd.DataFrame(
        np.random.randn(40,40),
        columns=("col %d" % i for i in range(40))
    )

    st.dataframe(dataframe.style.highlight_min(axis=0))