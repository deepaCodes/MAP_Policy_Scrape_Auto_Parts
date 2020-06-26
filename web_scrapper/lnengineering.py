import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/LnEngineering_Results.csv'
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_product_details(final_link_list):
    final_res = []
    for link in final_link_list:
        print("getting product details for {}".format(link))
        response = requests.get(link, headers=headers, timeout=request_timeout, params={'limit': 'all'})
        response.raise_for_status()
        print("url - foramtt {}".format(response.url))

        soup = BeautifulSoup(response.text, features='lxml')
        product_grid = soup.find('ul', {'class': 'products-grid'})
        if product_grid:
            detail_list = [{'sku': li_el.find('p', {'class': 'sku'}).text.split(':')[1],
                            'name': li_el.find('a', {'class': 'product-name'}).text,
                            'price': li_el.find('span', {'class': 'price'}).text}
                           for li_el in
                           product_grid.findAll('li', {'class': 'item'})]
            final_res.extend(detail_list)

    return final_res


def get_inner_links(url):
    print("get inner link for {}".format(url))
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    inner_links = [row_in.contents[1].attrs['href'] for row in soup.find('ul', {'id': 'left-nav'}).findAll('li') for
                   row_in in row.find_all('li')]

    return inner_links


def scrape_lnengineering():
    base_url = 'https://lnengineering.com/products.html'
    final_link_list = []
    response = requests.get(base_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    left_nav_links = [li_el.contents[1].attrs['href'] for li_el in soup.find('ul', {'id': 'left-nav'}).findAll('li')]

    for link in left_nav_links:
        link_res = get_inner_links(link)
        if link_res:
            final_link_list.extend(link_res)
        else:
            final_link_list.append(link)

    final_result = get_product_details(final_link_list)

    return final_result


def scrape_website():
    final_result = scrape_lnengineering()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
