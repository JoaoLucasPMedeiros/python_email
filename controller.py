import google.generativeai as genai
import json

GOOGLE_API_KEY='AIzaSyD3yxSCek64grwAQqmKlLQhq3XR-4KBjgk'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name='gemini-1.0-pro')


# Abrir o arquivo JSON
caminho_arquivo = 'emails.json'  # Substitua pelo caminho do seu arquivo JSON
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    # Carregar o conteúdo do arquivo JSON como um dicionário Python
    dados = json.load(arquivo)


caminho_arquivo = 'emails.json'  # Substitua pelo caminho do seu arquivo JSON

# Abrir o arquivo JSON e carregar o conteúdo como um dicionário Python
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

def IA(p):
    
    chat = model.start_chat(history=[])
    prompt = (
        f"Leia os seguintes emails e categorize-os em três categorias distintas com base no conteúdo dos emails "
        f"e retorne uma estrutura JSON mas sem exibir os \n :\n\n"
        f"{json.dumps(p, ensure_ascii=False, indent=2)}\n\n"
        "Exemplo de estrutura JSON a ser retornada:\n"
        "{\n"
        '  "Categoria": "nome_da_categoria",\n'
        '  "Assunto": "assunto_do_email"\n'
        "}\n"
    )
    response = chat.send_message(prompt)
    return response.text

categorias_email = IA(dados)

# Salvar o resultado categorizado em um novo arquivo JSON
with open('categorias.json', 'w', encoding='utf-8') as f:
    json.dump(json.loads(categorias_email), f, ensure_ascii=False, indent=4)

print(categorias_email)




#with open('categorias.json', 'w', encoding='utf-8') as f:
#    json.dump(categorias_email, f)
#
#print('SUCESSO: JSON GERADO!!!')
#print('Extrutura: ', categorias_email)
