import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def load_dataCaseGrowth():
    df = pd.read_csv('US_CovidCasesGrowth.csv', index_col='submission_date')
    return df

def load_dataDeaths():
    df = pd.read_csv('US_TotalCovidDeaths_perDay.csv', index_col='submission_date')
    return df

def load_vaccination():
    df = pd.read_csv('Vaccination.csv', index_col='State')
    return df

def load_data_covid():
    df = pd.read_csv('covid-data.csv', index_col='Province_State')
    return df


def load_dataCases():
    df = pd.read_csv('US_TotalCovidCases_perDay.csv', index_col='submission_date')
    return df


dfgrowth = load_dataCaseGrowth()
dfcovid = load_data_covid()
dfvaccine = load_vaccination()
dfcase = load_dataCases()
dfdeath = load_dataDeaths()


st.title('Visual Anaylsis Project')

welcome = ("""
### Application represent the Data anyslsis of covid trends in US.
""")

st.write(welcome)


st.sidebar.title("Covid19 Dashboard")
dashOptions = st.sidebar.selectbox("Select the Sub Menu Options from Dropdown:",
('Vacination Comparison', 'Deaths Tracker', 'New Cases', 'Comparison Rates(CDR)'))

st.header(dashOptions)


cols = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
'Kentucky', 'Louisiana', 'Maine', 'Maryland',
'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York','North Carolina', 'North Dakota','Ohio',
'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

if dashOptions == 'Vacination Comparison':
    cols_c = ['Janssen','Moderna','Pfizer']
    option_selectbox = st.sidebar.multiselect('Select a Multi Manufacturers:', cols_c, cols_c[1], key=4)
    df2 = dfvaccine.reset_index()
    multi_lc2 = alt.Chart(df2).transform_fold(
    option_selectbox,
    ).mark_bar().encode(
    y=alt.X('value:Q', title='Total Vacination Numbers'),
    x='State:N',
    color='key:N',
    ).properties(
    width=850,
    height=800
    ).interactive()
    st.write(multi_lc2)



if dashOptions == 'Comparison Rates(CDR)':
    st.write("Bar Chart Depicts the Comparision Rates of Confirm ,Deaths,Recovered")
    cols_catagories = ['Deaths','Recovered','Confirmed']
    st.bar_chart(dfcovid[cols_catagories], width=10000, height=800)
    
if dashOptions == 'Deaths Tracker':
    option = st.sidebar.multiselect('Which state(s) do you want in track?', cols, cols[39])
    df = dfcase.reset_index()
    df1 = dfdeath.reset_index()
    multi_lc = alt.Chart(df1).transform_fold(
    option,
    ).mark_circle(size =20).encode(
    x=alt.X('submission_date:T', title='Months'),
    y=alt.Y('value:Q', title='Deaths'),
    color='key:N',
    ).properties(
    title='Total Cases Deaths',
    width=600,
    height=400
    ).interactive()
    st.write(multi_lc)

if dashOptions == 'New Cases':
    option1 = st.sidebar.multiselect('Select a state(s):', cols, cols[39], key=1)
    df = dfgrowth.reset_index()
    multi_s = alt.Chart(df).transform_fold(
    option1,
    ).mark_circle(size=20).encode(
    x=alt.X('submission_date:T', title='Date'),
    y=alt.Y('value:Q', title='Cases'),
        color='key:N',
    ).properties(
    title='New Cases per Day',
    width=700,
    height=600
    ).interactive()
    st.write(multi_s)
