import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/DubParts_Results.csv'
start_page = 1
total_search_pages = 10
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def find_sku_frm_href(product_page_link):
    response = requests.get(product_page_link)
    soup = BeautifulSoup(response.text, features='lxml')
    sku = soup.find('span', {'class': 'variant-sku'}).text
    return sku


def get_collection_result(url):
    print('calling page - {}'.format(url))
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    next_page_results = []
    soup = BeautifulSoup(response.text, features='lxml')

    temp_res = [{'name': div_el.find('div', {'class': 'product-card__name'}).text.strip(),
                 'price': div_el.find('div', {'class': 'product-card__price'}).text.strip()
                 if div_el.find('div', {'class': 'product-card__price'}) else None}
                for div_el in soup.findAll('div', {'class': 'product-card__info'})]
    actual_res = [{'name': row['name'], 'price': row['price'].split('$')[-1] if row['price'] else None}
                  for row in temp_res]

    return actual_res


def scrape_dubparts():
    base_url = 'https://www.dubparts.com'
    final_result = []

    print('calling base page - {}'.format(base_url))

    response = requests.get('{}/collections'.format(base_url), headers=headers, timeout=request_timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features='lxml')
    collection_links = [a_el.attrs['href'] for a_el in soup.findAll('a', {'class': 'collection-card'})]

    for link in collection_links:
        for page in range(start_page, total_search_pages):
            collection_res = get_collection_result('{}{}?page={}'.format(base_url, link, page))
            if not collection_res:
                break
            final_result.extend(collection_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_dubparts()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
