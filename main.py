from turtle import up
import lxml
import time
import os
import json

from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

VERSION=["1.3.235.2"]

def original_version(version):
    return version[0]


def login(url, username, password):
    print("[+]...Открываю браузер...")    
    driver = webdriver.Firefox()
# Входим на сайт
    driver.get(url)
# Находим и заполняем поле Username
    print("[+]...Ввожу Username...")    
    username_form = driver.find_element(By.ID, "username")     
    username_form.send_keys(username)  
# Находим и заполняем поле Password        
    print("[+]...Ввожу Password...")
    password_form = driver.find_element(By.ID, "password")
    password_form.send_keys(password)
# Входим
    print("[+]...Вхожу на сайт...")
    time.sleep(1)
    password_form.send_keys(Keys.RETURN)    
# Сохраняем страницу
    time.sleep(4)
    html = driver.page_source
    with open("list_base.html", 'w', encoding="utf-8") as file:
        file.write(html)
    print("[+]...Веб страница сохранена...")
# Закрываем браузер
    print("[+]...Закрываю браузер...")
    driver.close()
    

def search_all_versions(file_name):
    list_releases=[]
# Открываем html в переменную data
    with open(file_name, 'r', encoding="utf-8") as file:
        data = file.read()
# Запихиваем ее в BS4    
    soup = BeautifulSoup(data, 'lxml')
# Вытаскиваем таблицу из html
    table = soup.find('table', class_='customTable table-hover')
# Вытаскиваем все строки (tr) без заголовка
    row_list = table.find_all('tr')[1:]
# Вытаскиваем из каждой строки колонку и вставляем в список
    id = 0
    
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
            'id': id,
            'number_version': number_version,
            'date_release': date_release,
            'update_version': update_version,
        })
        id += 1
# И сохраняем все в json

        with open('list_releases.json', 'w', encoding="utf-8") as file:
            json.dump(list_releases, file, indent=4, ensure_ascii=False)
    
        

def serch_up_for_my_version(list_releases, version):       
# Открываем файл на чтение
    with open(list_releases, 'r', encoding="utf-8") as file:
        data = json.load(file)  
# Проходимся по каждому элемента json для сравнения версий и выводим количество версий для обновлени
    count = 0
    new_ver = ''
    for ver in data:    
# Проверяем совпадение текущей версии и списка новых версий   
        try:
            if (ver['number_version'].split('.')[2] != version[0].split('.')[2]) and (version[0] not in ver['update_version']):
                new_ver = f'Новая версия == {ver['number_version']} от {ver["date_release"]}'           
        except:
            pass
# Проверяем совпадение текущей версии и списка версий для обновлений
        try:    
            if version[0] in ver['update_version']:
                count += 1
        except:
            pass        
# Если доходим до текущей версии прекращам цикл
        if ver['number_version'] == version[0]:
                break
# Возвращаем сообщение
    message_version = f'База "Управление Торговлей 1.3\n\nТвоя версия == {version[0]}\nДоступно обновлений этой версии == {count}\n{new_ver}\n\nНе мучай себя и коллег...\nПожалуйста обнови версию...'
    return message_version

def update_version(new_version):
    global VERSION
    VERSION[0] = new_version
    

# def main():
#     login(os.getenv('URL'), os.getenv('LOGIN'), os.getenv('PASSWORD'))    
#     search_all_versions('list_base.html')
#     serch_up_for_my_version('list_releases.json', VERSION[0])   


if __name__ == "__main__":
    main()