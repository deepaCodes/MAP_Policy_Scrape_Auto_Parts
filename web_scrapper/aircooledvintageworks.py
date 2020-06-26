import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/AirCooledVintageWorks.com_Results.csv'
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_product_details(url):
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    name = soup.find('div',{'class':'product-name top-product-detail'}).find('h1').text.strip()
    price = soup.find('div',{'id':'price'}).find('div',{'class':'price'}).text
    sku = soup.find('div',{'class':'product-sku'}).text.split(':')[1]

    return {'name': name, 'sku': sku, 'price': price}



def get_collection_result(url, base_url):
    print("calling page {}".format(url))
    link_res = []
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    product_link_list = [a_el.attrs['href'] for a_el in soup.findAll('a', {'class': 'product-image'}) if
                         'href' in a_el.attrs]

    for link in product_link_list:
        product_info = get_product_details(base_url.format(link))
        link_res.append(product_info)

    return link_res


def scrape_aircooledvintageworks():
    home_url = 'https://www.aircooledvintageworks.com/search?q=&type=product&product_cat=all'
    base_url = 'https://www.aircooledvintageworks.com{}'
    final_result = []

    response = requests.get(home_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    link_list = [li_el.find('a').attrs['href'] for li_el in soup.find('ul', {'id': 'categories_nav'}).findAll('li')]
    link_list.pop(0)

    for link in link_list:
        link_res = get_collection_result(base_url.format(link), base_url)
        if not link_res:
            break
        final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_aircooledvintageworks()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
