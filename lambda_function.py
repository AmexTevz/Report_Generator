from datetime import datetime
import dateutil.tz
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import psycopg2


from_email_address = "example@gmail.com"  # The address that is going to be used to send emails.
from_email_password = "example"  # Email Password or the dedicated key.
to_email = "example@gmail.com"  # Recipient emails. Can accept multiple emails as a list.

eastern = dateutil.tz.gettz('US/Eastern')
today = datetime.now(tz=eastern).strftime("%m-%d-%y %H:%M")
attachment = f"Report  {today}.csv"  # The report will be named "Report - today's date."
headers = "Id FirstName LastName Age Job Company".split()  # The headers which are going to be used in the generated file.
query = "SELECT * FROM table WHERE age < 40 ORDER by fname; "  # Query which will be sent to Postgres.


# Postgres credentials.
def sql():
    con = psycopg2.connect(
        database="",  # database name
        user="",  # username
        password="",  # password
        host="127.0.0.1",  # local or web host ip
        port='5432'  # database port
    )
    return con


# from_email credentials
# Example Gmail
def send_email():
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.ehlo()
        server.login(from_email_address, from_email_password)  # Email address and password.
        server.sendmail(from_email_address, to_email, msg.as_string())
        server.quit()


email_body = ''
cursor = sql().cursor()

cursor.execute(query)
sql().commit()
results = cursor.fetchall()
sql().close()
cursor.close()

if len(results) >= 1:  # A check is performed whether to generate a report or not.
    with open('/tmp/' + attachment, "w") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i in results:
            writer.writerow(i)

    msg = MIMEMultipart()
    msg['Subject'] = attachment.split('.')[0]
    body = 'The report has been generated.'
    body = MIMEText(body)
    msg.attach(body)
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open('/tmp/' + attachment, "rb").read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=attachment)
    msg.attach(part)
    send_email()
else:
    msg = MIMEMultipart()
    msg['Subject'] = 'No Report for today'
    body = 'Query ran successfully.\nNo report generated.'
    body = MIMEText(body)
    msg.attach(body)
    send_email()
