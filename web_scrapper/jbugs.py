import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/JBugs_Results.csv'
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
    print('calling page - {}'.format(url))
    try:
        response = requests.get(url, headers=headers, timeout=request_timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features='lxml')

        if not soup.find('select', {'class': 'results_per_page_select'}):
            return None

        actual_res = [
            {'name': div_el.find('a', {'class': 'v-product__title productnamecolor colors_productname'}).text.strip(),
             'sku': div_el.find('p', {'class': 'text v-product__desc'}).text.strip(),
             'price': div_el.find('div', {'class': 'product_productprice'}).text.split('$')[1]} for div_el in
            soup.findAll('div', {'class': 'v-product'})]

        return actual_res
    except:
        pass
    return None


def scrape_jbugs():
    base_url = 'https://www.jbugs.com/search.html?q='
    final_result = []

    response = requests.get(base_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    print('test')
    collection_links = [li_el.find('a').attrs['href'] for li_el in soup.findAll('li', {'class': {'vnav__item'}})]

    for link in collection_links:
        link_res = get_collection_result(link)
        if link_res:
            final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_jbugs()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
