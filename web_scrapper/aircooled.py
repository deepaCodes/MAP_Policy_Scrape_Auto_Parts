import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

csv_file_name = '../csv/AirCooled_Results.csv'
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_product_detail(url):
    try:
        response = requests.get(url, headers=headers, timeout=request_timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features='lxml')

        print('getting product {}'.format(url))

        title = soup.find('span',{'itemprop':'description'}).text.strip()
        price = soup.find('span',{'itemprop':'price'}).text.strip() if soup.find('span',{'itemprop':'price'}) else None
        sku = soup.find('span',{'class':'product_code'}).text.strip()
    except:
        return None

    return {'title':title, 'price' : price , 'sku' : sku}

def get_collection_result(url):
    print('processing {}'.format(url))

    product_links= []
    for page in range(1,2):
        print(url.format(page))
        response = requests.get(url.format(page), headers=headers, timeout=request_timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features='lxml')
        product_links.extend([a_el.attrs['href'] for a_el in soup.findAll('a',{'class':'productnamecolor colors_productname'})])

    final_link_list = set(product_links)
    product_info = []
    for product in final_link_list:
        product_info.extend(get_product_detail(product))

    print('processing completed: {}'.format(url))
    return product_info



def scrape_aircooled():
    base_url = 'http://vwparts.aircooled.net/v/vspfiles/templates/143/Menu_Popout_Data.js'
    final_result = []
    append_url = '?searching=Y&show=500&page={}'
    response = requests.get(base_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()

    url_list_raw = re.findall('url=(\S+);', response.text)
    url_list = []
    for url in url_list_raw:
        url_list.append(url.split(';')[0])

    for link in url_list:
        link_res = get_collection_result('{}{}'.format(link,append_url))
        if link_res:
            final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_aircooled()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
