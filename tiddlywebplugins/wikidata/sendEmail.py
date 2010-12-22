#sends email from a specified server
import smtplib

from email.mime.text import MIMEText

def send(to, subject='', body='', from_='avox@wiki-data.com'):
    if isinstance(to, basestring):
        to = [to]

    msg = MIMEText(body.encode('utf8', 'replace'), 'plain', 'utf8')

    msg['Subject'] = subject

    msg['From'] = 'Avox <%s>' % from_
    msg['Reply-To'] = from_

    msg['To'] = ', '.join(to)

    s = smtplib.SMTP('localhost')
    s.sendmail(from_, to, msg.as_string())
