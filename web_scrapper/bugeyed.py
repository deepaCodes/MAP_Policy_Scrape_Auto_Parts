import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/Bugeyed_Results.csv'
start_page = 1
total_search_pages = 5
request_timeout = 30

headers = {
    'Host': 'www.bugeyed.net',
    'Referer': 'https://www.bugeyed.net/product-catalog.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',

}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df['sku'] = df['sku'].astype(str)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_page_result(url):
    print('calling page - {}'.format(url))
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()

    print('got result for :{}'.format(url))
    soup = BeautifulSoup(response.text, features='lxml')
    result = [{'name': div_el.find('h2', {'class': 'product-grid__title'}).text.strip(),
               'price': div_el.find('div', {'class': 'product-grid__price paragraph'}).text.strip()} for div_el in
              soup.findAll('div', {'class': 'product-grid__item'})]
    for item in result:
        item['sku'] = str(item.get('title').split('ITEM NO.')[1]).strip()

    return result


def scrape_bugeyed():
    url = 'https://www.bugeyed.net/product-catalog.html'
    pagination_url = 'https://www.bugeyed.net/store/element/{}/page/{}/pagination/{}'
    final_result = []

    print('calling first page - {}'.format(url))

    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features='lxml')
    result = [{'title': div_el.find('h2', {'class': 'product-grid__title'}).text.strip(),
               'price': div_el.find('div', {'class': 'product-grid__price paragraph'}).text.strip()} for div_el in
              soup.findAll('div', {'class': 'product-grid__item'})]

    for item in result:
        item['sku'] = str(item.get('title').split('ITEM NO.')[1]).strip()

    final_result.extend(result)

    div_attrs = soup.find('div', {'class': 'products__published'}).attrs
    data_page_element_id = div_attrs['data-page-element-id']
    data_page_id = div_attrs['data-page-id']

    for page in range(start_page, total_search_pages):
        try:
            next_page = pagination_url.format(data_page_element_id, data_page_id, page)
            next_page_result = get_page_result(next_page)
            if not next_page_result:
                break
            final_result.extend(next_page_result)

        except Exception as ex:
            print(ex)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_bugeyed()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
