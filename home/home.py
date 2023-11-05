from bs4 import BeautifulSoup

with open ('home.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    print(soup.prettify())

    course_cards = soup.find_all('div', class_='card')

    for name in course_cards:
        course_name = name.h5.text
        course_price = name.a.text.split()[-1]

        print(f'{course_name}: {course_price}')