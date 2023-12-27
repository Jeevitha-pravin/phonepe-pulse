import os
import json
import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

# Setting up page configuration
icon = Image.open("icon.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization And Exploration",
                    page_icon=icon,
                    layout= "wide",
                    initial_sidebar_state= "expanded",
                    menu_items={'About': """Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

mydb = mysql.connector.connect(
host="localhost",
user="root",
password=""
)
print(mydb)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("use phonepe_data")
mydb.commit()

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    st.image("image.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("image2.jpg")
        
# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 States, Districts, Pincodes based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 States, Districts, Pincodes based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select states as states, sum(Transaction_count) as Transactions_Count, sum(Transaction_amount) as Total_amount from aggregated_transaction where years = {Year} and Quarter = {Quarter} group by states order by Total_amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['states','Transactions_Count','Total_amount'])
            fig = px.pie(df, values='Total_amount',
                            names='states',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select Districts as Districts , sum(Transaction_count) as Transactions_Count, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and Quarter = {Quarter} group by Districts order by Total_amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Districts', 'Transactions_Count','Total_amount'])

            fig = px.pie(df, values='Total_amount',
                            names='Districts',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincodes as Pincodes, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total_amount from top_transaction where years = {Year} and Quarter = {Quarter} group by Pincodes order by Total_amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincodes', 'Transactions_Count','Total_amount'])
            fig = px.pie(df, values='Total_amount',
                                names='Pincodes',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select Brands as Brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from aggregated_user where years = {Year} and Quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'Total_Count','Avg_Percentage'])
                fig = px.bar(df,
                                title='Top 10',
                                x="Total_Count",
                                y="Brands",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)
                
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select Districts as Districts, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and Quarter = {Quarter} group by Districts order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Districts', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Districts",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincodes as Pincodes, sum(RegisteredUser) as Total_Users from top_user where years = {Year} and Quarter = {Quarter} group by Pincodes order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincodes', 'Total_Users'])
            fig = px.pie(df,
                            values='Total_Users',
                            names='Pincodes',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select states, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and Quarter = {Quarter} group by states order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select states, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and Quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['states', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('states.csv')
            df1.states=df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='states',
                                    color='Total_amount',
                                    color_continuous_scale='sunset')
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select states, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and Quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['states', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('states.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.states = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='states',
                        color='Total_Transactions',
                        color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
    # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from aggregated_transaction where years= {Year} and Quarter = {Quarter} group by Transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                        title='Transaction Types vs Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
            
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                ('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                                'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat','Haryana',
                                'Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                                'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                                'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                                'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'),index=30)
        mycursor.execute(f"select states, Districts,years,Quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and Quarter = {Quarter} and states = '{selected_state}' group by states, Districts,years,Quarter order by states,Districts")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['states','Districts','years','Quarter','Total_Transactions','Total_amount'])

        fig = px.bar(df1,
                        title=selected_state,
                        x="Districts",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)


# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select states, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and Quarter = {Quarter} group by states order by states")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['states', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('states.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.states = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='states',
                    color='Total_Appopens',
                    color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any states to explore more]")
        selected_state = st.selectbox("",
                                ('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                                'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat','Haryana',
                                'Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                                'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                                'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                                'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'),index=30)

        mycursor.execute(f"select states,years,Quarter,Districts,sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and Quarter = {Quarter} and states = '{selected_state}' group by states, Districts,years,Quarter order by states,Districts")

        df = pd.DataFrame(mycursor.fetchall(), columns=['states','years', 'Quarter', 'Districts', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                        title=selected_state,
                        x="Districts",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("about1.jpg")


