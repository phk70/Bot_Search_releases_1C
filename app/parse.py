import time
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from database.requests import get_last_version_from_db

load_dotenv()


# Вход на сервис 1С
async def login(url, username, password):
    print("[+]...Открываю браузер...")    
    driver = webdriver.Firefox()
    driver.get(url)  # Входим на сайт

    print("[+]...Ввожу Username...")    
    username_form = driver.find_element(By.ID, "username")     
    username_form.send_keys(username) 

    print("[+]...Ввожу Password...")
    password_form = driver.find_element(By.ID, "password")
    password_form.send_keys(password)

    print("[+]...Вхожу на сайт...")
    time.sleep(2)
    password_form.send_keys(Keys.RETURN)    
    time.sleep(6)
    html = driver.page_source
    # with open("list_base.html", 'w', encoding="utf-8") as file:  # Сохраняем страницу
    #     file.write(html)

    print("[+]...Веб страница сохранена...")
    print("[+]...Закрываю браузер...")
    driver.close()
    return html

# Поиск всех доступных версий и запись их в файл
async def search_all_versions(file_name):
    list_releases=[]
# Открываем html в переменную data
    with open(file_name, 'r', encoding="utf-8") as file:
        data = file.read()
# Запихиваем ее в BS4    
    soup = BeautifulSoup(data, "lxml")
# Вытаскиваем таблицу из html
    table = soup.find("table", attrs={'class': 'customTable table-hover'}) 
# Вытаскиваем все строки (tr) без заголовка
    row_list = table.find_all("tr")[1:]
# Вытаскиваем из каждой строки колонку и вставляем в список     
    for row in row_list:
        td_list = row.find_all("td")
# Записываем из колонки с версиями       
        number_version = td_list[0].find('a').text.strip()
# Записываем из колонки с датой выхода
        date_release = td_list[1].text.strip()
# Записываем из колонки с версиями для обновлений   
        update_version = td_list[2].text.strip()
# Добавляем все в список
        list_releases.append({            
            'number_version': number_version,
            'date_release': date_release,
            'update_version': update_version,
        })       

        return list_releases 
    

# # И сохраняем все в json
#         with open('list_releases.json', 'w', encoding="utf-8") as file:
#             json.dump(list_releases, file, indent=4, ensure_ascii=False)
#     print("[+]...Все версии с сайта сохранены...")        


# Поиск обновлений для моей версии
async def serch_up_for_my_version(list_releases):     
# Добываем текущую версию  
    version = view_version()
# Открываем файл со всеми версиями на чтение
    with open(list_releases, 'r', encoding="utf-8") as file:
        data = json.load(file)  
# Проходимся по каждому элемента json для сравнения версий и выводим количество версий для обновлени
    count = 0
    new_ver = ''
    for ver in data:    
# Проверяем совпадение текущей версии и списка новых версий   
        try:
            if (ver['number_version'].split('.')[2] != version.split('.')[2]) and (version not in ver['update_version']):
                new_ver = f'Новая версия == {ver['number_version']} от {ver["date_release"]}'           
        except:
            pass
# Проверяем совпадение текущей версии и списка версий для обновлений
        try:    
            if version in ver['update_version']:
                count += 1
        except:
            pass        
# Если доходим до текущей версии прекращам цикл
        if ver['number_version'] == version:
                break
# Возвращаем сообщение
    message_version = f'База "УПП" 1.3\n\nТвоя версия == {version}\nДоступно обновлений этой версии == {count}\n{new_ver}\n\nНе мучай себя и коллег...\nПожалуйста обнови версию...'
    return message_version

async def check_version():
    html = await login(os.getenv('URL'), os.getenv('LOGIN'), os.getenv('PASSWORD'))
    list_releases = await search_all_versions(html)
    my_version = await get_last_version_from_db()
    
    print(f'Файл HTML == {html}')
    print(f'Список версий == {list_releases}')
    print(f'Моя версия == {my_version}')




