 
# Import required dependencies to use Google's API
import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Get students name and email from Algoritma Score Academy and Active Students spreadsheet
def get_students(creds, ACTIVE_STUDENT_ID, SHEET_RANGE, SCORE_ACADEMY_ID, EMAIL_RANGE):
    # Call Classroom API
    service = build('sheets', 'v4', credentials=creds)

    # Retrive values from sheet range in Active Students spreadsheet
    sheet = service.spreadsheets().values().batchGet(spreadsheetId=ACTIVE_STUDENT_ID,
                                                    ranges=SHEET_RANGE).execute()
    
    # Create a dataframe from the retrieved values
    active_df = pd.DataFrame(sheet['valueRanges'][0]['values'], columns=['Name', 'Class', 'Email'])
    active_df['Email'] = active_df['Email'].str.strip().str.lower()

    # Retrive values from sheet range in Score Academy spreadsheet
    sheet = service.spreadsheets().values().batchGet(spreadsheetId=SCORE_ACADEMY_ID,
                                                    ranges=EMAIL_RANGE).execute()
    # Create a dataframe from the retrieved values
    score_df = pd.DataFrame(sheet['valueRanges'][0]['values'], columns=['Email', 'Email Classroom'])
    score_df['Email'] = score_df['Email'].str.strip().str.lower()
    score_df['Email Classroom'] = score_df['Email Classroom'].str.strip().str.lower()

    # Merge both Active Students and Score Academy dataframes based on the student's email
    classroom_df = pd.merge(active_df, score_df, how='left', on='Email')
    classroom_df = classroom_df[classroom_df['Email'].notna()]

    # Give status based on the student's classroom email availability
    classroom_df.loc[classroom_df['Email Classroom'].notna(), 'Status'] = '✅ Assigned'
    classroom_df.loc[classroom_df['Email Classroom'].isna(), 'Status'] = '❌ Missing'

    return classroom_df


# Create draft announcement with assigned students
def announce(creds, courses, course_name, classroom_df, session):
    # Call Classroom API
    service = build('classroom', 'v1', credentials=creds)

    # Get Google Classroom id
    for course in courses:
        if course_name == course['name']:
            course_id = course['id']
            break
    
    # Get students list
    response = service.courses().students().list(courseId=course_id).execute()
    students = response.get('students')

    while response.get('nextPageToken'):
        response = service.courses().students().list(courseId=course_id, pageToken = response['nextPageToken']).execute()
        students.extend(response.get('students'))


    student_id = []

    # Get students id based on students' classroom email
    for student in students:
        if student['profile']['emailAddress'] in classroom_df['Email Classroom'].tolist():
            student_id.append(student['userId'])
        elif "@algorit.ma" in student['profile']['emailAddress']:
            student_id.append(student['userId'])
        elif (student['profile']['emailAddress'] == "algostudentday@gmail.com") & (session == 'Day Online'):
            student_id.append(student['userId'])
        elif (student['profile']['emailAddress'] == "algostudentnight0@gmail.com") & (session == 'Night Online'):
            student_id.append(student['userId'])
        elif (student['profile']['emailAddress'] == "algostudentnight1@gmail.com") & (session == 'Night Onsite'):
            student_id.append(student['userId'])


    # Create the announcement body and settings
    body = {
        'text': session,
        'state': "DRAFT",
        'assigneeMode': 'INDIVIDUAL_STUDENTS',
        "individualStudentsOptions": {
            "studentIds": student_id
        }
    }

    # Create the announcement
    response = service.courses().announcements().create(courseId=course_id, body=body).execute()


def course_list(specialization):

    if specialization == 'Data Analytics':
        return ['Python for Data Analysts (P4DA)', 
                'Exploratory Data Analysis (EDA)', 
                'Data Wrangling and Visualization (DWV)', 
                'Structured Query Language (SQL)',
                'Capstone Project Data Analytics',
                'Introduction to Machine Learning I (IML1)', 
                'Introduction to Machine Learning II (IML2)']

    elif specialization == 'Data Visualization':
        return ['Programming for Data Science (P4DS)',
                'Practical Statistic (PS)', 
                'Data Visualization (DV)', 
                'Interactive Plotting (IP)',
                'Capstone Project Data Visualization']

    elif specialization == 'Machine Learning':
        return ['Regression Model (RM)', 
                'Classification in Machine Learning I (C1)', 
                'Classification in Machine Learning II (C2)', 
                'Unsupervised Learning (UL)', 
                'Time Series & Forecasting (TSF)', 
                'Neural Network and Deep Learning (NN)',
                'Capstone Project Machine Learning']
    else:
        return ['']

def learnr(topic):
    if topic == 'Programming for Data Science (P4DS)': 
        return 'https://algoritmads.shinyapps.io/prep4ds/'
    elif topic == 'Practical Statistic (PS)': 
        return 'https://algoritmads.shinyapps.io/preps/'
    elif topic == 'Data Visualization (DV)': 
        return 'https://ahmadhusain.shinyapps.io/learnr-dv/'
    elif topic == 'Interactive Plotting (IP)': 
        return 'https://vicnp.shinyapps.io/IP_LearnR/'
    elif topic == 'Regression Model (RM)': 
        return 'https://inayatus.shinyapps.io/AlgLearnRM/'
    elif topic == 'Classification in Machine Learning I (C1)': 
        return 'https://algoritma.shinyapps.io/LearnRC1/'
    elif topic == 'Classification in Machine Learning II (C2)': 
        return 'https://11pgcm-amalia.shinyapps.io/LearnR-CIML2/'
    elif topic == 'Unsupervised Learning (UL)': 
        return 'https://inayatus.shinyapps.io/AlgLearnRUL/'
    elif topic == 'Time Series & Forecasting (TSF)': 
        return 'https://kevinwibowo.shinyapps.io/AlgLearnRTS/'
    else:
        return '_____________'