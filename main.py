import requests
import json
import re
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



class DataAnalizer:
    path = '/home/andrey/net_task2_pr/file1.json'
    ua = UserAgent()
    headers = {'User-Agent': ua.ff}
    
    def __init__(self):
        self.data_dict = {}

    def get_dict_data(self, page:int) -> dict:
        counter = 1
        count = 0
        while count < page:
            # time.sleep(1)
            url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={}'.format(count)
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            data = soup.find_all('div', class_='serp-item')
            for item in data:
                salary = item.find('span', class_='bloko-header-section-3')
                if salary:
                    salary = salary.text.replace('\u202f', '').replace('\u2013', '\u002d')
                else:
                    salary = 'not specified'
                description = item.find('a', class_= 'serp-item__title').text
                company_name = item.find('div', class_='vacancy-serp-item__meta-info-company').text
                city_name = item.find('div', {'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}).text
                link = item.find('a', class_='serp-item__title').get('href')
                if self.match_pattern(link):
                    if description not in self.data_dict:
                        description = description
                    else:
                        description = description + str(counter)
                        counter += 1
                    self.data_dict[description] = {'link': link, 'name': company_name, 'city': city_name, 'salary': salary }
            count += 1
            print(count)
        return self.data_dict

    def match_pattern(self, link:str) -> bool:
        response = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        vacancy_description = soup.find('div', class_='vacancy-description')
        if not vacancy_description:
            return False
        vacancy_description = vacancy_description.text
        pattern = r"(.*([Dd]jango).*([Ff]lask).*)|(.*([Ff]lask).*([Dd]jango).*)" 
        res = re.search(pattern, vacancy_description)
        if res:
            return True
        return False


if __name__ == '__main__':
    danalizer = DataAnalizer()
    data_dict = danalizer.get_dict_data(page=40)
    with open(danalizer.path, 'w', encoding='utf8') as file:
        json.dump(data_dict, file, ensure_ascii=False)







