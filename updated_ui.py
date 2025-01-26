import streamlit as st
import pandas as pd
import time
import pickle


data4 = pd.read_csv("kaggle_sw_raw.csv")

branches = ['Civil Engineering', 'Computer Science and Engineering', 'Information Technology', 'Electrical Engineering', 'Electronics and Telecommunication Engg', 'Mechanical Engineering']
categories = ['NT 2 (NT-C)', 'SC', 'OBC', 'ST', 'OPEN']

filtered_data = data4[(data4["branch"].isin(branches)) & (data4["category"].isin(categories))]

columns_to_drop = ["fulfillment","rank","gender", "seat_type", "primary_seat_type", "secondary_seat_type", "branch_code", "enrollment_no"]
filtered_data = filtered_data.drop(columns=columns_to_drop)

filtered_data = filtered_data[filtered_data["score_type"] == "MHT-CET"]


st.title("Predict Preferential allotment of college for admission 🎓")

# Add a percentage input box
percentage = st.number_input('Enter a MHT-CET Score (Percentage)', min_value=0.0, max_value=100.0, step=0.01, format="%.2f")

# Display the input values
st.write('Your entered score:', "{:.2f}".format(percentage))

# Add a radio button for gender selection
gender = st.radio("Select Gender :", ('Male', 'Female'))

st.write('Selected gender:', gender)

# User inputs
branch = st.selectbox("Select Branch :", filtered_data["branch"].unique())


category = st.selectbox("Select Reservation Category :", filtered_data["category"].unique())
#seat_type = st.selectbox("Select Seat Type", data4["seat_type"].unique())


# Add a multiselect dropdown box for selecting multiple colleges
selected_colleges = st.multiselect('Select preferred colleges:', filtered_data["college_name"].unique())

df = pd.DataFrame({'Selected Colleges': selected_colleges})
df.index += 1  # Adjust index to start from 1
st.write('Selected colleges:')
st.dataframe(df)


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Add a predict button
if st.button('Predict'):


    with st.spinner('Predicting...'):
        # Simulate a long-running task (e.g., prediction)
        time.sleep(2)