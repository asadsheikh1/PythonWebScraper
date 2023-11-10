from bs4 import BeautifulSoup
import requests
import pandas as pd


def find_clothes():
    data = []

    for i in range(1, 44):
        html_text = requests.get(f'https://www.gulahmedshop.com/women?p={i}')
        soup = BeautifulSoup(html_text.content, 'html.parser')

        listings = soup.find_all('li', class_='item product product-item')

        for listing in listings:
            name = listing.find('span', class_='product-item-link').get_text(strip=True)
            prices = listing.find('div', class_='price-box price-final_price').text.split('    ')
            url = listing.find('div', class_='product details product-item-details').a['href']

            html_text = requests.get(url)
            soup = BeautifulSoup(html_text.content, 'html.parser')

            sku = soup.find('div', class_='product attribute sku').find('div', 'value').text
            details = soup.find('div', class_='product info detailed general')
            more_info = details.find('div', class_='additional-attributes-wrapper table-wrapper').table.tbody.find_all('td', class_='col data')
            more_info = [td.get_text(strip=True) for td in more_info]
            more_info = ', '.join(more_info)

            if len(prices) > 1:
                pirces_list = []
                for string in prices:
                    words = string.split()
                    for word in words:
                        word = word.replace(',', '')
                        if word.isdigit():
                            pirces_list.append(word)
                old_price = pirces_list[1]
                new_price = pirces_list[0]
                saved_price = pirces_list[2]

                row = {
                    'name' : name,
                    'new_price' : new_price,
                    'old_price' : old_price,
                    'saved_price' : saved_price,
                    'sku' : sku,
                    'url' : url,
                    'more_info' : more_info
                }

            else:
                prices_list = [''.join(letter for letter in word if letter.isdigit() or letter == ',') for word in prices]
                old_price = prices_list[0]
                new_price = 0
                saved_price = 0

                row = {
                    'name' : name,
                    'new_price' : new_price,
                    'old_price' : old_price,
                    'saved_price' : saved_price,
                    'sku' : sku,
                    'url' : url,
                    'more_info' : more_info
                }

            data.append(row)

    return data


df = pd.DataFrame(find_clothes())
df.to_csv('gul_ahmed.csv')

print(pd.read_csv('gul_ahmed.csv'))
