#!/usr/bin/env python3
"""A scrapper created by Maher LAAROUSSI."""

# TODO: Ask if user want to download it on the NAS
# TODO: Max links (Only 1 if there are a lot for example) per movie with break

from gml.settings import auto_config as cfg
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.firefox.options import Options
import os
import sys
import time
import random
from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtWidgets import QComboBox, QLineEdit, QApplication, \
                            QGroupBox, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt

# CFG
header = cfg.HEADER
options = cfg.OPTIONS
url = cfg.URL
url_movies_all = cfg.URL_MOVIES_ALL
waiting_time = cfg.WAITING_TIME
waiting = cfg.WAITING
os_now = cfg.OS_NOW
jokes = cfg.JOKES

# Choices
movies_host_list = cfg.HOSTS
movies_qualities_dom = cfg.MOVIES_QUALITIES
movies_qualities_select = cfg.MOVIES_QUALITY_SELECT
movies_languages_dom = cfg.MOVIES_LANGUAGES

# DOM
element_movies_pages = cfg.MOVIES_PAGES
element_movies_pages_bis = cfg.MOVIES_PAGES_BIS
elements_text = cfg.MOVIES_INFO
elements_href = cfg.MOVIES_INFO_HREF
element_protection_click = cfg.PROTECTION_CLICK
element_protection_link = cfg.PROTECTION_LINK
element_check = cfg.CHECK_ALIVE

# SteelSheet
ssComboBox = cfg.COMBOBOX
ssStart = cfg.BTN_START
ssQuit = cfg.BTN_QUIT
ssDesc = cfg.LBL_DESC
ssTitle = cfg.LBL_TITLE
ssLine = cfg.LINE
ssPages = cfg.LBL_PAGES

# Global
NUMBER_LINKS = 0
NUMBER_LINKS_HOST = 0


class Master(QObject):
    """Manage the thread."""

    initialization = pyqtSignal()
    initialization_choices = pyqtSignal()
    scrapping = pyqtSignal(str, int, str, str, str)
    start = pyqtSignal()
    sayonara = pyqtSignal()
    check = pyqtSignal()
    quit = pyqtSignal()
    show_scrapping_by_name_mode = pyqtSignal()
    show_scrapping_randomly_mode = pyqtSignal()
    show_initialization_mode = pyqtSignal()


class Application(QWidget):
    """The GUI Application."""

    def __init__(self):
        """Initialize the application."""
        super(Application, self).__init__()
        self.init_app()
        self.init_stuffs()

    def init_app(self):
        """Initialize the elements of GUI."""
        # Main window
        # self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setFixedSize(640, 600)
        self.setWindowTitle(header)
        self.setStyleSheet("background-color: black;")

        self.king_label = QLabel("A king is below me!")
        self.king_label \
            .setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.king_label.setAlignment(Qt.AlignCenter)
        self.king_label.setStyleSheet(ssDesc)

        self.label_image = QLabel(self)
        self.init_image = QPixmap("gml/resources/maher.png")
        self.label_image.setPixmap(self.init_image.scaled(200, 200, Qt.KeepAspectRatio))
        self.label_image.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Give Me Links")
        self.title_label \
            .setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(ssTitle)

        self.movies_qualities = QComboBox(self)
        self.movies_qualities.setGeometry(50, 50, 400, 35)
        self.movies_qualities.setStyleSheet(ssComboBox)
        self.movies_qualities.addItem("Tous")

        self.movies_languages = QComboBox(self)
        self.movies_languages.setGeometry(50, 50, 400, 35)
        self.movies_languages.setStyleSheet(ssComboBox)

        self.movies_host = QComboBox(self)
        self.movies_host.setGeometry(50, 50, 400, 35)
        self.movies_host.setStyleSheet(ssComboBox)
        self.movies_host.addItems(movies_host_list)

        self.movies_pages = QLineEdit()
        self.movies_pages.setValidator(QIntValidator(0, 10))
        self.movies_pages.setMaxLength(2)
        self.movies_pages.setAlignment(Qt.AlignCenter)
        self.movies_pages.setStyleSheet(ssLine)
        self.movies_pages.setText("1")
        self.movies_pages.setPlaceholderText("1")

        self.movies_pages_label = QLabel("Page(s)")
        self.movies_pages_label \
            .setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movies_pages_label.setAlignment(Qt.AlignCenter)
        self.movies_pages_label.setStyleSheet(ssPages)

        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label \
            .setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setStyleSheet(ssDesc)

        self.horizontalGroupBox = QGroupBox()
        self.layout = QHBoxLayout()

        self.vGroupBox = QGroupBox()
        self.descGroupBox = QGroupBox()

        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

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

        self.layout3.addWidget(self.king_label)
        self.layout3.addWidget(self.label_image)
        self.layout3.addWidget(self.description_label)

        self.horizontalGroupBox.setLayout(self.layout)
        self.vGroupBox.setLayout(self.layout2)
        self.descGroupBox.setLayout(self.layout3)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.vGroupBox)
        self.mainLayout.addWidget(self.descGroupBox)
        self.mainLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.mainLayout)

        self.bt_start.setEnabled(False)

        self.show()

    def show_initialization_mode(self):
        """Show the initialization interface."""
        self.hide_all_mode()
        self.king_label.show()
        self.label_image.show()
        self.descGroupBox.show()

    def show_scrapping_randomly_mode(self):
        """Show the first choice."""
        self.hide_all_mode()
        self.label_image.hide()
        self.king_label.hide()
        self.vGroupBox.show()
        self.descGroupBox.show()
        self.horizontalGroupBox.show()

    def show_scrapping_by_name_mode(self):
        """Show te second choice."""

    def hide_all_mode(self):
        """Hide all elements of th application."""
        self.vGroupBox.hide()
        self.horizontalGroupBox.hide()
        self.descGroupBox.hide()
        self.king_label.hide()
        self.label_image.hide()

    def change_title(self, text):
        """Change text of label title."""
        self.title_label.setText(text)

    def change_description(self, text):
        """Change text of label description."""
        self.description_label.setText(text)

    def enable_qualities(self, bool):
        """Change status of combobox qualities."""
        self.movies_qualities.setEnabled(bool)

    def enable_languages(self, bool):
        """Change status of combobox languages."""
        self.movies_languages.setEnabled(bool)

    def enable_hosts(self, bool):
        """Change status of combobox hosts."""
        self.movies_host.setEnabled(bool)

    def enable_pages(self, bool):
        """Change status of combobox hosts."""
        self.movies_pages.setEnabled(bool)

    def enable_bt_quit(self, bool):
        """Enable of disable button quit."""
        self.bt_start.setEnabled(bool)

    def load_qualities(self, list):
        """Load qualities in the combobox."""
        list.sort(key = lambda x: x[0])
        for item, value in list:
            if (item != "Tous"):
                self.movies_qualities.addItem(item)

    def load_languages(self, list):
        """Load languages in the combobox."""
        list.sort(key = lambda x: x[0])
        self.movies_languages.addItem("Tous")
        for item, value in list:
            if (item != "Tous"):
                self.movies_languages.addItem(item)

    def sayonara(self):
        """Quit the application."""
        self.close()
        self.master.quit.emit()
        self.thread.quit()

    def start_scrapping(self):
        """Start scrapping links from website."""
        website = url + url_movies_all
        pagesOk = False

        # Pages
        try:
            pages = int(self.movies_pages.text())
            if (pages > 20 or pages < 1):
                msg = "Pages is too high and you fuckin' know it!"
                self.change_description(msg)
            else:
                pagesOk = True
        except ValueError:
            msg = "A fucking error occured with number of pages!!"
            self.change_description(msg)

        if (pagesOk):
            # Get values of comboboxs
            host = str(self.movies_host.currentText())
            language = str(self.movies_languages.currentText())
            quality = str(self.movies_qualities.currentText())

            # Start scrapping
            self.master.scrapping.emit(website, pages, host, quality, language)

    def init_stuffs(self):
        """Initialize thread, master and worker."""

        self.show_initialization_mode()

        self.thread = QThread()
        self.thread.start()

        self.worker = Scrapper()
        self.worker.moveToThread(self.thread)
        self.worker.start.connect(self.worker.start_animation)
        self.worker.title.connect(self.change_title)
        self.worker.description.connect(self.change_description)
        self.worker.bt_start.connect(self.enable_bt_quit)
        self.worker.load_qualities.connect(self.load_qualities)
        self.worker.load_languages.connect(self.load_languages)
        self.worker.show_scrapping_randomly_mode.connect(self.show_scrapping_randomly_mode)
        self.worker.c_qualities.connect(self.enable_qualities)
        self.worker.c_languages.connect(self.enable_languages)
        self.worker.c_hosts.connect(self.enable_hosts)
        self.worker.le_pages.connect(self.enable_pages)

        self.master = Master()
        self.master.start.connect(self.worker.start)
        self.master.initialization.connect(self.worker.init_all)
        self.master.initialization_choices.connect(self.worker.init_choices)
        self.master.scrapping.connect(self.worker.scrapping)
        self.master.check.connect(self.worker.check_website)
        self.master.quit.connect(self.worker.quit_webdriver)
        self.master.show_scrapping_by_name_mode.connect(self.show_scrapping_by_name_mode)
        self.master.show_scrapping_randomly_mode.connect(self.worker.show_scrapping_randomly_mode)
        self.master.show_initialization_mode.connect(self.show_initialization_mode)

        # Init things
        self.master.initialization.emit()
        self.bt_start.setEnabled(True)


class Scrapper(QObject):
    """The only scrapper which can do anything."""

    # Sinals
    start = pyqtSignal()
    title = pyqtSignal(str)
    c_qualities = pyqtSignal(bool)
    c_languages = pyqtSignal(bool)
    c_hosts = pyqtSignal(bool)
    le_pages = pyqtSignal(bool)
    description = pyqtSignal(str)
    bt_start = pyqtSignal(bool)
    load_qualities = pyqtSignal(list)
    load_languages = pyqtSignal(list)

    # Not used by now
    show_scrapping_randomly_mode = pyqtSignal()
    show_scrapping_by_name_mode = pyqtSignal()
    show_initialization_mode = pyqtSignal()

    # Variables
    browser = None
    summary = []
    t_qualities = []
    t_languages = []

    def init_all(self):
        self.init_webdriver()
        self.init_choices()
        self.show_scrapping_randomly_mode.emit()
        self.start_animation()

    def quit_webdriver(self):
        """Close the browser properly."""
        self.browser.quit()

    # Starting browser
    def init_webdriver(self):
        """Initialize the browser."""
        self.description.emit("Initialization of browser")
        try:
            self.opt = Options()
            self.opt.add_argument(options)
            self.browser = webdriver.Firefox(options=self.opt)
            self.description.emit("Ready for scrapping")
        except NoSuchWindowException:
            print_newline('No GUI on system :(')
        except SessionNotCreatedException:
            print_newline('Error when creating instance of webdrier :(')
            self.description \
                .emit("Error when creating instance of webdrier :(")

    # Check if the website is alive or not
    def check_website(self):
        """Check if the website is not down."""
        alive = False
        website = url + url_movies_all
        self.description.emit("Checking if the website is alive ...")
        self.browser.get(website)
        self.browser.implicitly_wait(waiting_time)

        # 503 or not?
        try:
            error_check_dom = self.browser.find_element_by_xpath(element_check)
            if (error_check_dom.size != 0):
                alive = True
        except NoSuchElementException:
            alive = False

        if (not alive):
            self.description.emit("The website is down my friend :(")
            self.start.emit(False)
            self.quit.emit(False)

        return alive

    # Scrapping qualities and languages
    def init_choices(self):
        """Get all qualities and languages available from website."""
        if (self.check_website()):

            website = url + url_movies_all
            self.description.emit("Initialization qualities and languages ...")
            self.browser.get(website)
            self.browser.implicitly_wait(waiting_time)

            # Qualities
            qualities_dom = self.browser \
                                .find_elements_by_xpath(movies_qualities_dom)
            for q in qualities_dom:
                self.t_qualities.append((q.text, q.get_attribute("value")))
            self.load_qualities.emit(self.t_qualities)
            self.t_qualities.append(("Tous", url_movies_all))

            # Languages
            languages_dom = self.browser \
                                .find_elements_by_xpath(movies_languages_dom)
            for lang in languages_dom:
                self.t_languages.append((lang.text, lang.get_attribute("value")))
            self.load_languages.emit(self.t_languages)

            msg = "Initialization complete and i'm fucking ready !"
            self.description.emit(msg)
            self.bt_start.emit(True)
        else:
            pass

    # BUG:  Fix the error when trying to do another scrapping.
    #       selenium.common.exceptions.InvalidSessionIdException: Message:
    #       Tried to run command without establishing a connection
    # Start scrapping links
    def scrapping(self, website, pages, host, quality, language):
        """Get links from the website."""

        summary = []

        if (self.check_website()):

            self.enable_choices(False)

            # Variables
            movies_links = []
            movies = []
            links = []
            resume = ""
            msg = ""

            try:

                msg = "Here we go!!"
                print_erase(msg)
                self.description.emit(msg)

                # Getting pages's links of movies
                movies_links = self \
                    .getting_links(website, pages, quality, language)

                # Getting informations of each movie
                movies = self.getting_informations(movies_links)

                # Getting dowload links
                links = self.getting_download_links(movies, host)

                # Saving the informations in txt file
                self.save_movies(links)

                print_newline("Job done!")

                for e in self.summary:
                    resume = resume + e + "\n"

                self.description.emit(resume)
                self.enable_choices(True)

            except NoSuchWindowException:
                print_newline('No GUI on system :(')
                self.enable_choices(True)

            finally:
                self.enable_choices(True)
        else:
            pass

    def enable_choices(self, bool):
        self.c_qualities.emit(bool)
        self.c_languages.emit(bool)
        self.c_hosts.emit(bool)
        self.le_pages.emit(bool)
        self.bt_start.emit(bool)

    def start_animation(self):
        """Show an animation in the cmd."""
        clear()
        animation = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r[" + animation[i % len(animation)] + "] ")
            sys.stdout.write(header)
            sys.stdout.flush()
        clear_with_msg()

    def getting_links(self, website, pages, quality, language):
        """Get the url's pages of movies."""
        current_page = 1
        movies_urls = []
        pages = int(pages)
        number_of_links = pages * 28
        u = 1

        self.description.emit("Getting the right link ...")
        self.browser.get(website)
        self.browser.implicitly_wait(waiting_time)

        for text, value in self.t_qualities:
            if (text == quality):
                if (text == "Tous"):
                    url_quality = ""
                else:
                    url_quality = value

        for text, value in self.t_languages:
            if (text == language):
                if (text == "Tous"):
                    url_language = ""
                else:
                    url_language = value.replace(url_movies_all, "")[1:]

        new_url = url + url_movies_all + url_quality + url_language

        msg = "Getting the " + str(number_of_links) + " links of the page(s) ..."
        self.description.emit(msg)

        while(current_page <= pages):
            # Getting url with page
            if (current_page == 1):
                current_url = new_url
            else:
                current_url = new_url + "page/" + str(current_page) + "/"
            # Getting pages's links of movies
            self.browser.get(current_url)
            self.browser.implicitly_wait(waiting_time)
            movies_urls_dom = self.browser \
                .find_elements_by_xpath(element_movies_pages_bis)
            if (len(movies_urls_dom) == 0):
                movies_urls_dom = self.browser \
                    .find_elements_by_xpath(element_movies_pages)
            for m in movies_urls_dom:
                movies_urls.append(m.get_attribute("href"))
                u = u + 1
            current_page = current_page + 1
        return movies_urls

    def getting_informations(self, movies_links):
        """Get all informtions about movies scrapped."""
        movies = []
        u = 1
        global NUMBER_LINKS
        NUMBER_LINKS = 0
        self.description.emit("Getting informations of each movie...")
        for m in movies_links:
            try:
                wait()
                movie = []
                self.browser.get(m)
                for key, value in elements_text:
                    movie \
                        .append((
                                key,
                                self.browser.find_element_by_xpath(value).text
                                ))
                for e in elements_href:
                    # FIXME: Change the xpath for getting links
                    # NOTE: The xpath changed totally and the href too
                    for a in self.browser.find_elements_by_xpath(e[1]):
                        if (e[0] == "Link"):
                            NUMBER_LINKS = NUMBER_LINKS + 1
                            lk = a.get_attribute("href")
                            movie.append(("Link", lk))
                movies.append(movie)
                msg = "[" + str(u) + "/" + str(len(movies_links)) + "]\nGetting: " + movie[0][1]
                self.description.emit(msg)
            except WebDriverException as e:
                print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Error: WebDriverException : " + format(e))
            except NoSuchElementException as e:
                print_erase("[" + str(u) + "/" + str(len(movies_links)) + "] Error: element not found : " + format(e))
            finally:
                u = u + 1

        return movies

    def getting_download_links(self, movies, host):
        """Get the protected links."""
        self.description.emit("Getting download links")
        u = 1
        links = []
        joke = "\n" + random.choice(jokes)
        global NUMBER_LINKS
        global NUMBER_LINKS_HOST
        NUMBER_LINKS_HOST = 0
        for movie in movies:
            try:
                for key, value in movie:
                    if (isinstance(value, str)):
                        # Random jokes
                        if (not (u % 10)):
                            joke = "\n" + random.choice(jokes)
                        # Save links with specific host
                        if ("http" in value):
                            u = u + 1
                            link_bypassed = self.bypass_protection(value)
                            if (host.lower() in link_bypassed):
                                links.append((key, link_bypassed))
                                NUMBER_LINKS_HOST = NUMBER_LINKS_HOST + 1
                            elif (host.lower() == "tous"):
                                links.append((key, link_bypassed))
                                NUMBER_LINKS_HOST = NUMBER_LINKS_HOST + 1
                            else:
                                pass
                        else:
                            links.append((key, value))
                msg = "[" + str(u) + "/" + str(NUMBER_LINKS) + "]\nBypassing url protection..." + joke
                self.description.emit(msg)
            except WebDriverException:
                print_erase("[" + str(u) + "/" + str(NUMBER_LINKS) + "] Skipping ...")

        # FIXME: Showing this message twice if we ran the scrapping twice
        self.summary.append("My lord,my lord!! Here is a summary just for you :)\nMovies: " + str(len(movies)) + " | Links: " + str(NUMBER_LINKS_HOST))
        self.description.emit(self.summary[len(self.summary) - 1])

        return links

    def bypass_protection(self, link):
        """Bypass protection to get download links."""
        wait()
        self.browser.get(link)
        self.browser.implicitly_wait(waiting_time)
        self.browser.find_element_by_xpath(element_protection_click).click()
        download_link = self \
            .browser \
            .find_element_by_xpath(element_protection_link) \
            .get_attribute("href")
        return download_link

    def save_movies(self, links):
        """Save all informations about each movie on a txt file."""
        timestamp = int(time.time())
        file_name = "gml/data/" + str(timestamp) + ".txt"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        file = open(file_name, "w")
        for key, value in links:
            if (key == "Title"):
                file.write("\n")
            file.write(key + ": " + value + "\n")
        file.close()
        self.summary.append("Saved links on: " + file_name)


def print_erase(str):
    """Print a text with erasing the line."""
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write(str)
    sys.stdout.flush()


def print_erase_persistent(str):
    """Print a text with erasing the line and new line."""
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write(str)
    sys.stdout.write("\n")
    sys.stdout.flush()


def clear():
    """Clear the cmd."""
    if (os_now == "Linux"):
        os.system('clear')
    else:
        os.system('cls')


def clear_with_msg():
    """Clear the cmd and show the header message."""
    if (os_now == "Linux"):
        os.system('clear')
    else:
        os.system('cls')
    print("[+] " + header)


def print_newline(str):
    """Print message in a new line."""
    sys.stdout.write('\n')
    sys.stdout.write(str)
    sys.stdout.flush()


def wait():
    """Sleep some seconds."""
    time.sleep(waiting)


def run():
    """Run the PyQt5 application."""
    # PyQt5
    app = QApplication(sys.argv)
    window = Application()
    window = window  # To avoid warning with PEP8
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
