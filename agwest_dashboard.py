
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets using Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# Connect to the Google Sheet and worksheet
sheet = client.open_by_key("1LUFKamENznSNzY7wXu6n1w2hHVy6q9TOvmM2EbtAULw")
worksheet = sheet.worksheet("Contacts")

# Load contacts into a DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("AgWest Contact Manager (Live Google Sheet)")

# Add new contact
st.markdown("### ➕ Add New Contact")
with st.form("add_contact_form"):
    name = st.text_input("Name")
    role = st.text_input("Role")
    company = st.text_input("Company")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submitted = st.form_submit_button("Add Contact")
    if submitted:
        new_contact = [name, role, company, email, phone]
        worksheet.append_row(new_contact)
        st.success("Contact added successfully. Please refresh to see the update.")

# Show current contacts
st.markdown("### 📇 Current Contacts")
st.dataframe(df)

# Edit/delete contact
st.markdown("### ✏️ Edit or Delete Contact")
if not df.empty:
    contact_names = df["Name"].tolist()
    selected_name = st.selectbox("Select contact to edit/delete", contact_names)
    selected_index = df[df["Name"] == selected_name].index[0]
    contact = df.loc[selected_index]

    with st.form("edit_contact_form"):
        updated_name = st.text_input("Name", contact["Name"])
        updated_role = st.text_input("Role", contact["Role"])
        updated_company = st.text_input("Company", contact["Company"])
        updated_email = st.text_input("Email", contact["Email"])
        updated_phone = st.text_input("Phone", contact["Phone"])
        update = st.form_submit_button("Update Contact")
        delete = st.form_submit_button("Delete Contact")

        if update:
            worksheet.update(f"A{selected_index+2}", [[updated_name, updated_role, updated_company, updated_email, updated_phone]])
            st.success("Contact updated. Please refresh to see changes.")

        if delete:
            worksheet.delete_rows(selected_index + 2)
            st.success("Contact deleted. Please refresh to update the table.")
