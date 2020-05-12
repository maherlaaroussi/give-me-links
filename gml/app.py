# TODO: Ask if user want to download it on the NAS
# TODO: Ask user for number of pages
# TODO: Propose to user catgory of movies and language (Blu-ray, 4K, vostfr, french ...)

# TODO: Function for getting links

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os, sys, re, csv, time

website = 'https://www2.tirexo.com/films-bluray-hd-1080/'
waiting_time = 25

def run():
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    u = 0
    try:
        print("Here we go!!")
        browser.get(website)
        browser.implicitly_wait(waiting_time)
        # Getting pages's links of movies
        print_erase("Getting links...")
        movies_dom = browser.find_elements_by_xpath('//*[@id="dle-content"]/div[1]')
        movies_links_dom = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/a[2]')
        movies_links = []
        movies = []
        links = []
        for l in movies_links_dom:
            movies_links.append(l.get_attribute("href"))
        # Getting informations of each movie
        print_erase("Getting informations of each movie...")
        for l in movies_links:
            try:
                movie = []
                browser.get(l)
                browser.implicitly_wait(waiting_time)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/h2/b').text)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/ul/li[1]/div/span[2]/span').text)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/ul/span').text)
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[3]/div[1]/table/tbody/tr/td[1]/a[1]').get_attribute("href"))
                movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[1]/span[1]').text)
                movies.append(movie)
                u = u + 1
                print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Getting: " + movie[0])
            except WebDriverException as e:
                print_erase('Error getting page on a movie :/, skipping ...')
        # Getting UpToBox's links
        print_erase("Getting UpToBox's links")
        for movie in movies:
            try:
                links.append(movie[0])
                links.append(movie[4])
                browser.get(movie[3])
                browser.implicitly_wait(waiting_time)
                browser.find_element_by_xpath('/html/body/center/div/div[2]/div/center/form/input').click()
                browser.implicitly_wait(waiting_time)
                links.append(browser.find_element_by_xpath('/html/body/center/div/div[2]/div/div[1]/a').get_attribute("href"))
            except WebDriverException as e:
                print_erase('Skipping ...')
        print_erase('Movies scrapped: ' + str(len(movies)))
        # Saving the links in txt
        timestamp = int(time.time())
        file_name = "data/" + str(timestamp) + ".txt"
        print_newline("Saving links on: " + file_name)
        file = open(file_name, "w")
        u = 0
        for l in links:
            file.write(l + '\n')
            u = u + 1
            if ((u % 3) == 0):
                file.write('\n')

        file.close()
    except NoSuchWindowException as e:
        print('Error GUI ... ;(')
    finally:
        print_newline('Job done :)')
        browser.quit()

def print_erase(str):
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write(str)
    sys.stdout.flush()

def print_newline(str):
    sys.stdout.write('\n')
    sys.stdout.write(str)
    sys.stdout.flush()

def getting_links(pages):
    page = 1
    while(page <= pages):
        page = page + 1
