#!/usr/bin/env python3

# TODO: Ask if user want to download it on the NAS
# TODO: Ask user to coose UpToBox or 1fichier or both
# TODO: Add random joke for bypassing protection
# TODO: CFG for elements dom
# TODO: Max links per movie with break
# TODO: Show progression for scrapping

from settings import auto_config as cfg
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, NoSuchElementException, SessionNotCreatedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os, sys, re, csv, time
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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

# Choices
movies_qualities_list = cfg.QUALITIES
movies_languages_list = cfg.LANGUAGES
movies_host_list = cfg.HOSTS

# SteelSheet
ssComboBox = cfg.COMBOBOX
ssStart = cfg.BTN_START
ssQuit = cfg.BTN_QUIT
ssDesc = cfg.LBL_DESC
ssTitle = cfg.LBL_TITLE
ssLine = cfg.LINE
ssPages = cfg.LBL_PAGES

NUMBER_LINKS = 0
NUMBER_LINKS_HOST = 0
HOST = ""


class Master(QObject):
    initialization = pyqtSignal()
    scrapping = pyqtSignal(str, int, str)
    start = pyqtSignal()
    sayonara = pyqtSignal()

class Application(QWidget):

    def __init__(self):
        super(Application, self).__init__()
        self.init_app()
        self.init_scrapper()
        self.master.start.emit()

    def init_app(self):

        # Main window
        self.setFixedSize(640, 480)
        self.setWindowTitle(header)
        self.setStyleSheet("background-color: black;")

        self.title_label = QLabel("Give Me Links")
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(ssTitle)

        self.movies_qualities = QComboBox(self)
        self.movies_qualities.setGeometry(50, 50, 400, 35)
        self.movies_qualities.setStyleSheet(ssComboBox)
        for text,url in movies_qualities_list:
            self.movies_qualities.addItem(text)

        self.movies_languages = QComboBox(self)
        self.movies_languages.setGeometry(50, 50, 400, 35)
        self.movies_languages.setStyleSheet(ssComboBox)
        for text,url in movies_languages_list:
            self.movies_languages.addItem(text)

        self.movies_host = QComboBox(self)
        self.movies_host.setGeometry(50, 50, 400, 35)
        self.movies_host.setStyleSheet(ssComboBox)
        self.movies_host.addItems(movies_host_list)

        self.movies_pages = QLineEdit()
        self.movies_pages.setValidator(QIntValidator(0, 10))
        self.movies_pages.setMaxLength(2)
        self.movies_pages.setAlignment(Qt.AlignCenter)
        self.movies_pages.setStyleSheet(ssLine)

        self.movies_pages_label = QLabel("Page(s)")
        self.movies_pages_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movies_pages_label.setAlignment(Qt.AlignCenter)
        self.movies_pages_label.setStyleSheet(ssPages)

        self.description_label = QLabel()
        self.description_label.setWordWrap(True);
        self.description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setStyleSheet(ssDesc)

        self.horizontalGroupBox = QGroupBox()
        self.layout = QHBoxLayout()

        self.vGroupBox = QGroupBox()
        self.descGroupBox = QGroupBox()

        self.layout2 = QVBoxLayout()
        self.layout3 = QHBoxLayout()

        self.layout2.addWidget(self.title_label)
        self.layout2.addWidget(self.movies_qualities)
        self.layout2.addWidget(self.movies_languages)
        self.layout2.addWidget(self.movies_host)
        self.layout2.addWidget(self.movies_pages_label)
        self.layout2.addWidget(self.movies_pages)

        self.bt_start = QPushButton("Start !")
        self.bt_start.setStyleSheet(ssStart)
        self.bt_start.setFixedHeight(60)
        self.bt_start.clicked.connect(self.start_scrapping)
        self.layout.addWidget(self.bt_start, 2)

        self.bt_quit = QPushButton("Quit")
        self.bt_quit.setStyleSheet(ssQuit)
        self.bt_quit.setFixedHeight(60)
        self.bt_quit.clicked.connect(self.sayonara)
        self.layout.addWidget(self.bt_quit)

        self.layout3.addWidget(self.description_label)

        self.horizontalGroupBox.setLayout(self.layout)
        self.vGroupBox.setLayout(self.layout2)
        self.descGroupBox.setLayout(self.layout3)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.vGroupBox)
        self.mainLayout.addWidget(self.descGroupBox)
        self.mainLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.mainLayout)

        self.show()

    def change_title(self, text):
        self.title_label.setText(text)

    def change_description(self, text):
        self.description_label.setText(text)

    def sayonara(self):
        self.close()
        self.thread.quit()

    def start_scrapping(self):
        self.bt_quit.setEnabled(False)
        self.master.scrapping.emit("https://www2.tirexo.org/films-bluray-hd-1080/", 1, "UpToBox")

    def init_scrapper(self):

        self.thread = QThread()
        self.thread.start()

        self.worker = Scrapper()
        self.worker.moveToThread(self.thread)
        self.worker.start.connect(self.worker.start_animation)
        self.worker.title.connect(self.change_title)
        self.worker.description.connect(self.change_description)
        self.worker.start.connect(self.worker.start_animation)

        self.master = Master()
        self.master.start.connect(self.worker.start)
        self.master.initialization.connect(self.worker.init_webdriver)
        self.master.scrapping.connect(self.worker.scrapping)

        # Init browser
        self.master.initialization.emit()


class Scrapper(QObject):

    # Sinals
    start = pyqtSignal()
    title = pyqtSignal(str)
    description = pyqtSignal(str)

    # Variables
    browser = None

    # Starting browser
    def init_webdriver(self):
        self.description.emit("Initialization of browser")
        try:
            self.options = Options()
            self.options.add_argument('--headless')
            self.browser = webdriver.Firefox(options=self.options)
            self.description.emit("Ready for scrapping")
        except NoSuchWindowException as e:
            print_newline('No GUI on system :(')
        except SessionNotCreatedException as e:
            print_newline('Error when creating instance of webdrier :(')
            self.description.emit("Error when creating instance of webdrier :(")

    # Start scrapping links
    def scrapping(self, website, pages, host):

        # Variables
        u = 0
        movies_links = []
        movies = []
        links = []

        try:

            print("Here we go!!")
            self.description.emit("Here we go ...")

            # Getting pages's links of movies
            movies_links = self.getting_links(website, pages)

            # Getting informations of each movie
            movies = self.getting_informations(movies_links)

            # Getting dowload links
            links = self.getting_download_links(movies, host)

            # Saving the informations in txt file
            self.save_movies(links)

            print_erase("Job done!")
            self.description.emit("Job done :)")

        except NoSuchWindowException as e:
            print_newline('No GUI on system :(')

        finally:
            print_newline("Sayonara my friend :D\n")
            self.browser.quit()

    def start_animation(self):
        clear()
        animation = "|/-\\"
        for i in range(50):
            time.sleep(0.1)
            sys.stdout.write("\r[" + animation[i % len(animation)] + "] ")
            sys.stdout.write(header)
            sys.stdout.flush()
        clear_with_msg()

    def getting_links(self, website, pages):
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
            self.browser.get(current_url)
            print_newline('URL: ' + current_url)
            time.sleep(5)
            self.browser.implicitly_wait(waiting_time)
            print_erase("[" + str(u) + "/" + str(number_of_links) + "] Getting links page")
            self.description.emit("[" + str(u) + "/" + str(number_of_links) + "] Getting links page")
            movies_urls_dom = self.browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/a[2]')
            print_newline('MDOM: ' + str(len(movies_urls_dom)))
            time.sleep(5)
            for m in movies_urls_dom:
                print_erase("[" + str(u) + "/" + str(number_of_links) + "] Getting links page ...")
                self.description.emit("[" + str(u) + "/" + str(number_of_links) + "] Getting links page ...")
                movies_urls.append(m.get_attribute("href"))
                u = u + 1
            current_page = current_page + 1
        return movies_urls

    def getting_informations(self, movies_links):
        movies = []
        u = 1
        global NUMBER_LINKS
        print_erase("Getting informations of each movie...")
        self.description.emit("Getting informations of each movie...")
        for m in movies_links:
            try:
                wait()
                movie = []
                self.browser.get(m)
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
                    movie.append((key, self.browser.find_element_by_xpath(value).text))
                for e in elements_href:
                    for a in self.browser.find_elements_by_xpath(e[1]):
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
                self.description.emit("[" + str(u) + "/" + str(len(movies_links)) + "] Getting: " + movie[0][1])
            except WebDriverException as e:
                print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Error: WebDriverException : " + format(e))
            except NoSuchElementException as e:
                print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Error: element not found : " + format(e))
            finally:
                u = u + 1

        return movies

    def getting_download_links(self, movies, host):
        print_erase("Getting download links")
        u = 1
        links = []
        global NUMBER_LINKS
        global NUMBER_LINKS_HOST
        for movie in movies:
            try:
                for key,value in movie:
                    if (isinstance(value, str)):
                        if ("http" in value):
                            u = u + 1
                            link_bypassed = self.bypass_protection(value)
                            if ((host == "UpToBox") and ("uptobox" in link_bypassed)):
                                links.append((key, link_bypassed))
                                NUMBER_LINKS_HOST = NUMBER_LINKS_HOST + 1
                            elif ((host == "1fichier") and ("1fichier" in link_bypassed)):
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

    def bypass_protection(self, link):
        wait()
        self.browser.get(link)
        self.browser.implicitly_wait(waiting_time)
        self.browser.find_element_by_xpath('/html/body/center/div/div[2]/div/center/form/input').click()
        download_link = self.browser.find_element_by_xpath('/html/body/center/div/div[2]/div/div[1]/a').get_attribute("href")
        return download_link

    def save_movies(self, links):
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

def run():
    # PyQt5
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())

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

def wait():
    time.sleep(waiting)
