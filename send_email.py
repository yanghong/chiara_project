# !/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL


class Mailer(object):
    def __init__(self, mail_list, mail_title, mail_content):
        self.mail_list = mail_list
        self.mail_title = mail_title
        self.mail_content = mail_content

        self.mail_host = "smtp.exmail.qq.com"
        self.mail_user = "h@0920er.com"
        self.mail_pass = "QZ6BH2nw9yaCPgbf"
        self.mail_postfix = "@qq.com"

    def send_mail(self):
        me = self.mail_user + "<" + self.mail_user + ">"
        msg = MIMEMultipart()
        msg['Subject'] = '银行外汇市场人民币汇率中间价'
        msg['From'] = me
        msg['To'] = ";".join(self.mail_list)

        # puretext = MIMEText('<h1>你好，<br/>'+self.mail_content+'</h1>','html','utf-8')
        pure_text = MIMEText(self.mail_content)
        msg.attach(pure_text)

        #     jpg类型的附件
        #     jpgpart = MIMEApplication(open('/home/mypan/1949777163775279642.jpg', 'rb').read())
        #     jpgpart.add_header('Content-Disposition', 'attachment', filename='beauty.jpg')
        #     msg.attach(jpgpart)

        # 首先是xlsx类型的附件
        xlsx_part = MIMEApplication(open('chiara.xls', 'rb').read())
        xlsx_part.add_header('Content-Disposition', 'attachment', filename='chiara.xls')
        msg.attach(xlsx_part)

        # mp3类型的附件
        # mp3part = MIMEApplication(open('kenny.mp3', 'rb').read())
        # mp3part.add_header('Content-Disposition', 'attachment', filename='benny.mp3')
        # msg.attach(mp3part)

        # pdf类型附件
        # part = MIMEApplication(open('foo.pdf', 'rb').read())
        # part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
        # msg.attach(part)

        try:
            # s = smtplib.SMTP()  # 创建邮件服务器对象
            s = SMTP_SSL(self.mail_host)
            s.set_debuglevel(1)
            s.ehlo(self.mail_host)
            # s.connect(self.mail_host)  # 连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)  # 登录到你邮箱
            s.sendmail(me, self.mail_list, msg.as_string())  # 发送内容
            s.close()
            print("Send success!!")
            return True
        except Exception as e:
            print(str(e))
            return False

