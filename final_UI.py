import streamlit as st
import pandas as pd
import time
import pickle
from sklearn.preprocessing import LabelEncoder
# Load the dataset
data4 = pd.read_csv("kaggle_sw_raw.csv")


columns_to_encode = ['college_name']
label_encoder = LabelEncoder()

for col in columns_to_encode:
    data4[col + '_encoded'] = label_encoder.fit_transform(data4[col])
# Define branches and categories

# Define branches and categories
branches = ['Civil Engineering', 'Computer Science and Engineering', 'Information Technology', 'Electrical Engineering', 'Electronics and Telecommunication Engg', 'Mechanical Engineering']
categories = ['NT 2 (NT-C)', 'SC', 'OBC', 'ST', 'OPEN']

# Filter the data based on branches and categories
filtered_data = data4[(data4["branch"].isin(branches)) & (data4["category"].isin(categories))]

# Drop irrelevant columns
columns_to_drop = ["fulfillment", "rank", "gender", "seat_type", "primary_seat_type", "secondary_seat_type", "branch_code", "enrollment_no"]
filtered_data = filtered_data.drop(columns=columns_to_drop)

# Filter by score type
filtered_data = filtered_data[filtered_data["score_type"] == "MHT-CET"]

# Load the trained model
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)

# Prediction function
def predict_college(percentile, branch, category):
    # Create DataFrame for prediction
    input_data = pd.DataFrame({
        'percentile': [percentile],
        'branch_Civil Engineering': [0],
        'branch_Computer Science and Engineering': [0],
        'branch_Electrical Engineering': [0],
        'branch_Electronics and Telecommunication Engg': [0],
        'branch_Information Technology': [0],
        'branch_Mechanical Engineering': [0],
        'category_NT 2 (NT-C)': [0],
        'category_OBC': [0],
        'category_OPEN': [0],
        'category_SC': [0],
        'category_ST': [0]
    })

    # Set the corresponding branch and category columns to 1 based on user input
    input_data['branch_' + branch] = 1
    input_data['category_' + category] = 1
    
    # Predict using the trained model
    college_encoded = clf.predict(input_data)[0]
    college_name = filtered_data[filtered_data['college_name_encoded'] == college_encoded]['college_name'].iloc[0]
    
    return college_name

# UI
st.title("Predict Preferential allotment of college for admission 🎓")

# Add input widgets
percentage = st.number_input('Enter a MHT-CET Score (Percentage)', min_value=0.0, max_value=100.0, step=0.01, format="%.2f")
gender = st.radio("Select Gender :", ('Male', 'Female'))
branch = st.selectbox("Select Branch :", filtered_data["branch"].unique())
category = st.selectbox("Select Reservation Category :", filtered_data["category"].unique())

# Multiselect preferred colleges
selected_colleges = st.multiselect('Select preferred colleges:', filtered_data["college_name"].unique())

df_selected_colleges = pd.DataFrame({'Selected Colleges': selected_colleges})
st.write('Selected colleges:')
st.dataframe(df_selected_colleges)

# Prediction
if st.button('Predict'):
    with st.spinner('Predicting...'):
        # Predict college
        predicted_college = predict_college(percentage, branch, category)
        time.sleep(2)  # Simulate a delay
        st.success(f'Predicted College: {predicted_college}')
        
        # Check if predicted college is in selected colleges
        if predicted_college in selected_colleges:
            st.write("Congratulations! You have selected the predicted college.")
        else:
            st.write("Sorry, the predicted college is not in your selected colleges.")