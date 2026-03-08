import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="🌍 COVID-19 Dashboard", layout="wide")

st.title("🌍 COVID-19 Interactive Dashboard")

# ------------------ Helper Functions ------------------ #
@st.cache_data
def get_country_list():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url).json()
    return sorted([country['country'] for country in response])

@st.cache_data
def get_country_data(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    return requests.get(url).json()

@st.cache_data
def get_historical_data(country):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=all"
    response = requests.get(url).json()
    
    # Use 'timeline' key if exists, otherwise fallback
    timeline = response.get('timeline', response)
    
    # Convert timeline dictionaries to DataFrame
    df = pd.DataFrame(timeline)
    
    # Create Series safely, with fallback to empty dict if key missing
    cases = pd.Series(df.get('cases', {})).rename("Cases")
    deaths = pd.Series(df.get('deaths', {})).rename("Deaths")
    recovered = pd.Series(df.get('recovered', {})).rename("Recovered")
    
    hist_df = pd.concat([cases, deaths, recovered], axis=1)
    
    # Convert index to datetime, ignore parsing errors
    hist_df.index = pd.to_datetime(hist_df.index, errors='coerce')
    hist_df = hist_df.dropna()
    
    return hist_df

@st.cache_data
def get_top10_countries(sort_by='cases'):
    url = "https://disease.sh/v3/covid-19/countries"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df = df[['country', 'cases', 'deaths', 'active', 'population']].sort_values(by=sort_by, ascending=False)
    return df.head(10)

# ------------------ Sidebar ------------------ #
st.sidebar.title("Select a Country")
country_list = get_country_list()
selected_country = st.sidebar.selectbox("Country", country_list)

# ------------------ Main Dashboard ------------------ #
# Current Statistics
data = get_country_data(selected_country)

st.subheader(f"Statistics for {selected_country}")
col1, col2, col3 = st.columns(3)
col1.metric("Population", f"{data.get('population', 0):,}")
col2.metric("Total Cases", f"{data.get('cases', 0):,}", f"+{data.get('todayCases', 0):,}")
col3.metric("Total Deaths", f"{data.get('deaths', 0):,}", f"+{data.get('todayDeaths', 0):,}")

col4, col5, col6 = st.columns(3)
col4.metric("Total Recovered", f"{data.get('recovered', 0):,}", f"+{data.get('todayRecovered', 0):,}")
col5.metric("Active Cases", f"{data.get('active', 0):,}")
col6.metric("Critical Cases", f"{data.get('critical', 0):,}")

st.write(f"Tests Conducted: {data.get('tests', 0):,}")

# ------------------ Top 10 Countries ------------------ #
st.subheader("Top 10 Countries by Total Cases")
top_cases = get_top10_countries('cases')
st.dataframe(top_cases[['country', 'cases', 'deaths', 'active']])

st.subheader("Top 10 Countries by Active Cases")
top_active = get_top10_countries('active')
st.dataframe(top_active[['country', 'cases', 'deaths', 'active']])

# ------------------ Historical Data ------------------ #
st.subheader(f"Historical COVID-19 Data for {selected_country}")
hist_df = get_historical_data(selected_country)

if not hist_df.empty:
    fig = px.line(
        hist_df,
        x=hist_df.index,
        y=['Cases', 'Deaths', 'Recovered'],
        labels={'value': 'Count', 'index': 'Date', 'variable': 'Metric'},
        title=f"COVID-19 Trends for {selected_country}"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Historical data not available for this country.")