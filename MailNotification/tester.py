from MailHandler import MailHandler

mh = MailHandler(587, 'smtp.gmail.com', 'noreply.PSN.Checker@gmail.com', 'Psn12345')
mh.sendInvitation('Anon', 'szachkonrad@op.pl')

gry = ['gra 1', 'gra 2', 'gra 3', 'gra 4']
ceny = ['11.11', '22.22', '33.33', '44.44']
linki = ['https://apollo2.dl.playstation.net/cdn/EP2103/CUSA01344_00/uYNqoXaHHh2mtU9UCRn1ZYiO6RuEx5Jx.png', 'https://apollo2.dl.playstation.net/cdn/EP2103/CUSA01344_00/uYNqoXaHHh2mtU9UCRn1ZYiO6RuEx5Jx.png', 'https://apollo2.dl.playstation.net/cdn/EP2103/CUSA01344_00/uYNqoXaHHh2mtU9UCRn1ZYiO6RuEx5Jx.png', 'https://apollo2.dl.playstation.net/cdn/EP2103/CUSA01344_00/uYNqoXaHHh2mtU9UCRn1ZYiO6RuEx5Jx.png']

mh.sendDiscount('Anon', 'szachkonrad@op.pl', gry, ceny, linki)