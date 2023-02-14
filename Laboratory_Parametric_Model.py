import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(page_title="Lab Parametric Model")
st.title("Laboratory Parametric Energy Model")
st.session_state.update(st.session_state)

st.markdown(
    """
    **Instructions:**
    1. Provide the project name and your email address in the sidebar.
    2. On the _Iterations_ page, enter the various laboratory characteristics and energy conservation measures to be tested.
       * Assign all parameters at least one value.
       * The total number of iterations and computation time will display along with a submit button.
       * There are separate tabs for Research and Academic labs. If both types of labs are to be tested, two submissions will be needed.
    3. On the _Project Inputs_ page, provide all relevant project-specific information and submit.

    For questions or suggestions, please reach out to me at urwa.irfan@smithgroup.com :)
    """
)
st.subheader("")
st.image("https://i.imgur.com/sPVBkh7.png", caption = "PowerBI Dashboard")
st.subheader("")
st.write("Source code is available [here](https://github.com/urwahah/Lab-Parametric-Model).")

def default(k):
    if k not in st.session_state:
        return ""
    else:
        return st.session_state[k]

st.sidebar.subheader("")
st.sidebar.text_input('Project name', value=default('project'), key='project')
st.sidebar.text_input('Email address', value=default('email'), key='email')

def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, file, attachment=None):
  message = MIMEMultipart()
  message['To'] = Header(receiver)
  message['From']  = Header(sender)
  message['Subject'] = Header(subject)
  message.attach(MIMEText(email_message,'plain','utf-8'))
  part = MIMEBase('application', "octet-stream")
  if file=='research':
    part.set_payload(attachment)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Iterations_Research.pkl"')
  elif file=='academic':
    part.set_payload(attachment)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Iterations_Academic.pkl"')
  else:
    part.set_payload(attachment.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Project_Inputs.xlsx"')
  message.attach(part)
  server = smtplib.SMTP(smtp_server, smtp_port)
  server.starttls()
  server.ehlo()
  server.login(sender, password)
  text = message.as_string()
  server.sendmail(sender, receiver, text)
  server.quit()

css='''
[data-testid="stSidebarNav"] {
  min-height: 50vh
}
'''
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)