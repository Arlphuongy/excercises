import subprocess
import pyautogui as pag
import time

#opening word application 
process = subprocess.Popen("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk", shell=True)
time.sleep(2)

#opening the file 
pag.hotkey('alt', 'f')
pag.press('o')
pag.press('e')
pag.write('dataset')
time.sleep(2)
pag.press('enter')

# #waiting for file to open
time.sleep(30)

# #translating the page
pag.hotkey('alt', 'r')
pag.press('l')
pag.press('down')
pag.press('enter')

# #waiting for file to finish translating


# #saving the page into src folder
pag.hotkey('alt', 'f')
pag.press('a')
time.sleep(2)
pag.press('o')
time.sleep(2)
pag.write('translated_text')
pag.hotkey('alt', 'd')
pag.write(r'C:\Users\ASUS\Desktop\Practice\src')
pag.hotkey('alt', 's')

# #close window
time.sleep(2)
pag.hotkey('alt', 'f4')
time.sleep(2)
pag.hotkey('alt', 'f4')

# #task 1 and also extracting the doc into txt
time.sleep(3)
import docx
doc = docx.Document('src/translated_text.docx')
text = ""
for paragraph in doc.paragraphs:
    text += paragraph.text + "\n"

file = open('src/translated_text.txt', 'w', encoding='utf-8')
file.write(text)
file.close()






