import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
from pprint import pprint
import json
 
headers = Headers(browser="Goolge", os="win")
# Находим page_max - номер последней страницы в поиске для возможности доступа ко всем отфильтрованным объявлениям
page = 0
html_data = requests.get(f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}", headers=headers.generate()).text
soup = BeautifulSoup(html_data, "lxml")
page_max = soup.find("div", class_="pager").find_all("a")[4].text
# Проходимся циклом по каждой странице и ищем необходимые данные, но в цикле указываем первые 2 страницы для тестового варианта
parsed_data = []
for page in range(0,2):
    html_data = requests.get(f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}", headers=headers.generate()).text
    soup = BeautifulSoup(html_data, "lxml")
    tag_vacancies = soup.find_all("div", class_="serp-item")
    for tag_vacancy in tag_vacancies:
        tag_span_salary = tag_vacancy.find_all("span")[2].text
        tag_a_company = tag_vacancy.find_all("a")[1].text
        tag_div_city = tag_vacancy.find_all("div")[15].text
        tag_h3 = tag_vacancy.find("h3")
        tag_a = tag_h3.find("a")
        link = tag_a["href"]
# По найденной ссылке на ваканию находим текст её описания для фильтрации по словам Django и Flask,
# для чего обрабатываем текст помощью регуляных выращжений и строковых методов
        tag_text_vacancy = requests.get(link, headers=headers.generate()).text
        soup_vacancy = BeautifulSoup(tag_text_vacancy, "lxml")
        tag_content = soup_vacancy.find("div", class_="g-user-content").text
        tag_content1 = re.sub(r'[^\w\s]','', tag_content.lower()).split(' ')
# при наличии в описании вакансии нужных слов, собираем список словарей с данными
        if 'django' in tag_content1 and 'flask' in tag_content1:
            data = {
                'link': link,
                'salary': tag_span_salary,
                'company': tag_a_company,
                'city': tag_div_city
            }
            parsed_data.append(data)
with open("vacation_file.json", "w") as pd:
    json.dump(parsed_data, pd, ensure_ascii=False)