from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv

site = 'https://www2.zone-warez.com/films-bluray-hd-1080/'
hdr = {'User-Agent': 'Mozilla/5.0'}

def run():
    print("Here we go!!")
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    print(soup)
