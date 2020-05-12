from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd
import re
import os
import time

website = 'https://www2.tirexo.com/films-bluray-hd-1080/'
waiting_time = 25

def run():
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    try:
        print("Here we go!!")
        browser.get(website)
        browser.implicitly_wait(waiting_time)
        # Getting pages's links of movies
        print("Getting links...")
        movies_dom = browser.find_elements_by_xpath('//*[@id="dle-content"]/div[1]')
        movies_links_dom = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/a[2]')
        movies_links = []
        movies = []
        links = []
        for l in movies_links_dom:
            movies_links.append(l.get_attribute("href"))
        # Getting informations of each movie
        print("Getting informations of each movie...")
        for l in movies_links:
            try:
                movie = []
                browser.get(l)
                browser.implicitly_wait(waiting_time)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/h2/b').text)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/ul/li[1]/div/span[2]/span').text)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/ul/span').text)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[3]/div[1]/table/tbody/tr/td[1]/a[1]').get_attribute("href"))
                movies.append(movie)
            except WebDriverException as e:
                print('Error getting page on a movie :/, skipping ...')
        # Getting UpToBox's links
        print("Getting UpToBox's links")
        for movie in movies:
            try:
                browser.get(movie[3])
                browser.implicitly_wait(waiting_time)
                browser.find_element_by_xpath('/html/body/center/div/div[2]/div/center/form/input').click()
                browser.implicitly_wait(waiting_time)
                links.append(browser.find_element_by_xpath('/html/body/center/div/div[2]/div/div[1]/a').get_attribute("href"))
            except WebDriverException as e:
                print('Skipping ...')
        print('Movies scrapped: ' + str(len(links)))
        # Saving the links in txt
        timestamp = int(time.time())
        file_name = "data/" + str(timestamp) + ".txt"
        print("Saving links on: " + file_name)
        file = open(file_name, "w")
        for l in links:
            file.write(l + '\n')
        file.close()
        # TODO: Ask if user want to download it on the NAS
    except NoSuchWindowException as e:
        print('Error window ... ;(')
    finally:
        print('Job done :)')
        browser.quit()
