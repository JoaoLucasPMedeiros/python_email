import imaplib
import email
import email.header
from datetime import datetime
from function import replace_characters,decode_subject, formatDate,decode_body
from controller import ia
import json


# p = input("Fala comigo: ")
# ia(p)


# Configuração do IMAP
imap = imaplib.IMAP4_SSL("imap.gmail.com")
username = "joaoesamc01@gmail.com"
password = "yuwihpeynhepmfeq"
validad = imap.login(username, password)

# Funcionalidades disponiveis
# for i in imap.list()[1]:
#     l = i.decode().split(' "/" ')
#     print(l[0] + " = " + l[1])


# Logica do programa
imap.select("INBOX")
start_date = datetime(2024, 5, 21).strftime('%d-%b-%Y')
status, messages = imap.search(None, 'SENTSINCE', start_date)

lista_email = [];       
for num in messages[0].split()[::-1]:
 
       _, msg = imap.fetch(num, "(RFC822)") #NÃO ALTERA
       message = email.message_from_bytes(msg[0][1])  #NÃO ALTERA


       assunto     = decode_subject(message['Subject'])
       remetente   = replace_characters(message['From'])
       data        = formatDate(message['Date'])
       mensagem    = decode_body(message)

       lista_email.append ({
              "Assunto": assunto,
               "Remetente": remetente,
               "Data": data,
               "Mensagem": mensagem 
              })
       
with open('emails.json', 'w', encoding='utf-8') as f:
    json.dump(lista_email, f, ensure_ascii=False, indent=4)


       








    


