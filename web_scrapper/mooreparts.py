import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/MooreParts_Results.csv'
request_timeout = 30
total_search_pages = 10000
items_per_page = 100

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_page_result(api_key):
    base_url = 'https://www.searchanise.com/getresults'
    params = {
        'api_key': api_key,
        'q': '',
        'sortBy': 'relevance',
        'sortOrder': 'desc',
        'items': 'true',
        'maxResults': items_per_page
    }

    products = []
    for page in range(0, total_search_pages):
        headers['referer'] = 'https://www.mooreparts.com/search-results-page?tab=products&page={}'.format(page + 1)
        params['startIndex'] = page * items_per_page

        response = requests.get(base_url, headers=headers, params=params, timeout=request_timeout)
        response.raise_for_status()
        print(response.url)

        result = response.json()
        products.extend(result['items'])
        if result['currentItemCount'] == 0:
            break

    print('total products : {}'.format(len(products)))
    results = [{'name': row['title'], 'sku': row['product_code'], 'price': row['price']} for row in products]
    return results


def scrape_mooreparts():
    home_page = 'https://www.mooreparts.com'

    response = requests.get(home_page, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    api_keys = [sc_el.attrs['src'].split('=')[1] for sc_el in soup.findAll('script') if
                'src' in sc_el.attrs and 'api_key' in sc_el.attrs['src']]
    if not api_keys:
        return pd.DataFrame()

    api_key = api_keys[0]
    print('api_key: {}'.format(api_key))

    results = get_page_result(api_key)
    return results


def scrape_website():
    final_result = scrape_mooreparts()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
