import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = '../csv/MaMotorWorks_Results.csv'
request_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def save_to_excel(final_result):
    print('saving to excel')
    df = pd.DataFrame(final_result)
    df.to_csv(csv_file_name, index=True)

    print('saved to : {}'.format(csv_file_name))


def scrape_mamotorworks():
    base_url = 'https://www.mamotorworks.com/vw'
    response = requests.get(base_url, headers=headers, timeout=request_timeout, verify = False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='lxml')
    final_result = [{'name': li_el.find('h2').text.strip(),
                     'price': li_el.find('span', {'class': 'woocommerce-Price-amount amount'}).text.split('$')[1]} for
                    li_el in soup.find('ul', {'class': 'products'}).findAll('li')]

    return final_result


def scrape_website():
    final_result = scrape_mamotorworks()
    save_to_excel(final_result)


if __name__ == '__main__':
    scrape_website()
