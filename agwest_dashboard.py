import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Sample contact data
if "contacts" not in st.session_state:
    st.session_state.contacts = pd.DataFrame([
        {"Name": "Jordan Wipf", "Role": "Owner", "Company": "Tria Products", "Email": "jordan@triaproducts.com", "Phone": "+1 (204) 280-0483"},
        {"Name": "Travis Gross", "Role": "Electrician", "Company": "", "Email": "Telectricalservicesltd@gmail.com", "Phone": "+1 (431) 866-2831"},
        {"Name": "Eugene Gala", "Role": "Hydronic Engineer", "Company": "SIM Enterprises", "Email": "", "Phone": "204-803-8209"},
    ])

contacts = st.session_state.contacts
subcontractors = contacts[contacts['Role'].str.lower().str.contains("electrician|engineer|contractor", na=False)]

tasks = pd.DataFrame([
    {"Task": "Order security cameras", "Project": "AgWest", "Due": ""},
    {"Task": "Apply for temporary hydro service", "Project": "AgWest Brandon", "Due": ""},
    {"Task": "Update site plan", "Project": "AgWest Russell", "Due": ""},
])

purchases = pd.DataFrame([
    {"Item": "Eufy 4G LTE Cam S330", "Category": "Security Camera", "Supplier": "Amazon.ca", "Price": "$249.99 CAD"},
    {"Item": "3-inch rebar chairs", "Category": "Concrete Accessory", "Supplier": "White Cap", "Price": "TBD"},
])

st.title("AgWest Project Dashboard")

st.markdown("### 📇 Contacts")
if st.checkbox("Add New Contact"):
    with st.form("add_contact_form"):
        name = st.text_input("Name")
        role = st.text_input("Role")
        company = st.text_input("Company")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        submitted = st.form_submit_button("Add Contact")
        if submitted:
            new_contact = {"Name": name, "Role": role, "Company": company, "Email": email, "Phone": phone}
            st.session_state.contacts = pd.concat([st.session_state.contacts, pd.DataFrame([new_contact])], ignore_index=True)
            st.success("Contact added successfully.")

st.dataframe(st.session_state.contacts)

st.markdown("### ✏️ Edit or Delete Contact")
if not contacts.empty:
    contact_names = contacts["Name"].tolist()
    selected_name = st.selectbox("Select contact to edit/delete", contact_names)

    if selected_name:
        contact_index = contacts[contacts["Name"] == selected_name].index[0]
        contact_row = contacts.loc[contact_index]

        with st.form("edit_contact_form"):
            updated_name = st.text_input("Name", contact_row["Name"])
            updated_role = st.text_input("Role", contact_row["Role"])
            updated_company = st.text_input("Company", contact_row["Company"])
            updated_email = st.text_input("Email", contact_row["Email"])
            updated_phone = st.text_input("Phone", contact_row["Phone"])

            update = st.form_submit_button("Update Contact")
            delete = st.form_submit_button("Delete Contact")

            if update:
                st.session_state.contacts.loc[contact_index] = {
                    "Name": updated_name,
                    "Role": updated_role,
                    "Company": updated_company,
                    "Email": updated_email,
                    "Phone": updated_phone
                }
                st.success("Contact updated.")

            if delete:
                st.session_state.contacts = st.session_state.contacts.drop(contact_index).reset_index(drop=True)
                st.success("Contact deleted.")

st.markdown("### 🧱 Subcontractors")
subcontractors = st.session_state.contacts[st.session_state.contacts['Role'].str.lower().str.contains("electrician|engineer|contractor", na=False)]
st.dataframe(subcontractors)

st.markdown("### 📋 Tasks")
st.dataframe(tasks)

st.markdown("### 🛒 Potential Purchases")
st.dataframe(purchases)

st.markdown("### 🌦️ Weather")
st.markdown("[🌤 Brandon Weather Forecast](https://forecast7.com/en/49d85n99d95/brandon/)")
st.markdown("[🌤 Russell Weather Forecast](https://forecast7.com/en/50d77n101d29/russell/)")

st.sidebar.title("Project Summary")
st.sidebar.info("Manage contacts, tasks, and procurement across AgWest sites.")
