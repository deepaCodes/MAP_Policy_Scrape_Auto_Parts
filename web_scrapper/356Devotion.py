import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/356Devotion_Results.csv'
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
    url_result = []

    for page in range(1, 10):
        print("calling {} page={}".format(url, page))

        response = requests.get('{}?page={}'.format(url, page), headers=headers, timeout=request_timeout)
        if response.status_code == 404:
            break
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features='lxml')
        if not soup.find('ul', {'class': 'ProductList'}).findAll('li'):
            break

        # get each product details
        product_links = [li_el.find('a').attrs['href'] for li_el in
                         soup.find('ul', {'class': 'ProductList'}).findAll('li')]
        for p_link in product_links:
            response = requests.get(p_link, headers=headers, timeout=request_timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, features='lxml')
            name = soup.find('h1', {'itemprop': 'name'}).text
            sku = soup.find('span', {'itemprop': 'sku'}).text.strip()
            price = soup.find('span', {'class': 'ProductPrice VariationProductPrice'}).text.strip().split('$')[1]
            url_result.append({'name': name, 'sku': sku, 'price': price})

    return url_result


def scrape_356devotion():
    base_url = 'http://356devotion.com/356-porsche-parts'
    final_result = []

    response = requests.get(base_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    link_list = [a_el.attrs['href'] for a_el in soup.find('div', {'class': 'CategoryList'}).findAll('a')]

    for link in link_list:
        link_res = get_collection_result(link)
        if not link_res:
            continue
        final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_356devotion()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
