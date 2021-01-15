'''Script that allows to monitor BSD system'''
import os
import smtplib
import argparse
import email

class BaseAlert():
    '''Requires recv defined'''

    def __init__(self,recv):
        self.recv = recv

    def send_alert(self,alert):
        msg = email.message.EmailMessage()
        msg['Subject'] = 'Alert from system'
        msg['From'] = 'alert@' + os.uname().nodename 
        msg['To'] = self.recv
        msg.set_content(alert)
        with smtplib.SMTP() as mail:
            mail.send_message(msg,msg['From'],self.recv)

class Disks(BaseAlert):
    '''Alerts in case there is a drive limit reached'''

    def __init__(self,recv,limit):
        BaseAlert.__init__(self,recv)
        self.limit = limit

    def max_drive_limit(self):
        msg = 'Disk space low for:\n'
        for line in os.popen('df -P'):
            p = line.split()[4]
            p = p[:-1]
            if p.isdigit() and self.limit < int(p):
                msg += str(line)
        self.send_alert(msg)


parser = argparse.ArgumentParser(description='Monitors BSD system and emails alerts on triggers')
parser.add_argument('receiver', help='email of receiver')
parser.add_argument('limit', type=int, help='integer limit of which above disk space will be alerted')
args = parser.parse_args()
disk = Disks(args.receiver, args.limit)
disk.max_drive_limit()
