import streamlit as st 
import pandas as pd

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from announcement import get_students, announce

# Get Algoritma email credentials to access the Google Classroom API
@st.cache_data
def Get_Credentials():
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', # View your Google Classroom classes.
            'https://www.googleapis.com/auth/classroom.rosters', # Manage your Google Classroom class rosters.
            'https://www.googleapis.com/auth/classroom.profile.emails', # View the email addresses of people in your classes.
            'https://www.googleapis.com/auth/classroom.announcements', # See, edit, and create classwork materials in Google Classroom.
            'https://www.googleapis.com/auth/spreadsheets.readonly'] # See all your Google Sheets spreadsheets.

    # Use st.secret to keep the credentials token
    creds = Credentials.from_authorized_user_info({"token": st.secrets['token'], 
                                                   "refresh_token": st.secrets['refresh_token'], 
                                                   "token_uri": "https://oauth2.googleapis.com/token", 
                                                   "client_id": st.secrets['client_id'], 
                                                   "client_secret": st.secrets['client_secret'], 
                                                   "scopes": ["https://www.googleapis.com/auth/classroom.courses.readonly", "https://www.googleapis.com/auth/classroom.rosters", "https://www.googleapis.com/auth/classroom.profile.emails", "https://www.googleapis.com/auth/classroom.announcements", "https://www.googleapis.com/auth/spreadsheets.readonly"], 
                                                   "expiry": "2024-01-17T09:28:38.755655Z"}, SCOPES)
    return creds

creds = Get_Credentials()

# Active Student Spreadsheet link
ACTIVE_STUDENT_LINK = 'https://docs.google.com/spreadsheets/d/12FB9410fhRhZp9jl5qLe7x-LGw0QTSfLujA-dE867JE/edit#gid=1593985743'
ACTIVE_STUDENT_ID = ACTIVE_STUDENT_LINK.split(sep='/')[-2] # Get the ID from the link

# Score Academy Spreadsheet link
SCORE_ACADEMY_LINK = 'https://docs.google.com/spreadsheets/d/1cGJ0pn9k9gKCBnceWVwaL9D7BBDMNjLh8uPYlaBlJi8/edit?usp=sharing' # Score Academy Link
SCORE_ACADEMY_ID = SCORE_ACADEMY_LINK.split(sep='/')[-2] # Get the ID from the link
    
# Use the `courses().list()` method to show a list of the user's courses
@st.cache_data
def Get_Courses():
    service = build('classroom', 'v1', credentials=creds)

    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    return courses

courses = Get_Courses()

course_name = None
specialization = None
batch = None
session = None

st.header('Google Classroom Input')
st.write('Select the Algoritma Academy Classroom where you want to post the announcements.')

# Use the courses from before as the select box's options
course_name = st.selectbox("Select Course", [course['name'] for course in courses], index=None, key='course_name')

if course_name != None:
    col1, col2, col3 = st.columns(3)

    with col1:
        # Text input with default value retrieved from course_name
        batch = st.text_input("Class Batch Name", value=course_name.split()[0]) # Get batch name from the first word of course_name
        if batch != None:
            batch = batch.strip().capitalize() # Captitalize string wizard -> Wizard

    with col2:
        # Get specialization name from the 2nd and 3rd word of course_name
        if ' '.join(course_name.split()[-2:]) == 'Data Analytics': 
            spec = 0
        elif ' '.join(course_name.split()[-2:]) == 'Data Visualization': 
            spec = 1
        elif ' '.join(course_name.split()[-2:]) == 'Machine Learning': 
            spec = 2
        else: 
            spec = None
        
        # Select box for class session
        specialization = st.selectbox("Select Specialization", ['Data Analytics', 'Data Visualization', 'Machine Learning'], index=spec, key='specialization')

    with col3:
        # Select box for class session
        session = st.selectbox("Select Class Session", ['Day Online', 'Night Onsite', 'Night Online'], index=None, key='session')

if session != None:
    st.write('#')
    st.header('Google Spreadsheet Input')
    st.write("The App uses Algoritma's Active Student and Score Academy Spreadsheet to collect students' Classroom email. Make sure the sheets below are correct!")

    # Get Sheet Name, if the specialization is 'Data Analytics', add DA to the default sheet name (Xion DA)
    if specialization == 'Data Analytics' :
        col1, col2 = st.columns(2)
        with col1:
            SCORE_NAMA_SHEET = st.text_input("Score Academy Sheet Name", value=f"{batch} DA")
            EMAIL_RANGE = [f'{SCORE_NAMA_SHEET}!D2:E'] # Get the students name and email sheet range from the score academy spreadsheet

        with col2:
            if session == 'Day Online':
                ACTIVE_SHEET = st.text_input("Active Students Sheet Name", value=f"{batch} DA Day [OL]")

            elif session == 'Night Onsite':
                ACTIVE_SHEET = st.text_input("Active Students Sheet Name", value=f"{batch} DA Night")

            elif session == 'Night Online':
                ACTIVE_SHEET = st.text_input("Active Students Sheet Name", value=f"{batch} DA Night [OL]")
            
            ACTIVE_RANGE = [f'{ACTIVE_SHEET}!B2:D'] # Get the students name and email sheet range from the active students spreadsheet
    
    if (specialization == 'Data Visualization') | (specialization == 'Machine Learning') :
        col1, col2 = st.columns(2) 

        with col1:
            # Get Sheet Name, if the specialization is not 'Data Analytics', Use Academy: Batch xx as sheet name (Academy: Batch 24)        
            SCORE_NAMA_SHEET = st.text_input("Score Academy Sheet Name", value=f"Academy: Batch {ord(batch[0])-64}")
            EMAIL_RANGE = [f'{SCORE_NAMA_SHEET}!D2:E'] # Get the students name and email sheet range from the score academy spreadsheet

        with col2:
            # Get Sheet Name, if the specialization is not 'Data Analytics', Use Academy: Batch xx as sheet name (Academy: Batch 24) 
            if session == 'Day Online':
                ACTIVE_SHEET = st.text_input("Active Students Sheet Name", value=f"{batch} Day [OL]")

            elif session == 'Night Onsite':
                ACTIVE_SHEET = st.text_input("Active Students Sheet Name", value=f"{batch} Night")

            elif session == 'Night Online':
                ACTIVE_SHEET = st.text_input("Active Students Sheet Name", value=f"{batch} Night [OL]")
            
            ACTIVE_RANGE = [f'{ACTIVE_SHEET}!B2:D'] # Get the students name and email sheet range from the active students spreadsheet

    st.write('#')

    _, _, col3, col4, _ = st.columns([1,1,2,1,1])
    with col3:
        announce_button = st.button('Create Announcement', use_container_width=True)
        st.write('#')

    with st.spinner('Creating Announcement...'):
        if announce_button:
            try:
                # Get student's data from score academy and active students spreadsheets 
                classroom_df = get_students(creds, ACTIVE_STUDENT_ID, ACTIVE_RANGE, SCORE_ACADEMY_ID, EMAIL_RANGE)

                # Create announcement draft in the chosen classroom and assigns the students automatically
                announce(creds, courses, course_name, classroom_df, session)

                st.success("Announcement Created!", icon='🎊')
                if classroom_df['Status'].str.contains('❌').any():
                    st.dataframe(classroom_df[['Name', 'Status']].sort_values('Status', ascending=False), use_container_width=True)
                    st.markdown(f"📝 **Note**: Please check the ❌ Missing students' classroom email at Algoritma Score Academy {SCORE_NAMA_SHEET} spreadsheets")
                else :
                    st.dataframe(classroom_df[['Name', 'Status']], use_container_width=True)

                st.balloons()

            except:
                st.error('Spreadsheet not Found', icon='⚠')
        
        



