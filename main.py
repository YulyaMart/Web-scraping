import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def get_headers():
    return Headers(browser='firefox', os='win').generate()

def get_text(url):
    html_data = requests.get(url, headers=get_headers()).text
    soup = BeautifulSoup(html_data, 'lxml')
    return soup

def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def filter_vacancies(url):
    soup = get_text(url)   
    vacancy_list_tag = soup.find(class_='vacancy-serp-content')
    vacancy_tags = vacancy_list_tag.find_all('div', class_='serp-item')
    parsed_data = []
    for vacancy_tag in vacancy_tags:
        vac_link = vacancy_tag.find(class_='serp-item__title').get('href')
        vacancy_description_html = get_text(vac_link)
        vacancy_description = vacancy_description_html.find('div',class_='vacancy-description').text
        if 'Django' and 'Flask' in vacancy_description:
            salary_tag = vacancy_tag.find('span', class_='bloko-header-section-3').text
            salary_fork = salary_tag.replace('\u202f', ' ')
            vacancy_info_tag = vacancy_tag.find('div', class_='vacancy-serp-item__info')
            company_name = vacancy_info_tag.find('a', class_='bloko-link_kind-tertiary').text
            city = vacancy_info_tag.find('div', attrs = {'data-qa':'vacancy-serp__vacancy-address'}, class_='bloko-text').text
            parsed_data.append(
                {
                'link': vac_link,
                'salary_fork': salary_fork,
                'company_name': company_name,
                'city': city
                }
            )
    return save_json('vacancies', parsed_data)

if __name__ == '__main__':
    HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    filter_vacancies(HOST)
