import json
from datetime import datetime
from imap_tools import MailBox, AND
from googleapiclient.discovery import build
from google.auth import credentials

username = "joaoesamc01@gmail.com"
password = "yuwihpeynhepmfeq"


with open("categorias.json", "r", encoding="utf-8") as arquivo:
    categorias = json.load(arquivo)

# Conectar-se à conta do Gmail usando imap-tools
with MailBox('imap.gmail.com').login(username, password) as mailbox:
    # Iterar sobre todas as categorias
    for categoria_info in categorias:
        categoria = categoria_info["Categoria"]
        assunto = categoria_info["Assunto"]
        
        # Verificar se a pasta da categoria já existe, senão criar
        if not mailbox.folder.exists(categoria):
            try:
                mailbox.folder.create(categoria)
                print(f"Pasta '{categoria}' criada com sucesso.")
            except Exception as e:
                print(f"Erro ao criar a pasta '{categoria}': {e}")
        
        # Consultar os emails na caixa de entrada que têm o assunto desejado
        emails_com_assunto = mailbox.fetch(AND(subject=assunto))
        
        # Iterar sobre os emails encontrados
        for email in emails_com_assunto:
            try:
                # Mover o email para a pasta correspondente à categoria
                mailbox.move(email.uid, categoria)
                print(f"Email com assunto '{email.subject}' movido para a pasta '{categoria}'")
            except Exception as e:
                print(f"Erro ao mover o email '{email.subject}' para a pasta '{categoria}': {e}")