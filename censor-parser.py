from bs4 import BeautifulSoup
import urllib.request
from argparse import ArgumentParser
import time
import re

from langdetect import detect
detect.seed = 0

from polyglot.text import Text

#Получить аргументы и применить параметры
pagecount = 0

#Задержка между обработкой ссылок
pagedelay = 1

pagecount = 1
lang = 0
clear = 0

parser = ArgumentParser()
parser.add_argument("-p", "--pages", dest="pages", help="Pages count (0 - all)")
parser.add_argument("-l", "--lang", dest="lang", help="uk, ru (0 - all)")
parser.add_argument("-c", "--clear", dest="clear", help="0 - no, 1 - yes")

args = parser.parse_args()

pagecount = args.pages
lang = args.lang
clear = args.clear

 #Запись в CSV шапки
with open("out.csv", "a", encoding='utf-8') as file:
    file.write("Author;Text;Language;Polarity()" + "\n")

#Получить ссылку на последнюю страницу и количество страниц

main_page = urllib.request.urlopen("https://censor.net/ua/news/all")
soup_main = BeautifulSoup(main_page, "html.parser")
for link in soup_main.findAll('a', {"class": "pag_last"}):
    print(link.get('href'))

censor_total_pages = link.get('href').split("/")
print ("Total pages: " + censor_total_pages[7])

if pagecount == 0:
    pagecount = censor_total_pages[7]

pagecount_counter = 1
pagecount_counter_max = censor_total_pages[7]

#Только первая страница
while pagecount_counter <= int(pagecount) and pagecount_counter <= int(pagecount_counter_max):
    #Создать массив ссылок с превой страницы
    current_page_url = "https://censor.net/ua/news/all/page/" + str(pagecount_counter) + "/category/0/interval/5/sortby/date"

    print("Page URL: " + current_page_url)
    print("News links:")

    #Ссылки на все новости с первой страницы
    current_page = urllib.request.urlopen(current_page_url)
    soup_current = BeautifulSoup(current_page, "html.parser")
    for link_current in soup_current.findAll('a', {"class": "news-list-item__link"}):
        print(link_current.get('href'))
        #Поиск комментариев в каждой новости
        news_page = urllib.request.urlopen(link_current.get('href'))
        soup_news = BeautifulSoup(news_page, "html.parser")
        #Массив для хранения комментариев с текущей страницы
        comments_array = []
        #Все никнеймы на странице
        for news_current in soup_news.findAll('a', {"class": "comments-item__author user_profile"}):
            #Запись в массив
            comments_array.append(news_current.getText().replace(";", ",").strip())

        #Тексты комментариев на странице
        comment_counter = 0
        for news_current in soup_news.findAll('div', {"class": "comments-item__wrapp"}):
            #Запись в массив
            current_comment_body = news_current.getText().replace(";", ",").replace("\n", " ").replace("\r", "").strip()
            if clear == 1:
                #Дополнительная очистка регулярным выражением
                current_comment_body = re.sub(r'[\W_]+', '', current_comment_body).lower()
            comments_array[comment_counter] = comments_array[comment_counter] + ";" + current_comment_body
            print(comments_array[comment_counter])

            #Определение языка
            try:
                comment_lang = detect(current_comment_body)
                print(comment_lang)
            except:
                comment_lang = "-"
                print(comment_lang)
            comments_array[comment_counter] = comments_array[comment_counter] + ";" + comment_lang

            #Определение тональности текста
            try:
                text = Text(current_comment_body, comment_lang)
                polarity = str(text.polarity)
                comments_array[comment_counter] = comments_array[comment_counter] + ";" + polarity
                print(polarity)
            except:
                comments_array[comment_counter] = comments_array[comment_counter] + ";" + "-"
            
            #Проверка фильтра языков
            if comment_lang == lang or lang == str(0):
                #Запись в CSV с никнеймом автора, языком и другими параметрами
                with open("comment_corpus.csv", "a", encoding='utf-8') as file:
                    file.write(comments_array[comment_counter] + "\n")

            comment_counter = comment_counter + 1
        time.sleep(pagedelay)

    pagecount_counter = pagecount_counter + 1
    time.sleep(pagedelay)



    
    


