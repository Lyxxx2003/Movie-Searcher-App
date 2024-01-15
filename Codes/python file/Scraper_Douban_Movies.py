import os
import threading
import time

# Store data into tree
from lxml import etree

# Import webdriver
from selenium import webdriver

def get_text(text):
    if text:
        return text[0]
    return ''

# Get respond from the website
def get_response_by_selenium(url):
    # 1、Create a driver
    chrome_options = webdriver.ChromeOptions()
    path_chrome_driver = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path_chrome_driver, options=chrome_options)

    # 2、Request url
    driver.get(url)

    time.sleep(1)
    # 3、Retrieve the source code of the webpage
    html_str = driver.page_source
    driver.close()
    return html_str

# Find the location of each target elements
def parse_page(div_list):
    books = []
    count = 0
    for div in div_list:
        # The name of the movies
        name_list = get_text(div.xpath('.//div[@class="title"]/a/text()'))
        name_date = name_list.split('\u200e')
        date = ""
        if len(name_date) > 1:
            name = name_date[0]
            date = name_date[1]
        else:
            name = name_date[0]
        # scores
        scores = get_text(div.xpath('.//span[@class="rating_nums"]/text()'))
        # description
        info = get_text(div.xpath('.//div[@class="meta abstract"]/text()'))
        # character
        character = get_text(div.xpath('.//div[@class="meta abstract_2"]/text()'))
        detail_url = get_text(div.xpath('.//div[@class="title"]/a/@href'))

        item = {'name': name, 'scores': scores, 'character': character, 'date': date, 'description': info, 'detail_url': detail_url}
        books.append(item)
        count += 1
    return books

# Actually crawl the data
def do_crawl_movie(search_txt: str, page_size: int): # parameter is input
    base_url = f'https://search.douban.com/movie/subject_search?search_text={search_txt}&start=%s'
    spider_movive = []
    for i in range(page_size):
        html_str = get_response_by_selenium(base_url % (i * 15))
        tree = etree.HTML(html_str)
        div_list = tree.xpath('//div[@id="root"]/div/div[2]/div/div/div')
        # If div_list is empty，end loop
        if not div_list:
            break
        temp = parse_page(div_list)
        spider_movive.append(temp)
    return spider_movive # output
