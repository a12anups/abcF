#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# CSV file name
csv_file = "responses.csv"

# Function to save responses
def save_response(email, mobile, answers):
    # Create a dictionary with responses
    response_data = {
        "Email": email,
        "Mobile": mobile,
        "Q1": answers[0],
        "Q2": answers[1],
        "Q3": answers[2],
        "Q4": answers[3],
        "Q5": answers[4]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([response_data])

    # Append to CSV file
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False)

# Streamlit UI
st.set_page_config(page_title="User Feedback Form", layout="centered")
st.title("📋 User Feedback Form")

# Collect Email & Mobile Number
email = st.text_input("📧 Enter your Email ID", placeholder="example@example.com")
mobile = st.text_input("📱 Enter your Mobile Number", placeholder="1234567890")

# Questions and Options
questions = [
    "How satisfied are you with our service?",
    "How likely are you to recommend us?",
    "How easy was the process?",
    "How responsive was our support team?",
    "How would you rate the overall experience?"
]

options = ["Very Poor", "Poor", "Neutral", "Good", "Excellent"]

# Collect responses
responses = []
for i, question in enumerate(questions):
    responses.append(st.radio(f"**{i+1}. {question}**", options, index=2))

# Submit Button
if st.button("Submit Response ✅"):
    if email and mobile:
        save_response(email, mobile, responses)
        st.success("✅ Response saved successfully! Thank you for your feedback.")
    else:
        st.warning("⚠️ Please enter both Email and Mobile Number.")

# Display current responses
if os.path.exists(csv_file):
    st.write("📊 **Current Responses:**")
    df_responses = pd.read_csv(csv_file)
    st.dataframe(df_responses)
# Convert categorical responses into counts
summary_data = df_responses.iloc[:, 2:].apply(pd.Series.value_counts).fillna(0)

    # Plot the response distribution
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(summary_data, annot=True, cmap="coolwarm", fmt=".0f", linewidths=0.5, ax=ax)
    
plt.xlabel("Responses")
plt.ylabel("Questions")
plt.title("Feedback Summary Heatmap")

st.pyplot(fig)
