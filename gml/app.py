from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import os

website = 'https://www2.tirexo.com/films-bluray-hd-1080/'
waiting_time = 25

def run():
    print("Here we go!!")
    browser = webdriver.Firefox()
    browser.get(website)
    browser.implicitly_wait(waiting_time)
    print("Getting links...\n\n")
    movies = browser.find_elements_by_xpath('//*[@id="dle-content"]/div[1]')
    movies_links = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/a[2]')
    
    # TODO: Récupérer les links à part parce les élements sont liées à la page
    for i in movies_links:
        browser.get(i.get_attribute("href"))
        browser.implicitly_wait(waiting_time)

    browser.quit()
