import streamlit as st
import pandas as pd

# Assuming data4 is your DataFrame
# Replace this with your actual data loading code
data4 = pd.read_csv("kaggle_sw_raw.csv")
# data4 = pd.DataFrame({'branch': ['Civil Engineering', 'Electrical Engineering'],
#                       'percentile': [55, 48],
#                       'category': ['OPEN', 'SC'],
#                       'seat_type': ['EWS', 'GENERAL']})

# Streamlit UI
st.title("Data Filtering App")

# User inputs
branch = st.selectbox("Select Branch", data4["branch"].unique())
min_percentile = st.slider("Select Minimum Percentile", min_value=0, max_value=100, value=49)
max_percentile = st.slider("Select Maximum Percentile", min_value=0, max_value=100, value=50)
category = st.selectbox("Select Category", data4["category"].unique())
seat_type = st.selectbox("Select Seat Type", data4["seat_type"].unique())

# Check if the minimum percentile is less than the maximum percentile
if min_percentile >= max_percentile:
    st.warning("Please select a minimum percentile value less than the maximum percentile value.")
else:

# Filter data based on user inputs
    filtered_data = data4[(data4["branch"] == branch) &
                        (data4["percentile"] > min_percentile) &
                        (data4["percentile"] < max_percentile) &
                        (data4["category"] == category) &
                        (data4["seat_type"] == seat_type)]

# Display filtered data
# st.subheader("Filtered Data:")
# st.dataframe(filtered_data)

    # Get unique rows based on 'college_name'
    unique_colleges_data = filtered_data.drop_duplicates(subset=['college_name'])

    # Sort the DataFrame by 'percentile' in ascending order
    unique_colleges_data = unique_colleges_data.sort_values(by='percentile')

    # Display the entire DataFrame with unique college names and sorted by 'percentile' in ascending order
    st.subheader("Filtered Data with Unique College Names (Sorted by Percentile in Ascending Order):")
    st.dataframe(unique_colleges_data)
