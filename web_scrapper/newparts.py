import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/NewParts_Results.csv'
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
    url = "https://www.newparts.com/ajaxSearchResultProducts.aspx"

    payload = {'portalID': ' 10263',
               'CurrentTabName': ' products',
               'itemsPerPage': ' 1000',
               'currentPage': ' 1',
               'resultView': ' list'}

    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.newparts.com',
        'referer': url,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Cookie': '__cfduid=de87368489937616dc95c87aeede660321593639092; .ASPXANONYMOUS=jehzJw5VJhIq85ImcSm4fSt55NwOozY1snyBQJnL6lNSz7gc7kgPb3_iUpyvD_NuvO8gjUpQsp7TptbOqN3Z6bciEuhL7z_7bUaCC4tPun8B7-CFENMFndGfBSl7yKbR12cwXem18gtjmk3hoOpPdQ2; wholesale=; ASP.NET_SessionId=oqojqskakq2han5bhmicnajn; firstTouch=source=https://www.newparts.com/products/accessories-and-fluids&tick=637292218455661630'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    print('test')

    return None



def scrape_newparts():
    base_url = 'https://www.newparts.com'
    final_result = []

    response = requests.get(base_url, headers=headers, timeout=request_timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')

    collection_links = [li_el.find('a').attrs['href'] for div_el in
                        soup.findAll('div', {'class': 'column col-md-4'})[:3] for li_el in div_el.findAll('li')]

    for link in collection_links:
        link_res = get_collection_result('{}{}'.format(base_url, link))
        if link_res:
            final_result.extend(link_res)

    print('result count : {}'.format(len(final_result)))

    return final_result


def scrape_website():
    final_result = scrape_newparts()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
