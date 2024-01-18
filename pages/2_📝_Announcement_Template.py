import streamlit as st
import datetime as dt
import locale

from announcement import course_list, learnr

locale.setlocale(locale.LC_TIME, "id") # Use Indonesian language for datetime data

st.title('Announcement Template')
st.write('Select the informations below based on the class you manage.')

# Retrieve values when switching pages or reloading streamlit using st.session_state
try :
    course_name = st.session_state['course_name']
    specialization = st.session_state['specialization']
    session = st.session_state['session']
    batch = course_name.split()[0]

    st.session_state['session'] = session
    st.session_state['course_name'] = course_name
    st.session_state['specialization'] = specialization

except :
    st.error('Please fill the 🏫 Create Announcement page first')
    course_name = None
    specialization = None
    session = None
    batch = None

# Select list of topics in the specialization
nama_course = st.selectbox('Select Course Topic', options=course_list(specialization))

# Select starting and ending date of the class
col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input('Select Class Start Date 📅', format='DD/MM/YYYY')
with col2:
    date2 = st.date_input('Select Class End Date 📅', format='DD/MM/YYYY', value=date1+dt.timedelta(days=4))

# Change datetime format
hari1 = date1.strftime('%A')
hari2 = date2.strftime('%A')

tanggal1 = date1.strftime(f'%d %B %Y')
tanggal2 = date2.strftime(f'%d %B %Y')

# Change askalgo and learn link based on specialization
if specialization == 'Data Analytics':
    askalgo = 'https://askalgo-py.netlify.app/'
    learn = 'Learnpy Data Analytics (learnpy-da): https://gitlab.com/algoritma4students/academy-python/exercise/learnpy-da'
elif (specialization == 'Data Visualization') | (specialization == 'Machine Learning') :
    askalgo = 'https://askalgo-r.netlify.app/'
    learn = f'Link pembelajaran mandiri (LearnR) : {learnr(nama_course)}'
else :
    askalgo = '_____________'
    learn = '_____________'

# Change class time based on session
if session == 'Night Online':
    waktu_kelas = '18.30 - 21.30'
    waktu_qna = '17.45 - 18.05'
elif session == 'Day Online':
    waktu_kelas = '13.00 - 16.00'
    waktu_qna = '12.40 - 13.00'
else :
    waktu_kelas = '_____________'
    waktu_qna = '_____________'

st.write('#')

# Change announcement text format based on session
if session == 'Night Onsite':
    st.write(
f'''
Dear Class,
<br>
<br>
Selamat datang di Algoritma Academy kelas {batch} {session}. Berikut adalah post terkait:

- Topik		    : <b>{nama_course}</b>
- Hari		    : <b>{hari1} - {hari2}, {tanggal1} - {tanggal2}</b>
- Waktu Kelas	: <b>18.30 - 21.30 WIB</b>
- Sesi QnA	    : <b>17.45 - 18.05 WIB (opsional)</b>
- Tempat	    : <b>Algoritma Data Science School - Training Center, Menara Kadin Indonesia, lt. 4</b>

<b>----------------------------------------------------------------------</b>

<b>PRANALA KELAS:</b>

- Panduan Offline Class, dokumentasi Dive Deeper, dan QnA session: _____________
- {learn}

<b>----------------------------------------------------------------------</b>

<b>LAMPIRAN:</b>

- <b><TBA></b>

<b>----------------------------------------------------------------------</b>

Kami telah mendokumentasikan <b>Frequently Asked Questions (FAQ)</b> yang dapat dikunjungi melalui {askalgo}.  Semoga bermanfaat bagi Bapak/Ibu sebagai referensi bahan pembelajaran.


Apabila Bapak/Ibu mengalami kendala dalam proses pembelajaran silahkan menghubungi kami melalui :
- Untuk pertanyaan administratif, silakan kirim email ke mentor@algorit.ma.
- Untuk pertanyaan teknis dan materi pembelajaran, Anda dapat bergabung di https://github.com/teamalgoritma/community/discussions.


Demikian yang dapat kami sampaikan, terima kasih.
<br>
<br>
Best regards,

Team Algoritma

''', unsafe_allow_html = True)
    
elif (session == 'Night Online') | (session == 'Day Online'):
    st.write(
f'''
Dear Class,
<br>
<br>
Selamat datang di Algoritma Academy kelas {batch} {session}. Berikut adalah post terkait:

- Topik		    : <b>{nama_course}</b>
- Hari		    : <b>{hari1} - {hari2}, {tanggal1} - {tanggal2}</b>
- Waktu Kelas	: <b>{waktu_kelas} WIB</b>
- Sesi QnA	    : <b>{waktu_qna} WIB (opsional)</b>

Silakan bergabung ke dalam kelas melalui link berikut:
<br>_____________
<br><br>
Meeting ID: _____________<br>
Passcode: _____________

<b>----------------------------------------------------------------------</b>

<b>PRANALA KELAS:</b>

- Panduan Online Class, dokumentasi Dive Deeper, dan QnA session: _____________
- Dokumentasi Error: _____________
- Form kehadiran: _____________
- {learn}

<b>----------------------------------------------------------------------</b>

<b>RECORDING:</b>

- <b><TBA></b>

<b>----------------------------------------------------------------------</b>

<b>LAMPIRAN:</b>

- <b><TBA></b>

<b>----------------------------------------------------------------------</b>

Kami telah mendokumentasikan <b>Frequently Asked Questions (FAQ)</b> yang dapat dikunjungi melalui {askalgo}.  Semoga bermanfaat bagi Bapak/Ibu sebagai referensi bahan pembelajaran.


Apabila Bapak/Ibu mengalami kendala dalam proses pembelajaran silahkan menghubungi kami melalui :
- Untuk pertanyaan administratif, silakan kirim email ke mentor@algorit.ma.
- Untuk pertanyaan teknis dan materi pembelajaran, Anda dapat bergabung di https://github.com/teamalgoritma/community/discussions.


Demikian yang dapat kami sampaikan, terima kasih.
<br>
<br>
Best regards,

Team Algoritma

''', unsafe_allow_html = True)