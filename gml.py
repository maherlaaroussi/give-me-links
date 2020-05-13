#!/usr/bin/env python3

# TODO: Ask if user want to download it on the NAS
# TODO: Try to get download ink after geetting informations of each movie
# BUG: Scrapping randomly stop without getting any links

from settings import auto_config as cfg
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os, sys, re, csv, time

# CFG
header = cfg.HEADER
url = cfg.URL
url_movies_all = cfg.URL_MOVIES_ALL
url_movies_bluray1080 = cfg.URL_MOVIES_BLURAY1080
url_movies_uhd = cfg.URL_MOVIES_UHD
url_movies_french = cfg.URL_MOVIES_FRENCH
url_movies_vostfr = cfg.URL_MOVIES_VOSTFR
url_movies_multi = cfg.URL_MOVIES_MULTI
waiting_time = cfg.WAITING_TIME
waiting = cfg.WAITING
os_now = cfg.OS_NOW

# Starting wedriver
try:
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
except NoSuchWindowException as e:
    print_newline('No GUI on system :(')

def main():
    # Variables
    u = 0
    movies_links = []
    movies = []
    links = []
    website = ""

    # Starting animation
    start_animation()

    # Getting useful data
    website = choose_category()
    website = choose_language(website)
    pages = choose_pages()

    try:

        print("Here we go!!")

        # Getting pages's links of movies
        movies_links = getting_links(website, pages)

        # Getting informations of each movie
        movies = getting_informations(movies_links)

        # Getting dowload links
        links = getting_download_links(movies)

        # Saving the links in txt
        timestamp = int(time.time())
        file_name = "data/" + str(timestamp) + ".txt"
        print_newline("Saving links on: " + file_name)
        file = open(file_name, "w")
        for l in links:
            file.write(l + '\n')
            if ("http" in l):
                file.write('\n')
        file.close()
        print_newline("Job done!")

    except NoSuchWindowException as e:
        print_newline('No GUI on system :(')

    finally:
        browser.quit()

def print_erase(str):
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write(str)
    sys.stdout.flush()

def print_erase_persistent(str):
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write(str)
    sys.stdout.write("\n")
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
    print("[+] " + header)

def print_newline(str):
    sys.stdout.write('\n')
    sys.stdout.write(str)
    sys.stdout.flush()

def start_animation():
    clear()
    animation = "|/-\\"
    for i in range(50):
        time.sleep(0.1)
        sys.stdout.write("\r[" + animation[i % len(animation)] + "] ")
        sys.stdout.write(header)
        sys.stdout.flush()
    clear_with_msg()

def getting_links(website, pages):
    current_page = 1
    movies_urls = []
    pages = int(pages)
    while(current_page <= pages):
        # Getting url with page
        if (current_page == 1):
            current_url = website
        else:
            current_url = website + "page/" + str(current_page) + "/"
        # Getting pages's links of movies
        browser.get(current_url)
        browser.implicitly_wait(waiting_time)
        print_erase("[" + str(current_page) + "/" + str(pages) + "] Getting links page")
        movies_urls_dom = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/a[2]')
        for m in movies_urls_dom:
            movies_urls.append(m.get_attribute("href"))
        current_page = current_page + 1
    return movies_urls

def getting_informations(movies_links):
    movies = []
    u = 1
    print_erase("Getting informations of each movie...")
    for m in movies_links:
        try:
            wait()
            movie = []
            browser.get(m)
            browser.implicitly_wait(waiting_time)
            movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/h2/b').text)
            movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/ul/li[1]/div/span[2]/span').text)
            movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/ul/span').text)
            # UpToBox
            movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[3]/div[1]/table/tbody/tr/td[1]/a[1]').get_attribute("href"))
            movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[1]/span[1]').text)
            movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div/div[1]/span[2]').text)
            # 1fichier
            #movie.append(browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div/div[3]/div[2]/table/tbody/tr/td[1]/a').get_attribute("href"))
            movies.append(movie)
            print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Getting: " + movie[0])
        except WebDriverException as e:
            print_erase_persistent("[" + str(u) + "/" + str(len(movies_links)) + "] Error: WebDriverException")
        except NoSuchElementException as e:
            print_erase_persistent("[" + str(u) + "/" + str(len(movies_links)) + "] Error: element not found")
        finally:
            u = u + 1

    return movies

def getting_download_links(movies):
    print_erase("Getting download links")
    u = 1
    links = []

    for movie in movies:
        try:
            links.append(movie[0])
            links.append(movie[4])
            links.append(movie[5])
            links.append(bypass_protection(movie[3]))
            #links.append(bypass_protection(movie[6]))
            print_erase("[" + str(u) + "/" + str(len(movies)) + "] Getting download links")
            u = u + 1
        except WebDriverException as e:
            print_erase("[" + str(u) + "/" + str(len(movies)) + " Skipping ...")

    print_erase('Movies scrapped: ' + str(len(movies)))
    return links

def bypass_protection(link):
    browser.get(link)
    browser.implicitly_wait(waiting_time)
    browser.find_element_by_xpath('/html/body/center/div/div[2]/div/center/form/input').click()
    return browser.find_element_by_xpath('/html/body/center/div/div[2]/div/div[1]/a').get_attribute("href")

def choose_category():
    available_choice = [1, 2]
    isOK = False
    while (not isOK):
        category = input("\nChoose a category\n1. Blu-Ray 1080p\n2. UHD 2160p x265\nChoice? ")
        category = int(category)
        if (category in available_choice):
            isOK = True
            clear_with_msg()
            if (category == 1):
                website_category = url + url_movies_bluray1080
            elif (category == 2):
                website_category = url + url_movies_uhd
            return website_category
        else:
            clear_with_msg()


def choose_language(website):
    available_choice = [1, 2, 3]
    isOK = False
    while (not isOK):
        language = input("\nChoose a language\n1. Multi\n2. Vostfr\n3. French\nChoice? ")
        language = int(language)
        if (language in available_choice):
            isOK = True
            clear_with_msg()
            if (language == 1):
                website_language = website + url_movies_multi
            elif (language == 2):
                website_language = website + url_movies_vostfr
            elif (language == 3):
                website_language = website + url_movies_french
            return website_language
        else:
            clear_with_msg()

def choose_pages():
    clear_with_msg()
    pages = input("\nHow many pages do you want to scrap? ")
    clear_with_msg()
    pages = int(pages)

    return pages

def wait():
    time.sleep(waiting)

main()
