import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/PartsPlaceInc_Results.csv'
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_collection_result(url):
    print("calling page {}".format(url))

    response = requests.get(url, headers=headers, timeout=request_timeout, params={'limit': 'all'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    actual_res = [
        {'name': div_el.find('div', {'class': 'product-name'}).text.strip(), 'sku': div_el.find('b').text.split(':')[1],
         'price': div_el.find('span', {'itemprop': 'price'}).text.split('$')[1]} for div_el in
        soup.findAll('div', {'class': 'product-main-info'})]

    return actual_res


def scrape_partsplaceinc():
    base_url = 'https://www.partsplaceinc.com/vw-tdi-engine-parts.html'
    final_result = []

    response = requests.get(base_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    link_list = [label_el.find('a').attrs['href']
                 for label_el in soup.find('ul', {'id': 'outer_ul'}).findAll('label', {'class': 'main-element'})]

    for link in link_list:
        link_res = get_collection_result(link)
        if not link_res:
            break
        final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_partsplaceinc()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
