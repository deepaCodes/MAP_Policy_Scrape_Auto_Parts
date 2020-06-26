import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/DuneBuggyWareHouse_Results.csv'
request_timeout = 30
start_page = 1
total_search_pages = 20

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_product_details(url):
    response = requests.get(url, headers=headers, timeout=request_timeout, params={'limit': 'all'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    name = soup.find('div', {'class': 'product-name'}).text.strip()
    price = soup.find('div', {'class': 'price-box'}).findAll('span', {'class': 'price'})[-1].text.split('$')[1].strip()
    sku = soup.find('th', text='SKU').find_next_sibling('td').text

    return {'name': name, 'price': price, 'sku': sku}


def get_page_result(url, page):
    print("calling page {},{}".format(url, page))

    response = requests.get(url, headers=headers, timeout=request_timeout, params={'limit': '36', 'p': page})
    print(response.url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    active_page_el = soup.find('li', {'class': 'current active'})

    if active_page_el:
        active_page = int(active_page_el.text)

        if page > active_page:
            return None
    elif page > 1 :
        return None


    product_links_in_page = [li_el.find('a').attrs['href'] for li_el in soup.findAll('li', {'class': 'item'})]
    product_details = []

    for link in product_links_in_page:
        product_details.append(get_product_details(link))

    return product_details


def get_collection_result(url):
    print("calling page {}".format(url))
    page_final_res = []

    for page in range(start_page, total_search_pages):
        link_res = get_page_result(url, page)
        if not link_res:
            break
        page_final_res.extend(link_res)

    return page_final_res


def scrape_appletreeauto():
    base_url = 'https://dunebuggywarehouse.com/bugpack.html'
    final_result = []

    response = requests.get(base_url, headers=headers, timeout=request_timeout, params={'limit': 'all'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    base_link_collection = [li_el.find('a').attrs['href'] for li_el in
                            soup.findAll('div', {'class', 'category-menu'})[1].findAll('li')[1:]]

    for link in base_link_collection:
        next_page_result = get_collection_result(link)
        final_result.extend(next_page_result)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_appletreeauto()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
