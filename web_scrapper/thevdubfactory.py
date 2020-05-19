import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/TheVDubFactory_Results.csv'
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


def get_page_result(url):
    base_url = 'https://thevdubfactory.com'
    print('calling page - {}'.format(url))
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    next_page_results = []

    print('got result for :{}'.format(url))
    soup = BeautifulSoup(response.text, features='lxml')

    for div_el in soup.findAll('div', {'class': 'grid__item wide--one-fifth large--one-quarter medium-down--one-half'}):
        title = div_el.find('p', {'class': 'grid-link__title'}).text.strip()
        price = div_el.find('p', {'class': 'grid-link__meta'}).findAll(text=True, recursive=False)[-1].strip()
        href_link = div_el.find('a', {'class': 'grid-link'}).attrs['href']
        product_page_link = base_url + href_link
        sku = find_sku_frm_href(product_page_link)
        next_page_results.append({'title': title, 'price': price,'sku':sku ,'product_link': product_page_link})

    return next_page_results


def scrape_thevdubfactory():
    pagination_url = 'https://thevdubfactory.com/collections/all?page={}'
    final_result = []

    for page in range(start_page, total_search_pages):
        try:
            next_page = pagination_url.format(page)
            next_page_result = get_page_result(next_page)
            if not next_page_result:
                break
            final_result.extend(next_page_result)

        except Exception as ex:
            print(ex)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_thevdubfactory()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
