from imap_tools import MailBox, AND
from datetime  import datetime
import json
import re

data_inicial = datetime.strptime("20/05/2024", '%d/%m/%Y').date()

print(data_inicial)
username = "joaoesamc01@gmail.com"
password = "yuwihpeynhepmfeq"

lista_email_ = []

def formatar_assunto(assunto):
    assunto_formatado = re.sub(r'[^\x00-\x7F]+', ' ', assunto)
    return assunto_formatado

with MailBox('imap.gmail.com').login(username, password ) as mailbox:

    lista_email = list(mailbox.fetch(AND(date_gte=data_inicial)))

    for l in lista_email:
     assunto = l.subject
     msg     = (l.text)

     lista_email_.append(
        {
        'Assunto': formatar_assunto(assunto), 
        'Mensagem':msg
        }
        )

with open('emails.json', 'w', encoding='utf-8') as f:
    json.dump(lista_email_, f, ensure_ascii=False, indent=4)

print('SUCESSO: JSON GERADO!!!')