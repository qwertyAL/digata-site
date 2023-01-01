import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random

pin = []
for i in range(6):
    pin.append(random.randint(0,9)) 

pin = "".join(map(str, pin))

addr_from = "digatareg@mail.ru"                  
addr_to   = "sergeyiksanov25@gmail.com"          
password  = "oq89mNircWEk4PFXvDex"               

msg = MIMEMultipart()                         
msg['From']    = addr_from                     
msg['To']      = addr_to                        
msg['Subject'] = 'Регистрация на сайт'            

body = 'Здравствуйте.\n \nНа сайте "digata" был запрос на создание учетной записи с указанием вашего адреса электронной почты.\n \nДля подтверждения новой учетной записи введите следующий код в окне сайта ' + pin + '.\n \nС уважением, администратор сайта.'
msg.attach(MIMEText(body, 'plain'))            

server = smtplib.SMTP('smtp.mail.ru', 25)    
server.set_debuglevel(True) 
server.starttls()
server.login(addr_from, password)
server.send_message(msg)
server.quit()                 