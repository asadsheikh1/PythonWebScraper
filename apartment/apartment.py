from bs4 import BeautifulSoup
import requests
import csv

def find_apartments():
    url = 'https://www.apartments.com/pima-county-az/'
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    html_text = requests.get(url, headers=agent)
    soup = BeautifulSoup(html_text.content, 'lxml')
    
    apartments = soup.find_all('li', class_ = 'mortar-wrapper')

    for apartment in apartments:
        name = apartment.find('span', class_ = 'js-placardTitle title').text
        url = apartment.article.header.div.a['href']

        print(f'Name: {name}')
        print(f'URL: {url}')

        apartment_details(url)


def apartment_details(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    html_text = requests.get(url, headers=agent)
    soup = BeautifulSoup(html_text.content, 'lxml')
    detail = soup.find('div', class_ = 'profileContent')
    header = detail.header

    price_bed_range_list = []
    features = ''
    latitude = soup.find('meta', property='place:location:latitude')['content']
    longitude = soup.find('meta', property='place:location:longitude')['content']
    name = header.find('div', class_='propertyNameRow').h1.text.strip()
    raw_address = header.find('div', class_='propertyAddressContainer').h2.text
    address, location = address_formatter(raw_address)
    description = soup.find('section', class_='descriptionSection js-viewAnalyticsSection mortar-wrapper').p.text.strip().replace('\n', ' ').replace('  ', ' ')

    price_bed_range = detail.find_all('li', class_='column')
    unique_features = soup.find_all('li', class_='specInfo uniqueAmenity')

    for item in unique_features:
        feature = item.span.text.strip()
        features += feature + ","
    features = features[:-1]
    
    if features == '':
        unique_features = soup.find_all('div', class_='amenityCard')
    
        for item in unique_features:
            feature = item.p.text.strip()
            features += feature + ","
        features = features[:-1]

    for item in price_bed_range:
        label = item.find('p', class_='rentInfoLabel').text.strip()
        detail = item.find('p', class_='rentInfoDetail').text.strip()
        price_bed_range_list.append(detail)


    with open('post/apartments.csv', 'a', newline='') as f:
        field_names = ['latitude', 'longitude', 'name', 'address', 'location', 'description', 'features', 'price_range', 'bed', 'bath', 'square_feet']
        writer = csv.DictWriter(f, fieldnames=field_names)

        if f.tell() == 0:
            writer.writeheader()

    with open('post/apartments.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
    
        writer.writerow({
            'latitude': latitude,
            'longitude': longitude,
            'name': name,
            'address': address,
            'location': location,
            'description': description,
            'features': features,
            'price_range': price_bed_range_list[0],
            'bed': price_bed_range_list[1],
            'bath': price_bed_range_list[2],
            'square_feet': price_bed_range_list[3]
        })    

    print(latitude)
    print(longitude)
    print(name)
    print(address)
    print(location)
    print(description)
    print(features)


def address_formatter(address):
    sentences = address.split("–")

    if len(sentences) >= 2:
        address = ' '.join(sentences[0].split())
        location = sentences[1].strip()

    return address, location


find_apartments()
