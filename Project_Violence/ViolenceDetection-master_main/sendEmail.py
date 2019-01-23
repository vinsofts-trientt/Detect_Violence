import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
# sendEmail.sendMail('trientt@vinsofts.net','12345Aa@','boynd10101996@gmail.com','This is the subject','This is my message','C:/Users/anlan/OneDrive/Desktop/_Result.avi')
def sendMail(email,password,send_to_email,subject,message,file_location):
    # email = 'trientt@vinsofts.net'
    # password = '12345Aa@'
    # send_to_email = 'boynd10101996@gmail.com'
    # subject = 'This is the subject'
    # message = 'This is my message'
    # file_location = 'C:/Users/anlan/OneDrive/Desktop/_Result.avi'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
# sendMail('trientt@vinsofts.net','12345Aa@','boynd10101996@gmail.com','This is the subject','This is my message','C:/Users/anlan/OneDrive/Desktop/_Result.avi')