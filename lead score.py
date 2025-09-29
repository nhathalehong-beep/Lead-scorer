import streamlit as st
import pandas as pd

def calculate_score(data):
    required_fields = ['Contact name', 'Company name', 'Email', 'Phone', 'Personal ID', 'Business License']
    score = 0
    missing = []
    
    for field in required_fields[:-1]:
        if pd.notna(data.get(field)):
            score += 1
        else:
            missing.append(field)
    
    if data.get('Company Type') == 'Company' and pd.notna(data.get('Business License')):
        score += 1
    elif data.get('Company Type') == 'Company':
        missing.append('Business License')
        
    return score, missing

st.title('Lead Scorer')

tab1, tab2 = st.tabs(["Manual Entry", "File Upload"])

with tab1:
    contact_name = st.text_input("Contact Name*")
    company_name = st.text_input("Company Name*")
    email = st.text_input("Email*")
    phone = st.text_input("Phone*")
    personal_id = st.text_input("Personal ID*")
    company_type = st.radio("Company Type", ["Individual", "Company"])
    business_license = st.text_input("Business License")
    
    if st.button("Calculate Score"):
        data = {
            'Contact name': contact_name,
            'Company name': company_name,
            'Email': email,
            'Phone': phone,
            'Personal ID': personal_id,
            'Business License': business_license,
            'Company Type': company_type
        }
        score, missing = calculate_score(data)
        st.write(f"Score: {score}/6")
        if missing:
            st.write(f"Missing fields: {', '.join(missing)}")

with tab2:
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        results = []
        for _, row in df.iterrows():
            score, missing = calculate_score(row)
            results.append(f"Score: {score}/6, Missing: {', '.join(missing) if missing else 'None'}")
            
        for i, result in enumerate(results):
            st.write(f"Record {i+1}: {result}")
