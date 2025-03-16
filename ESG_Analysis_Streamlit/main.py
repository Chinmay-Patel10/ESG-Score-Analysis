import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Multi-Page App", layout="wide")


st.title("ESD Data Analysis")
st.header("Summary of Project")
st.write("This a ESG Score Analysis of over 100 tech companies. Data Visualization find important insights about ESG score and its affect on Revenue, Tobin Q, and Market Cap.")

Top_100_Tech_Final = pd.read_excel("Top_100_Tech_Final.xlsx")





