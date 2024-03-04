import smtplib
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from sendEMailSetting import *
import os

def sendEmail(toAddress: list, error):
    form = MIMEBase('multipart', 'mixed')
    form['Subject'] = Header("[PET] 세미나실 예약 프로그램 동작 오류".encode('UTF-8'), 'UTF-8')
    form['From'] = "PET-세미나 봇"
    form['to'] = ','.join(toAddress)

    content = MIMEText(error.encode('UTF-8'), _subtype='plain', _charset="UTF-8")
    form.attach(content)

    smtp_server, port = smtp_info['gmail.com']
    try:
        # SMTP 서버 접속 여부 확인
        if port == 587:
            smtp = smtplib.SMTP(smtp_server, port)
            rcode2, _ = smtp.starttls()
        else:
            smtp = smtplib.SMTP_SSL(smtp_server, port)
    
        smtp.login(account, password)
        smtp.sendmail(account, toAddress, form.as_string())
        smtp.quit
    except Exception as e:
        print("Error occurred: " + str(e))