#coding=utf-8
import site_helper, web, page_helper
from site_helper import getModel
import subprocess, os, time

from email.MIMEText import MIMEText
import smtplib
from smtplib import SMTPRecipientsRefused

# ../editor/SendMail.html
CONTENT_DIR = '/tmp/aoaola_mail_content'
if not os.path.exists(CONTENT_DIR):
    os.mkdir(CONTENT_DIR)

class SendMail:

    def GET(self):
        return site_helper.editor_render.SendMail()

    def POST(self):
        i = web.input()
        subject = i.get('subject', '').encode('utf-8','ignore').replace('"','')
        from_addr = i.get('from_addr', '').encode('utf-8','ignore').replace('"','')
        to = i.get('to', '').encode('utf-8','ignore')
        content = i.get('content', '').encode('utf-8','ignore')
        now = time.localtime()

        #content_file_name = os.path.join(CONTENT_DIR, '%d_%d_%d_%d_%d_%d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec) )

        #f = open(content_file_name,'w')
        #f.write(content)
        #f.close()

        if i.get('to_all','') == 'on':
            db = site_helper.getDBHelper()
            receivers = [i.email for i in db.fetchSome('select email from User')]
        else:
            receivers = [i.strip().replace('"','') for i in to.split('\n')]
        
        #sends = []
        for receiver in receivers:
            if receiver:
                #sends.append('mail -r "%s" -s "%s" "%s" < %s' % (from_addr, subject, receiver, content_file_name))
                try:
                    self.send_html_email(from_addr, receiver, subject, content)
                except SMTPRecipientsRefused:
                    pass
        #os.system('\n'.join(sends))

        return page_helper.refresh()



    def send_html_email(self,from_addr, receiver, subject, body):
        """subject and body are unicode objects"""
        msg = MIMEText(body, 'html', 'utf8')
        msg['From'] = from_addr
        msg['To'] = receiver
        msg['Subject'] = subject

        smtpserver = 'smtp.163.com'  
        username = 'aoaola2011'  
        password = 'z1x2c3a4s5d6'  

        smtp = smtplib.SMTP()  
        smtp.connect('smtp.163.com')  
        smtp.login(username, password)  
        smtp.sendmail(from_addr, receiver, msg.as_string())
        smtp.quit()  
        
