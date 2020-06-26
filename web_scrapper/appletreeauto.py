import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/AppleTreeAuto_Results.csv'
start_page = 1
total_search_pages = 150
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
        {'name': div_el.find('a').text, 'price': div_el.find('span', {'class': 'currency'}).text.split('$')[1],
         'sku': div_el.find('div', {'class': 'sku'}).text.split(':')[1].strip()} for div_el in
        soup.findAll('div', {'class': 'details'})]

    return actual_res


def scrape_appletreeauto():
    base_url = 'https://www.appletreeauto.com/search.php?mode=search&page={}'
    final_result = []

    for page in range(start_page, total_search_pages):
        try:
            next_page = base_url.format(page)
            next_page_result = get_collection_result(next_page)
            if not next_page_result:
                break
            final_result.extend(next_page_result)

        except Exception as ex:
            print(ex)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_appletreeauto()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
