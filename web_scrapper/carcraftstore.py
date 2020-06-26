import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/CarCraftStore_Results.csv'
request_timeout = 30
start_page = 1
total_search_pages = 65

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_collection_result(url):
    print('getting product details')

    response = requests.get(url, headers=headers, timeout=request_timeout, params={'limit': 'all'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    name = soup.find('div',{'class':'product-detail'}).find('h1').text.strip()
    price_el = soup.find('span',{'class':'prod-detail-cost-value'})
    price = price_el.text if price_el else None
    sku_el = soup.find('span',{'class':'prod-detail-part-value'})
    sku = sku_el.text if sku_el else None


    product_details = {'name':name,'price': price , 'sku': sku}
    return product_details


def get_base_links(url):
    append_url = 'http://carcraftstore.com'

    response = requests.get(url, headers=headers, timeout=request_timeout, params={'limit': 'all'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    base_link_per_page = ['{}{}'.format(append_url,div_el.find('a').attrs['href']) for div_el in soup.findAll('div',{'class':'product-list-options'})]

    return base_link_per_page


def scrape_carcraftstore():
    base_url = 'http://carcraftstore.com/search.aspx?find=&page={}'
    final_result = []
    base_link_collection = []

    for page in range(start_page, total_search_pages):
        base_link = get_base_links(base_url.format(page))
        if not base_link:
            break
        base_link_collection.extend(base_link)

    for link in base_link_collection:
        link_res = get_collection_result(link)
        final_result.append(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_carcraftstore()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
