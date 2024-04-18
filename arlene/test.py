import docx
from deep_translator import GoogleTranslator
# api_key = '614cfa1ce829dcc2cf48738e59e8307d'

def translate(text):
    translator = GoogleTranslator(source='auto', target='vi')
    translated = translator.translate(text)

    return translated

doc = docx.Document('src/dataset.docx')
text = ''
file = open('src/translated_text.txt', 'w', encoding='utf-8')
for para in doc.paragraphs:
    text = para.text 
    file.write(translate(text) + '\n')

file.close()










