#!/usr/bin/env python3

# TODO: Ask if user want to download it on the NAS
# TODO: Ask user to coose UpToBox or 1fichier or both
# TODO: Add random joke for bypassing protection

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
import random

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
jokes = cfg.JOKES

NUMBER_LINKS = 0
NUMBER_LINKS_HOST = 0
HOST = ""

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
    website = ""

    # Starting animation
    start_animation()

    # Getting useful data
    website = choose_category()
    website = choose_language(website)
    choose_host()
    pages = choose_pages()

    try:

        print("Here we go!!")

        # Getting pages's links of movies
        movies_links = getting_links(website, pages)

        # Getting informations of each movie
        movies = getting_informations(movies_links)

        # Getting dowload links
        links = getting_download_links(movies)

        # Saving the informations in txt file
        save_movies(links)

        print_erase("Job done!")

    except NoSuchWindowException as e:
        print_newline('No GUI on system :(')

    finally:
        print_newline("Sayonara my friend :D\n")
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
    number_of_links = pages * 28
    while(current_page <= pages):
        u = 1
        # Getting url with page
        if (current_page == 1):
            current_url = website
        else:
            current_url = website + "page/" + str(current_page) + "/"
        # Getting pages's links of movies
        browser.get(current_url)
        browser.implicitly_wait(waiting_time)
        print_erase("[" + str(u) + "/" + str(number_of_links) + "] Getting links page")
        movies_urls_dom = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/a[2]')
        for m in movies_urls_dom:
            print_erase("[" + str(u) + "/" + str(number_of_links) + "] Getting links page ...")
            movies_urls.append(m.get_attribute("href"))
            u = u + 1
        current_page = current_page + 1
    return movies_urls

def getting_informations(movies_links):
    movies = []
    u = 1
    global NUMBER_LINKS
    global HOST
    print_erase("Getting informations of each movie...")
    for m in movies_links:
        try:
            wait()
            movie = []
            browser.get(m)
            elements_text = [
                ("Title", '/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/h2/b'),
                ("Quality", '/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[1]/span[1]'),
                ("Language", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div/div[1]/span[2]')
            ]
            elements_href = [
                ("Link", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div[1]/div[3]/div/table/tbody/tr/td[1]/a[1]'),
                ("Date", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div[1]/div[3]/div/table/tbody/tr/td[4]'),
                ("Size", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div[1]/div[3]/div/table/tbody/tr/td[3]')
            ]
            for key,value in elements_text:
                movie.append((key, browser.find_element_by_xpath(value).text))
            for e in elements_href:
                for a in browser.find_elements_by_xpath(e[1]):
                    if (e[0] == "Link"):
                        NUMBER_LINKS = NUMBER_LINKS + 1
                        lk = a.get_attribute("href")
                        movie.append(("Link", lk))
                    #elif (e[0] == "Date"):
                        #movie.append(("Date", a.text))
                    #elif (e[0] == "Size"):
                        #movie.append(("Date", a.text))
            movies.append(movie)
            print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Getting: " + movie[0][1])
        except WebDriverException as e:
            print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Error: WebDriverException : " + format(e))
        except NoSuchElementException as e:
            print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Error: element not found : " + format(e))
        finally:
            u = u + 1

    return movies

def getting_download_links(movies):
    print_erase("Getting download links")
    u = 1
    links = []
    global NUMBER_LINKS
    global NUMBER_LINKS_HOST
    global HOST
    for movie in movies:
        try:
            for key,value in movie:
                if (isinstance(value, str)):
                    if ("http" in value):
                        u = u + 1
                        link_bypassed = bypass_protection(value)
                        if ((HOST == "UpToBox") and ("uptobox" in link_bypassed)):
                            links.append((key, link_bypassed))
                            NUMBER_LINKS_HOST = NUMBER_LINKS_HOST + 1
                        elif ((HOST == "1fichier") and ("1fichier" in link_bypassed)):
                            links.append((key, link_bypassed))
                            NUMBER_LINKS_HOST = NUMBER_LINKS_HOST + 1
                        else:
                            links.append((key, link_bypassed))
                            NUMBER_LINKS_HOST = NUMBER_LINKS_HOST + 1
                    else:
                        links.append((key, value))
            print_erase("[" + str(u) + "/" + str(NUMBER_LINKS) + "] Bypassing url protection... " + random.choice(jokes))
        except WebDriverException as e:
            print_erase("[" + str(u) + "/" + str(NUMBER_LINKS) + "] Skipping ...")

    clear_with_msg()
    print_erase("My lord, here is a summary!")
    print_newline('Movies scrapped: ' + str(len(movies)))
    print_newline('Links scrapped according to your requests: ' + str(NUMBER_LINKS_HOST))
    return links

def bypass_protection(link):
    wait()
    browser.get(link)
    browser.implicitly_wait(waiting_time)
    browser.find_element_by_xpath('/html/body/center/div/div[2]/div/center/form/input').click()
    download_link = browser.find_element_by_xpath('/html/body/center/div/div[2]/div/div[1]/a').get_attribute("href")
    return download_link

def save_movies(links):
    timestamp = int(time.time())
    file_name = "data/" + str(timestamp) + ".txt"
    file = open(file_name, "w")
    u = 0
    print_newline("")
    for key,value in links:
        u = u + 1
        if (key == "Title"):
            file.write("\n")
        file.write(key + ": " + value + "\n")
        print_erase("[" + str(u) + "/" + str(len(links)) + "] Saving ...")
    file.close()
    print_erase_persistent("Saved links on: " + file_name)

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

def choose_host():
    global HOST
    available_choice = [1, 2, 3]
    isOK = False
    while (not isOK):
        host_choice = input("\nChoose a host\n1. UpToBox\n2. 1fichier\n3. ALL\nChoice? ")
        host_choice = int(host_choice)
        if (host_choice in available_choice):
            isOK = True
            clear_with_msg()
            if (host_choice == 1):
                HOST = "UpToBox"
            elif (host_choice == 2):
                HOST = "1fichier"
            elif (host_choice == 3):
                HOST = "All"
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
