import streamlit as st
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import csv

st.set_page_config(page_title="Customer Risk Dashboard",layout="wide")

# Page header
st.title("Customer Risk Dashboard")

@st.experimental_singleton
def init_connection():
   return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
   with conn.cursor() as cur:
       cur.execute(query)
       return cur.fetchall()

# Query Snowflake for features and predictions
data = run_query("SELECT ds.*, p.churn_prediction, p.churn_true_prediction_score from [database name].customerchurn.telco_info ds left join [database name].customerchurn.MODEL_CUSTOMER_CHURN_30DAYS_PREDICTIONS p using (id)")

# Create dataframe of features and predictions
df = pd.DataFrame(data, columns=["CustomerID", "State", "CustomerAge", "Area_Code", "International_Plan",
"Voicemail_Plan", "Voicemail_Messages", "Total_Day_Minutes", "Total_Day_calls", "Total_Day_Charge",
"Total_Eve_Minutes", "Total_Eve_Calls", "Total_Eve_Charge", "Total_Night_Minutes", "Total_Night_Calls",
"Total_Night_Charge","Total_Intl_Minutes", "Total_Intl_Calls", "Total_Intl_Charge", "Number_Customer_Service_Calls",
"Churn", "Churn_Prediction", "Churn_True_Prediction_Score"])

# Edit data
df['Area_Code'] = df.Area_Code.str[10:]

# Add a fictitious customer monthly spend to the dataframe
df['Monthly_Spend'] = 75

# Settings section
with st.sidebar:
    st.title("Data Settings")

    # Filter data by the customer's probability of churn
    threshold = st.slider('Set Churn Probability Threshold', 0.0, 1.0,(0.4, 0.8))

    # Filter data by account plan
    plan = st.radio('Choose plan', ['Both','Domestic','International'])

    # Filter by State
    states = st.multiselect("Select states", df['State'].unique(), default=df['State'].unique())

    # create an adjusted dataframe based on the user's settings
    if plan == 'Both':
        adjusted_df = df.loc[(
            (df['Churn_True_Prediction_Score'] >= threshold[0])
            &
            (df['Churn_True_Prediction_Score'] <= threshold[1])
            &
            (df['State'].isin(states))
        )]
    else:
        adjusted_df = df.loc[(
            (df['Churn_True_Prediction_Score'] >= threshold[0])
            &
            (df['Churn_True_Prediction_Score'] <= threshold[1])
            &
            (df['International_Plan'] == 'yes' if plan == "International" else df['International_Plan'] == 'no')
            &
            (df['State'].isin(states))
        )]

# Create columns for each metric to display horizontally
churn_col, net_retention_rate_col, monthly_revenue_col = st.columns(3)

with churn_col:
   # Count how many customers in the adjusted dataframe are within the churn prediction threshold
    st.metric("Customers Predicted to Churn",
    adjusted_df.CustomerID.count())


with net_retention_rate_col:
   # Calculate and display the net retention rate
   # Monthly Net Retention Rate = (Recurring Revenue + (Expansion Revenue - Lost Revenue) / Recurring Revenue
   monthly_recurring_rev = df.Monthly_Spend.sum()
   monthly_expansion_rev = monthly_recurring_rev*0.0415
   monthly_lost_rev = adjusted_df.Monthly_Spend.sum()
   net_retention_rate = (monthly_recurring_rev+monthly_expansion_rev-monthly_lost_rev)/monthly_recurring_rev
   st.metric("Forecasted Net Retention Rate", "{:.1%}".format(net_retention_rate))

with monthly_revenue_col:
   # Revenue impact if the customers predicted to churn actually churn
   st.metric("Forecasted Monthly Revenue Impact", "${:,.2f}".format(monthly_lost_rev))


st.header("Customers at risk of churning")
sorted_df = adjusted_df.sort_values(by='Churn_True_Prediction_Score', ascending=False)
sorted_df.insert(0, 'Probability of Churn', sorted_df.pop('Churn_True_Prediction_Score'))
st.dataframe(sorted_df.iloc[:, 0:21])

st.write(" ")

graph_col1, graph_col2 = st.columns(2)
with graph_col1:
   # Count the number of customers likely to churn in each category of customer service contact
   cust_service_calls = adjusted_df.groupby(by='Number_Customer_Service_Calls').count().reset_index()

   fig, ax = plt.subplots()
   ax.bar(cust_service_calls.Number_Customer_Service_Calls, cust_service_calls.CustomerID, color = 'red', label='Customers')
   ax.set_xlabel("Customer Service Calls")
   ax.set_ylabel("Customers predicted to Churn")
   plt.title("Calls with customer service calls by at-risk customers")
   st.pyplot(fig)

with graph_col2:
   # Churned customers with an International plan versus domestic plan
  
   fig2, ax2 = plt.subplots()
   ax2.bar(['International', 'Domestic'], [adjusted_df[(adjusted_df.International_Plan=='yes')].CustomerID.count(), adjusted_df[(adjusted_df.International_Plan=='no')].CustomerID.count()] , color = 'red')
   ax2.set_xlabel("Account Plan")
   ax2.set_ylabel("Customers predicted to Churn")
   plt.title("Number of Churned customers per account plan")
   st.pyplot(fig2)

st.header("Customers predicted to Churn by State")

# Read in data of states and their capitol's longitude and latitude
with open('state_capitol_coordinates.csv', mode='r') as myfile:
    reader = [rows for rows in csv.reader(myfile)]

    latitude = {rows[2]:rows[0] for rows in reader} 
    longitude = {rows[2]:rows[1] for rows in reader}
    adjusted_df['latitude']=adjusted_df['State'].map(latitude).astype("int")
    adjusted_df['longitude']=adjusted_df['State'].map(longitude).astype("int")

st.map(adjusted_df, 2)

