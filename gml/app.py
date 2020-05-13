# TODO: Ask if user want to download it on the NAS
# TODO: Ask user for number of pages
# TODO: Propose to user catgory of movies and language (Blu-ray, 4K, vostfr, french ...)

# TODO: Function for getting links

msg = "GML v1.0 by Maher LAAROUSSI"

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os, sys, re, csv, time, platform

website = 'https://www2.tirexo.com/films-bluray-hd-1080/'
waiting_time = 25
os_now = platform.system()

# Starting wedriver
try:
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
except NoSuchWindowException as e:
    print_newline('No GUI on system :(')

def run():

    # Variables
    u = 0
    movies_links = []
    movies = []
    links = []

    # Starting animation
    start_animation()

    # Getting useful data
    #category = input("\nChoose a category\n1.Blu-Ray 1080p\n2.UHD 2160p\nCategory? ")
    #clear_with_msg()
    #language = input("\nChoose a language\n1.Multi\n2.Vostfr\n3.French\nLanguage? ")
    #clear_with_msg()
    pages = input("\nHow many pages do you want to scrapping? ")
    clear_with_msg()

    try:
        print("Here we go!!")
        # Getting pages's links of movies
        movies_links = getting_links(pages)

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
        print_newline('Job done :)')

    except NoSuchWindowException as e:
        print_newline('No GUI on system :(')

    finally:
        browser.quit()

def print_erase(str):
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write(str)
    sys.stdout.flush()

def clear():
    if (os_now == "Linux"):
        os.system('clear')
    else:
        os.system('cls')

def clear_with_msg():
    if (os_now == "Linux"):
        os.system('clear')
    else:
        os.system('cls')
    print(msg)

def print_newline(str):
    sys.stdout.write('\n')
    sys.stdout.write(str)
    sys.stdout.flush()

def start_animation():
    animation = "|/-\\"
    for i in range(50):
        time.sleep(0.1)
        sys.stdout.write("\r[" + animation[i % len(animation)] + "] ")
        sys.stdout.write(msg)
        sys.stdout.flush()
    clear_with_msg()

def getting_links(pages):
    current_page = 1
    movies_urls = []
    pages = int(pages)
    while(current_page <= pages):
        current_url = website + "page/" + str(current_page) + "/"
        # Getting pages's links of movies
        browser.get(current_url)
        browser.implicitly_wait(waiting_time)
        print_erase("Getting links page " + str(current_page) + "/" + str(pages))
        movies_urls_dom = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/a[2]')
        for m in movies_urls_dom:
            movies_urls.append(m.get_attribute("href"))
        current_page = current_page + 1
    return movies_urls
