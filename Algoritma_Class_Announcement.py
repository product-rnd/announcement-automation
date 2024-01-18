import streamlit as st 

st.title("Algoritma Class Announcement")
st.write("Use this App to create Google Classroom Announcements that have already been assigned with the list of students from Algoritma's Active Students.")
st.write("#")

st.header('How to Use')
st.subheader('Create Draft Announcement Post')
st.write(
'''
1. Select the 🏫 **Create Announcement** page on the sidebar.
2. Select the Algoritma Academy Classroom where you want to post the announcements.
3. Fill your classroom's name, batch, specialization, and session.
4. Make sure the sheet name in Algoritma Score Academy and Active Student is correct.
5. Press the **Create Announcement** button to create draft announcement
''')

st.subheader('Create Annoncement Template')
st.write(
'''
1. Select the 📝 **Announcement Template** page on the sidebar.
2. Select the Class topic, start date, and end date
3. Copy the announcement template to the created announcement in Google Classroom
''')