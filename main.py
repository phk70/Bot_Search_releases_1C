import requests
import lxml
import time

from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from send_message_telegram import start, send_message
from env import USERNAME, PASSWORD, URL


VERSION="1.3.235.2"
LIST_RELEASES=[]

def login(url, username, password):
    print("[+]...Открываю браузер...")
    driver = webdriver.Firefox()
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
    with open("temp/html_page.html", 'w', encoding="utf-8") as file:
        file.write(html)
    print("[+]...Веб страница сохранена...")
# Закрываем браузер
    time.sleep(4)
    print("[+]...Закрываю браузер...")
    driver.close()
    

def search_all_versions(file_name):
# Открываем html в переменную data
    with open(f"temp/{file_name}", 'r', encoding="utf-8") as file:
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
# Записываем из колонки с версиями для обновлений   
        update_version = td_list[2].text.strip()
# Добавляем все в список
        LIST_RELEASES.append({
            'id': id,
            'number_version': number_version,
            'update_version': update_version,
        })
        id += 1
        

def serch_my_version(LIST_RELEASES, VERSION):         
    count=0

    for ver in LIST_RELEASES: 
        count += 1 
        if VERSION in ver['update_version']:    
            print(f'Вышло обновление {ver['number_version']}.')
            break  
    
    pprint(count)






def main():
    # login(URL, USERNAME, PASSWORD)
    search_all_versions("html_page.html")
    serch_my_version(LIST_RELEASES, VERSION)
    start('Текущая версия')
    send_message('текущая версия')

if __name__ == "__main__":
    main()