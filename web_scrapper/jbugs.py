import requests
import pandas as pd

csv_file_name = '../csv/JBugs_Results.csv'
request_timeout = 30
total_search_pages = 10000
items_per_page = 100

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Host': 'api.searchspring.net',
    'Origin': 'https://www.jbugs.com',
    'Referer': 'https://www.jbugs.com/search.html?q='
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def get_page_result(url):
    print('getting result for -{}'.format(url))
    response = requests.get(url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    result_json = response.json()['results']
    result = []

    for res in result_json:
        name = res['name']
        sku = res['code']
        price = res['price']
        result.append({'name': name, 'sku': sku, 'price': price})

    return result


def scrape_jbugs():
    home_page = 'https://api.searchspring.net/api/search/search.json?resultsFormat=native&siteId=behvgi&page={}&resultsPerPage=500'
    results = []

    for page in range(1, 21):
        result = get_page_result(home_page.format(page))
        results.extend(result)

    return results


def scrape_website():
    final_result = scrape_jbugs()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
