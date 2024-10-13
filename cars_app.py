# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 11:07:22 2023

@author: HP
"""
#data cols has changed from project 2 data-set to project 3
#engine = acceleration
#horse power = top speed
#lenght = load
#curb weight = weight
#latest date = launch date

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#st.set_option('deprecation.showPyplotGlobalUse', False) # to avoid warning in streamlit

#st.set_page_config(layout="wide")

# Set page title and icon
st.set_page_config(
    page_title="Car Data Analysis",
    page_icon="🚗",layout="wide"
)
#We are using Project 3 Data-Set
#df = pd.read_csv(r'C:\Users\HP\Desktop\streamlit\Project-2.3\Cars _data.csv')
df = pd.read_csv('Cars _data.csv')
st.set_option('deprecation.showPyplotGlobalUse', False) # suggestion by streamlit to remove warning on app,

#--------------------------Data Cleaning Process------------------------------#
a1=df.info()
a2=df.isna().sum()
a3=df['year_resale_value'].fillna(0,inplace = True)
a4=df['year_resale_value'].isna().any()

#Since our dataset have few missing value btw 1 to 3 except (year resale col) so we could drop null rows which won't effect the data
a5=df.dropna(inplace = True)
a6=df.isna().sum()

#Columns data types corrections:
a7=df['Fuel_efficiency']=df['Fuel_efficiency'].astype('int64')
a8=df['Top_Speed']=df['Top_Speed'].astype('int64')
a9=df['Launch_date']=pd.to_datetime(df['Launch_date'])

#we don't have any duplication on data set (i.e doesn't have any similar rows)
a10=df.duplicated().any()

#Checking if there any duplication on column.
a11=df[df['Model'].duplicated()]

a12=df[df['Model']=='Neon']

#They are the same company, (DaimlerChrysler),different 'brands'. 
#Cars like the Dodge Daytona and Plymouth Sundance were the same body style with different accessory packages.

a13=df.drop(index=[114], inplace= True )
a14=df[df['Model']=='Neon']
#-------------------------------END---------------------------------------#
# Now, Code for streamlit APP:-

with st.container():
    col1,col2= st.columns(spec=[0.7,0.3], gap="small")
    
    with col2:
        st.image("https://images.pexels.com/photos/2343508/pexels-photo-2343508.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        width=300,) # Manually Adjust the width of the image as per requirement)
    with col1:
# Set the title and subtitle of the Streamlit app
        st.title('Depending on your preferences, pick the ideal vehicle for you.')
        st.write('Exploratory Data Analysis of Automotive Dataset for car purchase')

# Sidebar with options
st.sidebar.title('Created by: Mr Saad Ahmed')
st.sidebar.header('Options')
selected_question = st.sidebar.selectbox(
    'Select a Question',
    ('Description', '1. Sales Distribution by Manufacturer', '2. Sales Trends Over the Years',
     '3a. Top 10 Models by Horsepower','3b. Bottom 10 Models by Horsepower', '4. Engine Size vs. Fuel Efficiency',
     '5. Average Price by Vehicle Type and Manufacturer', '6. Curb Weight by Vehicle Type',
     '7. Fuel Efficiency Distribution', '8. Engine Power vs. Body Length & Weight')
)

#showing Data-set
if selected_question == 'Description':
    st.subheader('Beta-Version')
    st.markdown('This project is based on automotive industry. The data collected could include information about sales figures, market trends, consumer preferences, and vehicle specifications. The analyst would use software tools to organize and manipulate the data, and then generate reports and visualizations to communicate key insights to stakeholders. The goal of this project would be to help automotive companies make informed decisions about their products, marketing strategies, and business operations, based on data-driven insights.')
    print('\n')
    st.markdown('Users of this Streamlit APP can access and examine data pertaining to cars and their features. Users can enter information about different car metrics, such as acceleration, speed, weight, and load, and the app creates visualizations to help users better understand the data and assist in helping the user make the best car purchase decision based on their preferences. Users can also download the report in PDF format.')

# Display data based on selected question
if selected_question == '1. Sales Distribution by Manufacturer':
    st.subheader('1. What is the distribution of Sales_in_thousands for each Manufacturer?')
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='Manufacturer', y='Sales_in_thousands')
    plt.xticks(rotation=90)
    plt.xlabel('Manufacturer')
    plt.ylabel('Sales_in_thousands')
    st.pyplot()

#For 2
elif selected_question == '2. Sales Trends Over the Years':
    st.subheader('2. How do Sales_in_thousands vary over the years?')
    plt.figure(figsize=(10, 3))
    sns.lineplot(x='Launch_date', y='Sales_in_thousands', data=df)
    plt.xlabel('Year')
    plt.ylabel('Sales_in_thousands')
    st.pyplot()

#For 3a
elif selected_question == '3a. Top 10 Models by Horsepower':
    st.subheader('3. What are the top 10 models with the highest Horsepower?')
    
    with st.container():
        col1,col2= st.columns(spec=[0.3,0.7], gap="medium")
        
        with col1:            
            top_horsepower_models = df.nlargest(10, 'Top_Speed')[['Model', 'Top_Speed']]
            st.table(top_horsepower_models)
            
        with col2:
            plt.figure(figsize=(5, 2))
            #For Highest
            top_horsepower_models = df.nlargest(10, 'Top_Speed').sort_values('Top_Speed', ascending=True)
            x1=top_horsepower_models['Model']
            y1=top_horsepower_models['Top_Speed']
            
            #plot graph by using matplotlib
            #plt.barh(x1, y1, color=sns.color_palette("Spectral",len(x1))) # color=red or any color for signal pattern
            
            sns.barplot(x=y1, y=x1, data=df,palette="YlGn")
            plt.gca().invert_yaxis()  # Invert y-axis to display the highest horsepower at the top
            plt.title('Top 10 Models with the Highest Horsepower')
            plt.xlabel('Horsepower')
            plt.ylabel('Model')
            plt.show()
            st.pyplot()

#For 3b
elif selected_question == '3b. Bottom 10 Models by Horsepower':
    st.subheader('3. What are the 10 models with the Lowest Horsepower?')
    
    with st.container():
        col1,col2= st.columns(spec=[0.3,0.7], gap="medium")
        
        with col1:            
            bottom_horsepower_models = df.nsmallest(10, 'Top_Speed')[['Model', 'Top_Speed']]
            st.table(bottom_horsepower_models)
            
        with col2:
            plt.figure(figsize=(5, 2))
            lowest_horsepower_models = df.nsmallest(10, 'Top_Speed').sort_values('Top_Speed', ascending=True)
            x2=lowest_horsepower_models['Model']
            y2=lowest_horsepower_models['Top_Speed']
           
            # Plotting a bar graph by using seaborn Lib, it's a advance version of Matplotlib
            sns.barplot(x=y2, y=x2, data=df,palette="autumn") # color=red or any color for signal pattern, i.e palette use for diff colors
            plt.gca().invert_yaxis()  # Invert y-axis to display the highest horsepower at the top
            plt.title('Top 10 Models with the lowest Horsepower')
            plt.xlabel('Horsepower')
            plt.ylabel('Model')
            plt.show()
            st.pyplot()

#For 4
elif selected_question == '4. Engine Size vs. Fuel Efficiency':
    st.subheader('4. How does Engine_size relate to Fuel_efficiency?')
    plt.figure(figsize=(10, 3))
    sns.scatterplot(x='acceleration', y='Fuel_efficiency', data=df)
    plt.xlabel('Engine_size')
    plt.ylabel('Fuel_efficiency')
    st.pyplot()

#For 5
elif selected_question == '5. Average Price by Vehicle Type and Manufacturer':
    st.subheader('5. What is the average Price_in_thousands by Vehicle Type and Manufacturer?')
    average_price_by_type_manufacturer = df.groupby(['Vehicle_type', 'Manufacturer'])['Price_in_thousands'].mean().unstack()
    st.write(average_price_by_type_manufacturer)

#For 6
elif selected_question == '6. Curb Weight by Vehicle Type':
    st.subheader('6. How does Curb_weight vary by Vehicle Type?')
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='Vehicle_type', y='Weight')
    plt.xlabel('Vehicle_type')
    plt.ylabel('Curb_weight')
    st.pyplot()

#For 7
elif selected_question == '7. Fuel Efficiency Distribution':
    st.subheader('7. What is the distribution of Fuel_efficiency?')
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Fuel_efficiency'], bins=20)
    plt.xlabel('Fuel_efficiency')
    plt.ylabel('Frequency')
    st.pyplot()

#For 8
elif selected_question == '8. Engine Power vs. Body Length & Weight':
    st.subheader('8. How does Engine_Power relate to Body Length & Weight?')
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='acceleration', y='Load', data=df)
    plt.xlabel('Engine_Power')
    plt.ylabel('Body Length & Weight')
    st.pyplot()
#----------------------------1st Part EDA END HERE-----------------------------------------#

def load_data():
    #data = pd.read_csv(r'C:\Users\HP\Desktop\streamlit\Project-2.3\Cars _data.csv')  # Replace with the path to your dataset
    data = pd.read_csv('Cars _data.csv')
    return data

data = load_data()

# (Sidebar)Create a sidebar for user input on left side:
st.sidebar.header("Car Preferences")

# (Sidebar) Range input fields for user preferences btw hight to low: Min,Max,Range,Jump
acceleration_range = st.sidebar.slider("Acceleration Range (0-60 Kph)", 0.0, 20.0, (0.0, 20.0), 0.1)
top_speed_range = st.sidebar.slider("Top Speed Range (Kph)", 0, 500, (0, 450), 1)
weight_range = st.sidebar.slider("Weight Range (tons)", 0, 6, (0, 6), 1)
load_range = st.sidebar.slider("Load Range", 0, 300, (0, 225), 1)

# Filter the dataset based on user preferences for make Table:
filtered_data = data[
    (data["acceleration"] >= acceleration_range[0]) & (data["acceleration"] <= acceleration_range[1]) &
    (data["Top_Speed"] >= top_speed_range[0]) & (data["Top_Speed"] <= top_speed_range[1]) &
    (data["Weight"] >= weight_range[0]) & (data["Weight"] <= weight_range[1]) &
    (data["Load"] >= load_range[0]) & (data["Load"] <= load_range[1])
]

#(Main) Display user preferences and filtered data
with st.container():
    col1,col2= st.columns(spec=[0.3,0.7], gap="small")
    
    with col1:
        st.subheader("User Preferences:")
        user_prefs = pd.DataFrame({
            "Preference": ["Acceleration", "Top Speed", "Weight", "Load"],
            "Range": [acceleration_range, top_speed_range, weight_range, load_range]
        })
        
        
        st.write(user_prefs.set_index("Preference"))
    
    with col2:
        st.subheader("Filtered Car Data:")
        st.write(filtered_data)



# (Main)Data visualization
st.header("Data Visualization")

# Scatterplot of price vs. fuel efficiency for the filtered data
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x="Price_in_thousands", y="Fuel_efficiency", hue="Manufacturer", palette="viridis")
plt.xlabel("Price (in thousands)")
plt.ylabel("Fuel Efficiency (mpg)")
plt.title("Price vs. Fuel Efficiency")
st.pyplot()

# (Main)Recommendations
st.header("Recommendations")

if filtered_data.empty:
    st.warning("No cars match your preferences.")
else:
    # Find the car with the best combination of low price and high fuel efficiency
    best_car = filtered_data[
        (filtered_data["Price_in_thousands"] == filtered_data["Price_in_thousands"].min()) &
        (filtered_data["Fuel_efficiency"] == filtered_data["Fuel_efficiency"].max())
    ]
    
    if not best_car.empty:
        st.success("Based on your preferences, we recommend the following car:")
        st.write(best_car[["Manufacturer", "Model", "Price_in_thousands", "Fuel_efficiency"]])
    else:
        st.warning("No car matches your exact preferences, but here are some good options:")
        st.write(filtered_data[["Manufacturer", "Model", "Price_in_thousands", "Fuel_efficiency"]].head(5))

# About section
st.sidebar.header("About")
st.sidebar.info(
    "This Streamlit app helps you make informed decisions when purchasing a car."
    " You can adjust the range input fields to specify your preferences and explore the data visualization and recommendations."
)

# Display the Streamlit app
#---------------------------2nd Part End here--------------------------------#
