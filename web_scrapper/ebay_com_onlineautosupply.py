import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/Ebay_Onlineautosupply_Results.csv'
start_page = 1
total_search_pages = 250
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',

}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_page_result(url):
    print('calling page - {}'.format(url))

    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    page_result = [{'name': div_el.find('a').text.strip(),
                    'price': div_el.find('span', {'class': 's-item__price'}).text.split('$')[1]} for div_el in
                   soup.findAll('div', {'class': 's-item__info clearfix'})]

    return page_result


def scrape_ebay_onlineautosupply():
    pagination_url = 'https://www.ebay.com/str/onlineautosupply?_pgn={}'
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
    final_result = scrape_ebay_onlineautosupply()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
