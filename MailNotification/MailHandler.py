import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailHandler:
    def __init__(self, port, server, sender_email, passwd):
        self.port = port #587
        self.smtp_server = server # smtp.gmail.com
        self.sender_email = sender_email # noreply.PSN.Checker@gmail.com
        self.passwd = passwd # Psn12345

    def send(self, receiver_email, subject, text, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = receiver_email


        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(self.sender_email, self.passwd)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
                return True
        except Exception as e:
            print(e)
            return False

    def returnTemplateInvitation(self, username):
        text = """\
                Hi {0},
                Welcome in PSN Checker app!
                To set your account preferences visit:
                psnchecker.com""".format(username)
        html = """\
                <html>
                  <body>
                    <p>Hi {0},<br>
                       Welcome in PSN Checker app!<br>
                       Click <a href="psnchecker.com">here</a> 
                       to set your account preferences.
                    </p>
                  </body>
                </html>
                """.format(username)
        return text, html
