import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re 
import json

class Parser:
    def __init__(self, URL, os, browser):
        self.URL = URL
        self.os = os
        self.browser = browser

    def header_gen(self):
        header_gen = Headers(self.os, self.browser)
        return header_gen

    def main_html(self):
        URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
        main_hh = requests.get(self.URL, headers=self.header_gen().generate())
        main_hh_html = main_hh.text
        return main_hh_html
    
    def main_soup(self):
        main_html = self.main_html()
        main_soup = BeautifulSoup(main_html, features='lxml')
        serp_list = main_soup.find(name='div', id='a11y-main-content')
        serp_tags = serp_list.find_all(class_='serp-item')
        return serp_tags
    
    def get_info(self):
        parsed_data = []
        for serp_tag in self.main_soup():
            headers_tag = serp_tag.find(name='h3', class_="bloko-header-section-3")
            a_tag = headers_tag.find(name='a')
            link = a_tag['href']
            link = link.split('?')[0]
            compensation_tag = serp_tag.find(name='span', class_="bloko-header-section-2")
            if compensation_tag is not None:
                compensation = compensation_tag.text
            else:
                compensation = "ЗП не указана"
            company_tag = serp_tag.find(name='a', class_='bloko-link bloko-link_kind-tertiary').text
            city_tag = serp_tag.find(name='div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            main_vacation = requests.get(link, headers=self.header_gen().generate())
            main_vacation_html = main_vacation.text
            off_soup = BeautifulSoup(main_vacation_html, features='lxml')
            class_list = off_soup.find(name='div', class_="HH-MainContent HH-Supernova-MainContent")
            class_list_html = class_list.text
            find_vacation = re.findall(r"Django|Flask", class_list_html)
            # find_dollars = re.findall(r"\$\d+", class_list_html) #на момент запуска не было на хх на главной странице вакансий с оплатой в долларах
            if len(find_vacation) > 0: #and len(find_dollars) > 0 код для добавления фильтра
                parsed_data.append({
                    'link': link,
                    'compensation': compensation,
                    'company': company_tag,
                    'city': city_tag
                })
        return parsed_data
    
class Save_json(Parser):

    def save_js(self):
        with open('vacancy_data.json', 'w') as f:
            json.dump(self.get_info(), f)

    def open_js(self):
        with open('vacancy_data.json', 'r') as f:
            parsed_data = json.load(f)
        return parsed_data
