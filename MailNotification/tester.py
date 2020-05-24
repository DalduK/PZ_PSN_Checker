from MailHandler import MailHandler

mh = MailHandler(587, 'smtp.gmail.com', 'noreply.PSN.Checker@gmail.com', 'Psn12345')
text, html = mh.returnTemplateInvitation('anon')
mh.send('szachkonrad@op.pl', 'test', text, html)
