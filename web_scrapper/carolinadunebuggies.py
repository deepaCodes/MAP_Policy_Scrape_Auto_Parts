import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/CarolinaDuneBuggies_Results.csv'
start_page = 1
total_search_pages = 100
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
    print("calling page {}".format(url))

    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    actual_res = [{'name': li_el.find('div', {'class', 'head-h3 product-name'}).text,
                   'price': li_el.find('span', {'class': 'price product-price'}).text.split('$')[-1]}
                  for li_el in soup.findAll('li', {'class': 'product-cell box-product'})]

    return actual_res


def scrape_carolinadunebuggies():
    base_url = 'https://carolinadunebuggies.com/xcart5.3/?target=search&mode=search&including=all&pageId={}'
    final_result = []

    for page in range(start_page, total_search_pages):
        link_res = get_collection_result(base_url.format(page))
        if not link_res:
            break
        final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_carolinadunebuggies()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
