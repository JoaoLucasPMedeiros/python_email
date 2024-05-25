import google.generativeai as genai
GOOGLE_API_KEY='AIzaSyBW5t_80nKFzVUfW3HvLyktXs6EvXU25VA'
genai.configure(api_key=GOOGLE_API_KEY)

#for modelo in genai.list_models():
#  if 'generateContent' in modelo.supported_generation_methods:
#    print(modelo.name)


model = genai.GenerativeModel(model_name='gemini-1.0-pro')

# Resposta
def ia (p):

    response = model.generate_content(p)
    print(response.text)
#
#
#prompt = 'categorize emails em três categorias distintas com base em suas características. Os dados de entrada incluem informações sobre o assunto, remetente, data e mensagem de cada email. O objetivo é categorizar os emails para ajudar o usuário a organizar sua caixa de entrada de forma mais eficiente. O modelo deve retornar um JSON contendo os emails categorizados. Certifique-se de que, mesmo que os emails estejam em diferentes idiomas, o retorno seja sempre em português (pt-br) esse é o email. ',lista_email_json
## onde está o aquivo
#arquivo = ia(prompt)
