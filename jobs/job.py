from bs4 import BeautifulSoup
import requests
import time
import csv

def find_jobs():
    html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    with open('post/jobs.csv', 'a', newline='') as f:
        field_names = ['Index', 'Company', 'Skills', 'Date', 'More']
        writer = csv.DictWriter(f, fieldnames=field_names)

        if f.tell() == 0:
            writer.writeheader()
        
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text

        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']

            with open('post/jobs.csv', 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=field_names)
            
                writer.writerow({
                    'Index': index,
                    'Company': company_name.strip(),
                    'Skills': skills.strip(),
                    'Date': published_date,
                    'More': more_info
                })


if __name__ == "__main__":
    while True:
        find_jobs()
        # time_wait = 10
        # print(f'Waiting for {time_wait} seconds')
        # time.sleep(time_wait * 60)
