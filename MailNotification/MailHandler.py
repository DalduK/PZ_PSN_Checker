import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

    def sendInvitation(self, username, receiver_email):
        text, html = self.returnTemplateInvitation(username)
        self.send(receiver_email, 'Witaj w serwisie PSN Checker!', text, html)

    def sendDiscount(self, username, receiver_email, gameNames, prices, urls):
        text, html = self.returnTemplateDiscount(username, gameNames, prices, urls)
        self.send(receiver_email, 'Gra w promocji!', text, html)

    def sendChangedPassword(self, receiver_email, username, passwd):
        text, html = self.returnTemplateChangedPassword(username, passwd)
        self.send(receiver_email, 'Prośba o przypomnienie hasła', text, html)

    def returnTemplateChangedPassword(self, username, passwd):
        text = """\
                Witaj {0},
                wygenerowaliśmy dla Ciebie tymczasowe hasło, pamiętaj aby je zmienić zaraz po zalogowaniu!
                Nowe hasło: {1}""".format(username, passwd)
        html = """\
                        <html>
                          <body>
                            <p>Witaj {0},<br>
                                wygenerowaliśmy dla Ciebie tymczasowe hasło, pamiętaj aby je zmienić zaraz po zalogowaniu!
                                Nowe hasło: {1}
                            </p>
                          </body>
                        </html>
                        """.format(username, passwd)
        return text, html

    def returnTemplateInvitation(self, username):
        text = """\
                Witaj {0},
                dziękujemy za rejestrację w serwisie PSN Checker!
                W celu ustawienia preferencji konta odwiedź poniższy adres:
                psnchecker.com""".format(username)
        html = """\
                <html>
                  <body>
                    <p>Witaj {0},<br>
                       dziekujemy za rejestrację w serwisie PSN Checker!<br>
                       Odwiedź <a href="psnchecker.com">tutaj</a> 
                       aby sprawdzić swój koszyk.
                    </p>
                  </body>
                </html>
                """.format(username)
        return text, html

    def returnTemplateDiscount(self, username, gameNames, prices, urls):
        if (len(gameNames) == len(prices)) & (len(prices) == len(urls)):
            textTmp = ''
            for i in range(0, len(gameNames)):
                textTmp = textTmp + gameNames[i] + "\t" + str(prices[i]) + "zł\n"

            text = """\
                            Witaj {0},
                            gra, którą obserwujesz jest teraz przeceniona:
                            {1}""".format(username, textTmp)

            htmlTmp = '<br><br>'
            for i in range(0, len(gameNames)):
                htmlTmp = htmlTmp + gameNames[i] + '</a>\t' + str(prices[i]) + "zł<br>" + '<img src="' + urls[i] + '" height = "400" width = "400" />'+"<br><br>"
            html = """\
                            <html>
                              <body>
                                <p>Witaj {0},<br>
                                   gra, którą obserwujewsz jest teraz w przecenie:<br>
                                   {1}
                                </p>
                              </body>
                            </html>
                            """.format(username, htmlTmp)
            return text, html
        else:
            raise Exception('Invalid function variables')
