import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/Gowesty_Results.csv'
start_page = 0
#page numbers increment by 30 for each page
total_search_pages = 3000
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


def get_collection_result(url):
    print("calling page {}".format(url))

    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    temp_res = [{'title': div_el.find('p', {'class': 'product-name'}).text.strip(),
                 'price': div_el.find('p', {'class': 'product-price'}).text.strip(),
                 'code': div_el.find('p', {'class': 'product-code'}).text.strip()} for div_el in
                soup.findAll('div', {'class': 'product'})]

    temp_res_marked_red = [{'title': div_el.find('p', {'class': 'product-name'}).text.strip(),
                            'price': div_el.find('p', {'class': 'product-price'}).text.strip(),
                            'code': div_el.find('p', {'class': 'product-code'}).text.strip()
                            } for div_el in soup.findAll('div', {'class': 'product ribbon-wrapper-red'})]
    temp_res.extend(temp_res_marked_red)

    actual_res = [{'title': row['title'], 'price': row['price'].split('$')[-1], 'code': row['code'].split(':')[-1].strip()}
                  for row in temp_res]

    return actual_res


def scrape_gowesty():
    base_url = 'https://www.gowesty.com/search-results.php?start={}&search_phrase=&sort=score'
    final_result = []

    for page in range(start_page, total_search_pages, 30):
        link_res = get_collection_result(base_url.format(page))
        if not link_res:
            break
        final_result.extend(link_res)


    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_gowesty()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
