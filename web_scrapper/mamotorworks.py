import json
import re

import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/MaMotorWorks_Results.csv'
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_sub_link_details(url):
    append_url = 'https://www.mamotorworks.com/vw/category/{}'
    print('Getting Link detail for-- {}{}'.format(append_url, url))

    result = []
    soup = get_soup(append_url.format(url))
    if not soup.find('span', {'class': 'rddlFakeInput'}):
        sub_links = [li_el.find('a').attrs['href'] for li_el in soup.find('ul', {'class': 'catList'}).findAll('li')]
        for link in sub_links:
            result.extend(get_sub_link_details(link))
    else:
        result.append(url)

    return result


def get_soup(url):
    response = requests.get(url, headers=headers, timeout=request_timeout, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def get_product_details(url):
    append_url = 'https://www.mamotorworks.com/vw/category/{}'
    result = []

    for link in url:
        print('Getting product detail for-- {}{}'.format(append_url, link))
        soup = get_soup(append_url.format(link))
        if soup.find('span', {'class': 'rddlFakeInput'}):
            res = [{'name': li_el.find('h3', {'class': 'fs12'}).text.strip() if li_el.find('h3',
                                                                                           {'class': 'fs12'}) else None,
                    'sku': li_el.find('span').text if li_el.find('span') else None,
                    'price': li_el.find('span', {'class': 'darkBlue fwBold'}).text.split('$')[1].strip() if li_el.find(
                        'span', {'class': 'darkBlue fwBold'}) else None} for li_el in
                   soup.find('ul', {'class': 'featProd'}).findAll('li')]
            result.append(res)

    return result


def get_link_details(url):
    link_data = []

    sub_links = get_sub_link_details(url)
    link_data = get_product_details(sub_links)

    return link_data


def scrape_mamotorworks():
    base_url = 'https://www.mamotorworks.com/vw'
    final_res = []
    response = requests.get(base_url, headers=headers, timeout=request_timeout, verify=False)
    response.raise_for_status()
    url_value_list = json.loads('[{}]'.format(response.text.split('"itemData":[')[1].split(']')[0]))
    url_list = [row['value'] for row in url_value_list]

    for link in url_list:
        final_res.extend(get_link_details(link))

    return final_res


def scrape_website():
    final_result = scrape_mamotorworks()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
