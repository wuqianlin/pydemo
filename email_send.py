import socks
import smtplib
from email.mime.text import MIMEText

proxy_host = "172.20.1.196"
proxy_port = 1080

# socks.set_default_proxy(socks.SOCKS4, proxy_host, proxy_port)
# socks.wrapmodule(smtplib)

email_host = "email_host"
email_user = 'email_user'  # 发送者账号
email_pwd = 'email_pwd'  # 发送者的密码
maillist = 'maillist'

# 收件人邮箱，多个账号的话，用逗号隔开
me = email_user
msg = MIMEText("hello cat")  # 邮件内容
msg['Subject'] = 'python测试'  # 邮件主题
msg['From'] = me  # 发送者账号
msg['To'] = maillist  # 接收者账号列表

smtp = smtplib.SMTP(email_host)
smtp.login(email_user, email_pwd)
smtp.sendmail(me, maillist, msg.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
smtp.quit()  # 发送完毕后退出smtp
print('email send success.')
