import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

st.title("ESG and Financial Performance Dashboard")

Top_100_Tech_Final = pd.read_excel("Top_100_Tech_Final.xlsx")
with st.expander("Data Preview"):
    st.dataframe(Top_100_Tech_Final)
#st.divider()
#-----------

tab1, tab2 = st.tabs(["ESG Analysis", "Financial Trends"])

# Plotting Change in ESG Scores
# 1.
def per_change_esg():
    esg_2018 = Top_100_Tech_Final[Top_100_Tech_Final['Year'] == 2018][['Ticker Symbol', 'ESG Score']]

    esg_2021 = Top_100_Tech_Final[Top_100_Tech_Final['Year'] == 2021][['Ticker Symbol', 'ESG Score']]

    esg_change = esg_2018.merge(esg_2021, on='Ticker Symbol', how='inner')

    esg_change['ESG Score Change (%)'] = ((esg_change['ESG Score_y'] - esg_change['ESG Score_x']) / esg_change['ESG Score_x']) * 100

    esg_change_sorted = esg_change.sort_values(by='ESG Score Change (%)', ascending=True)
    # Show the dataframe in Streamlit
    #st.subheader("Percentage Change in ESG Scores from 2018 to 2021:")

    chart = alt.Chart(esg_change_sorted).mark_bar().encode(
        x='ESG Score Change (%):Q',
        y=alt.Y('Ticker Symbol:N', sort=alt.SortField(field='ESG Score Change (%)', order='descending')),
        color='ESG Score Change (%):Q',
        tooltip=['Ticker Symbol:N', 'ESG Score Change (%):Q']
    ).properties(
        title = 'Percentage Change in ESG Scores from 2018 to 2021',
        width=1000,
        height=1000
    )

    # Display the chart using Streamlit
    st.altair_chart(chart)
#per_change_esg()
#st.divider()

#-----------
# Plotting ESG Scores for each company
# 2.
def esg_score_trends():
    #st.subheader("ESG Score Trends (2018-2021)")
    selected_company = st.selectbox("Select a Company", Top_100_Tech_Final["Ticker Symbol"].unique(), key ='esg_score_2018-2021')

    # Filter the data based on the selected company
    filtered_data = Top_100_Tech_Final[Top_100_Tech_Final["Ticker Symbol"] == selected_company]

    # Create a line chart for ESG Score trends
    fig = px.line(filtered_data, x="Year", y="ESG Score", 
                title=f"ESG Score Trend for {selected_company}", 
                markers=True)

    # Display the chart
    st.plotly_chart(fig)
#esg_score_trends()
#st.divider()

#----------
# Plotting ESG Scores compared to Revenue
# 3.
def esg_vs_revenue():
    fig = px.scatter(Top_100_Tech_Final, x="Revenue", y="ESG Score",
                 size="Market Capitalization", color="TobinQ",
                 hover_name="Ticker Symbol", title="ESG Score vs Revenue (Bubble Chart)")
    st.plotly_chart(fig)
#esg_vs_revenue() 
#st.divider()

#----------
# Comparing ESG Score Pillar Comparison to Revenue
# 4.
def esg_pillar_comparison():

    company = st.selectbox("Select a Company", Top_100_Tech_Final["Ticker Symbol"].unique(), key = 'esg_pillar_scores')
    company_data = Top_100_Tech_Final[Top_100_Tech_Final["Ticker Symbol"] == company].iloc[-1]

    categories = ['Environmental Pillar Score', 'Social Pillar Score', 'Governance Pillar Score']
    values = [company_data[c] for c in categories]

    fig = px.line_polar(r=values, theta=categories, line_close=True, title=f"ESG Pillar Breakdown: {company}")

    fig.update_traces(line=dict(width=3, color="royalblue"), marker=dict(size=8, symbol="circle", color="red"))
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            showline=True, linewidth=2,  # Change grid color
            tickfont=dict(color="black"),  # Axis label color
        ),
        angularaxis=dict(  # Category label color
            showline=True, linewidth=2, linecolor="black",  # Axis line color
        )
    )
)

# Display in Streamlit
    st.plotly_chart(fig)
#esg_pillar_comparison()
#st.divider()

#----------
# ESG Score vs Tobin's Q 
# 5.
def esg_vs_tobinQ():
    fig = px.scatter(Top_100_Tech_Final, x="ESG Score", y="TobinQ",
                 color="Market Capitalization", size="Revenue",
                 hover_name="Ticker Symbol", title="ESG Score vs. Tobin's Q")
    st.plotly_chart(fig)
#esg_vs_tobinQ()
#st.divider()

#----------
# Market Capitalization Growth
# 6.
def market_cap_growth():
    selected_company = st.selectbox("Select a Company", Top_100_Tech_Final["Ticker Symbol"].unique(), key ='market cap growth')

    # Filter the data based on the selected company
    filtered_data = Top_100_Tech_Final[Top_100_Tech_Final["Ticker Symbol"] == selected_company]

    fig = px.area(filtered_data, x="Year", y="Market Capitalization",
              color="Ticker Symbol", title="Market Capitalization Growth (2018-2021)")
    st.plotly_chart(fig)
#market_cap_growth()
#st.divider()

#---------
# Company Insights
def company_insights():
    selected_years = st.multiselect("Select Years", [2018, 2019, 2020, 2021], default=[2018, 2021])
    filtered_df = Top_100_Tech_Final[Top_100_Tech_Final["Year"].isin(selected_years)]

with tab1:
    st.subheader("ESG Score Trends")
    esg_score_trends()  # ESG Score Trends Line Chart
    per_change_esg()  # ESG Score Change Bar Chart
    esg_pillar_comparison()  # ESG Pillar Radar Chart

with tab2:
    st.subheader("Financial Performance")
    esg_vs_revenue()  # ESG Score vs Revenue Bubble Chart
    market_cap_growth()  # Market Cap Growth Area Chart
    esg_vs_tobinQ()  # ESG Score vs Tobin’s Q Scatter Plot
