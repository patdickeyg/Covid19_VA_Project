import streamlit as st
import pandas as pd
import altair as alt


# loading Data
@st.cache
def load_vaccination():
    df = pd.read_csv('Vaccination.csv', index_col='State')
    return df

def load_dataCases():
    df = pd.read_csv('US_TotalCovidCases_perDay.csv', index_col='submission_date')
    return df

def load_dataDeaths():
    df = pd.read_csv('US_TotalCovidDeaths_perDay.csv', index_col='submission_date')
    return df

def load_dataCaseGrowth():
    df = pd.read_csv('US_CovidCasesGrowth.csv', index_col='submission_date')
    return df

def load_data_covid():
    df = pd.read_csv('covid-data.csv', index_col='Province_State')
    return df

# load the data
dfvaccine = load_vaccination()
dfcase = load_dataCases()
dfdeath = load_dataDeaths()
dfgrowth = load_dataCaseGrowth()
dfcovid = load_data_covid()


# main points
st.title('COVID-19 Visual Anaylsis')

welcome = ("""
    ### Welcome! Use the panel on the left to navigate to different dashboards.
    
    Note: Data represents Covid trends in the United States
""")

st.write(welcome)



###dashboard options for the sidebar
st.sidebar.title("Covid19 Dashboard")
dashOptions = st.sidebar.selectbox("Select a Menu Option to display:", 
                                   ('Vaccination', 'Cases Tracker', 'New Cases', 'Comparison'))
    
# displays headers fore each dashboard
st.header(dashOptions)

# global variables
cols = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 
        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',            'New Mexico', 'New York','North Carolina', 'North Dakota','Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


# dashboard for bar chart comparisons
if dashOptions == 'Comparison':
    
    
    st.write("Bar Chart")
    
    cols_catagories = ['Confirmed','Deaths','Recovered']
    option_selectbox = st.sidebar.selectbox('Select a category:', cols_catagories)
    st.bar_chart(dfcovid[option_selectbox], width=800, height=500)
    
    
    st.write("Comparison Bar Chart with Specific Category")
    
    option_multiselect = st.sidebar.multiselect('Select one to more categories:', cols_catagories, cols_catagories[0])
    st.bar_chart(dfcovid[option_multiselect], width=800, height=500)

  

# dashboard for tracking 
if dashOptions == 'Cases Tracker':
    
    option = st.sidebar.multiselect('Which state(s) do you want in track?', cols, cols[32])
   
    #chart for tracking covid cases
    df = dfcase.reset_index()
    
    multi_lc = alt.Chart(df).transform_fold(
    option,
    ).mark_line().encode(
    x=alt.X('submission_date:T', title='Date'),
    y=alt.Y('value:Q', title='Cases'),
    color='key:N',
    tooltip=['cols:Q']
    ).properties(
    title='Total Cases',
    width=600,
    height=400
    ).interactive()
    
    st.write(multi_lc)
    
    
    #chart for tracking covid deaths
    df1 = dfdeath.reset_index()
    
    multi_lc1 = alt.Chart(df1).transform_fold(
    option,
    ).mark_line().encode(
    x=alt.X('submission_date:T', title='Date'),
    y=alt.Y('value:Q', title='Death Toll'),
    color='key:N',
    tooltip=['value:Q']
    ).properties(
    title='Total Deaths',
    width=600,
    height=400
    ).interactive()
    
    st.write(multi_lc1)   
    
    
    
    
# dashboard for new cases
if dashOptions == 'New Cases':
    
    
    option1 = st.sidebar.multiselect('Select a state(s):', cols, cols[32],  key=1)
   

    df = dfgrowth.reset_index()  
    
    #Scatter plot comparisons
    multi_s = alt.Chart(df).transform_fold(
    option1, 
    ).mark_circle(size=20).encode(
    x=alt.X('submission_date:T', title='Date'),
    y=alt.Y('value:Q', title='Cases'),
    color='key:N',
    tooltip=['value:Q']
    ).properties(
    title='New Cases per Day',
    width=700,
    height=600
    ).interactive()
    st.write(multi_s)
    
    
    
# dashboard for new cases
if dashOptions == 'Vaccination':
    
    cols_c = ['Janssen','Moderna','Pfizer', 'Other MF']
    option_selectbox = st.sidebar.multiselect('Select a Vaccine Manufacturer(s):', cols_c, cols_c[2], key=4)
    
    df2 = dfvaccine.reset_index()
    
    multi_lc2 = alt.Chart(df2).transform_fold(
    option_selectbox,
    ).mark_bar().encode(
    x=alt.X('value:Q', title='Doses'),
    y='State:N',
    color='key:N',
    tooltip=['Janssen:Q', 'Moderna:Q', 'Pfizer:Q', 'Other MF:Q']
    ).properties(
    title='Vaccines Administered per State',
    width=700,
    height=700
    ).interactive()
    
    st.write(multi_lc2)





