import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/Mofoco_Results.csv'
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


def get_collection_result(url):
    print("calling page {}".format(url))

    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    actual_res = [{'name': td_el.find('a').text.strip(),
                   'sku': td_el.find('div', {'class': 'catcode'}).text.split('#')[1].strip() if td_el.find('div', {
                       'class': 'catcode'}) else None,
                   'price': td_el.find('div', {'class': 'price'}).text.split('$')[1] if td_el.find('div', {
                       'class': 'price'}) else None
                   } for
                  td_el in soup.findAll('td', {'class': 'column2'})]

    return actual_res


def scrape_mofoco():
    base_url = 'https://www.mofoco.com/search.php?page={}'
    final_result = []

    for page in range(start_page, total_search_pages):
        link_res = get_collection_result(base_url.format(page))
        if not link_res:
            break
        final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_mofoco()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
