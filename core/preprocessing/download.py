# System modules
import re
import time as timer
from urllib.error import HTTPError
import urllib.request
from enum import Enum
from shutil import rmtree
from os import getenv, mkdir, path
from multiprocessing.pool import ThreadPool

# External modules
import fitz  # PyMuPDF module
from Bio import Entrez
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Pubpeer constants
PUBPEER_BASE_URL = 'https://www.pubpeer.com/search?q='
PUBPEER_IMG_PATH = r'Data\Blot data\Pubpeer'
PUBPEER_PUBLICATION_URL = 'https://www.pubpeer.com/publications/'

# Pubmed constants
PUBMED_IMG_PATH = r'Data\Blot data\Pubmed'
PUBMED_TEMP_PDF_PATH = r'Data\Blot data\Pubmed\PDFs'

# Selenium constants
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
CHROMEDRIVER_PATH = fr'{CHROME_PATH[:-11]}\chromedriver.exe'

# Other constants
HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
SECRETS = r'ForgeryDetector\secrets.env'


class DownloadManager():
    def __init__(self, headless=None, threads=None, webbrowser_path=None, driver_path=None):
        if headless is None:
            self.headless = True

        if threads is None:
            self.threads = 8
        else:
            self.threads = threads

        if webbrowser_path is None:
            self.webbrowser = CHROME_PATH
        else:
            self.webbrowser = webbrowser_path

        if driver_path is None:
            self.driver = CHROMEDRIVER_PATH
        else:
            self.driver = driver_path

        self.PubMed = DownloadManager.PubMed(threads=self.threads)
        self.PubPeer = DownloadManager.PubPeer(headless=self.headless, threads=self.threads)

    class PubMed():
        class ArticleType(Enum):
            PMC = 1
            DOI = 2

        def __init__(self, threads):
            # Load environment in order to read the environment variables in the .env file
            load_dotenv(SECRETS)
            Entrez.email = getenv('EntrezMail')
            Entrez.api_key = getenv('EntrezAPI')

            # Loads threads
            self.threads = threads

            # Create some needed folders if they don't already exist
            if not path.exists(PUBMED_TEMP_PDF_PATH):
                mkdir(PUBMED_TEMP_PDF_PATH)

        def get_records(self, db, retmax, datetype, mindate, maxdate, term, usehistory):
            """Gets the URLs of articles given a list of parameters.

            Args:
                db (str): Which database to search in.
                retmax (int): Maximum return value.
                datetype (str): What type of date to use.
                mindate (str): Minimum date.
                maxdate (str): Maximum date.
                term (str): Which term to search for.
                usehistory (str): When usehistory is set to 'y' eSearch
                will post the UIDs resulting from the search operation
                onto the History server so that they can be used directly
                in a subsequent E-utility call.

            Returns:
                records (Custom Dictionary tree): Returns the found records and
                the accompanying information.
                count (int): Returns the amount of records found.
            """
            # Send query and return found articles as dictionary
            result = Entrez.read(Entrez.esearch(db=db, retmax=retmax, datetype=datetype, mindate=mindate, maxdate=maxdate, term=term, usehistory=usehistory), validate=False)
            count = result["Count"]

            # Fetch the results using the found articles from the previous line
            handle = Entrez.efetch(db=db, rettype="full", retmode="xml", retstart=0, retmax=1, webenv=result["WebEnv"], query_key=result["QueryKey"])

            # Parse the results and get count
            records = Entrez.read(handle, validate=False)
            return records, count

        def get_links(self, db, retmax, datetype, mindate, maxdate, term, usehistory):
            """Gets the URLs of articles given a list of parameters.

            Args:
                db (str): Which database to search in.
                retmax (int): Maximum return value.
                datetype (str): What type of date to use.
                mindate (str): Minimum date.
                maxdate (str): Maximum date.
                term (str): Which term to search for.
                usehistory (str): When usehistory is set to 'y' eSearch
                will post the UIDs resulting from the search operation
                onto the History server so that they can be used directly
                in a subsequent E-utility call.

            Returns:
                tuple(list[str], ArticleType): Returns a tuple containing
                a list of article URLs and the type of the articles.
            """
            handle = Entrez.esearch(db=db, retmax=retmax, datetype=datetype, mindate=mindate, maxdate=maxdate, term=term, usehistory=usehistory)
            records = Entrez.read(handle, validate=False)

            # get a list of Pubmed IDs for all articles
            idlist = ','.join(records['IdList'])
            handle = Entrez.efetch("pmc", id=idlist, retmode="xml")
            records = Entrez.read(handle, validate=False)

            pmc_articles = []
            dois = []

            for record in records:
                if record.get('front'):
                    if record['front']['article-meta'].get('article-id'):
                        for article_id in record['front']['article-meta']['article-id']:
                            # Get PMCID link
                            if 'pmc' in article_id.attributes.values():
                                pmc_articles.append((f'http://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/pdf/', str(article_id)))

                            # Get DOI link
                            if 'doi' in article_id.attributes.values():
                                dois.append((f'http://dx.doi.org/{article_id}', str(article_id)))

            return (pmc_articles, self.ArticleType.PMC), (dois, self.ArticleType.DOI)

        def show_articles(self, articles):
            """Print articles.

            Args:
                articles (list[str]): List of article links.
            """
            if isinstance(articles, tuple):
                if articles[1] == self.ArticleType.PMC:
                    for index, article in enumerate(articles[0], start=1):
                        print(f'Paper {index} with ID {article[1]}: {article[0]}')

                if articles[1] == self.ArticleType.DOI:
                    for index, article in enumerate(articles[0], start=1):
                        print(F'Paper {index} with ID {article[1]}: {article[0]}')

        def download(self, articles, path=None, rm=None):
            """Given a list of article URLs, the articles are
            downloaded and the images extracted from said articles.

            Args:
                articles (list[str]): A list of article URLs.
                rm (bool, optional): If True then remove the folder with the downloaded papers. Defaults to None.
            """
            if rm is None:
                rm = True

            if path is None:
                path = PUBMED_TEMP_PDF_PATH

            if isinstance(articles, tuple):
                article_list = articles[0]
            else:
                print(f'Expected type <class \'tuple\'>, but got {type(articles)} instead.')

            pdf_paths = []
            downloads_iterable = []
            for index, (url, article_id) in enumerate(article_list, start=1):
                downloads_iterable.append((url, fr'{path}\Paper_{index}_{article_id}.pdf'))
                pdf_paths.append([fr'{path}\Paper_{index}_{article_id}.pdf'])

            try:
                with ThreadPool(self.threads) as tp:
                    tp.starmap(urllib.request.urlretrieve, downloads_iterable)
            except Exception as e:
                print(f'Exception occurred during urlretrieve: {e}')

            try:
                with ThreadPool(self.threads) as tp:
                    tp.starmap(self.extract_images, pdf_paths)
            except Exception as e:
                print(f'Exception occurred during extract_images: {e}')

            if rm:
                # Remove the folder with the papers since they are not needed anymore
                rmtree(path)

        @staticmethod
        def extract_images(pdf_path, path=None):
            """Extracts images from a PDF given a path.

            Args:
                path (str): Path of the PDF file.
            """
            if path is None:
                path = PUBMED_IMG_PATH

            article_id = pdf_path[-11:-4]

            if path.exists(pdf_path):
                with fitz.open(filename=pdf_path, filetype='pdf') as pdf:
                    xrefs = set()

                    for page_index in range(pdf.pageCount):
                        for image in pdf.get_page_images(page_index):
                            # The XREF unique identifier is added to the set
                            # in order to not have duplicates.
                            xrefs.add(image[0])

                    # A pixmap is an object specific to PyMuPDF (Fitz)
                    # and represents a rectangular square of pixels.
                    pixmaps = [fitz.Pixmap(pdf, xref) for xref in xrefs]

                    for index, pixmap in enumerate(pixmaps, start=1):
                        pixmap.save(fr'{path}\Pubmed_{article_id}_{index}.png')
            else:
                print(f'File not found: {pdf_path}')
                return

    class PubPeer():
        def __init__(self, threads, headless):
            # Check image folder existence
            if not path.exists(PUBPEER_IMG_PATH):
                mkdir(PUBPEER_IMG_PATH)

            # Set options for Selenium
            self.opts = Options()
            self.opts.add_experimental_option('excludeSwitches', ['enable-logging'])  # Disable annoying messages
            self.opts.headless = headless
            self.opts.binary_location = CHROME_PATH

            # Set the location of the webdriver
            self.chrome_driver = CHROMEDRIVER_PATH
            self.driver = webdriver.Chrome(options=self.opts, executable_path=self.chrome_driver)

            # Get threads
            self.threads = threads

        def get_soup(self, term, pages=None):
            """Given a search term, get the HTML code (soups) of
            the result.

            Args:
                term (str): What you want to search for.
                pages (int, optional): How many pages to scroll. Defaults to None.

            Returns:
                list[BeautifulSoup]: List of BeautifulSoup objects containing the HTML code
                of the search.
            """
            if pages is None:
                pages = 1

            if not isinstance(pages, int):
                print(f'Wrong type for parameter \'pages\'. Expected type of arg: <class \'int\'>, Actual type of arg: {type(pages)}')
                return

            term = re.sub(' ', '+', term)
            url = f'{PUBPEER_BASE_URL}{term}'

            # Maximize the window size to ensure scrolling to the bottom works
            self.driver.maximize_window()

            # Get content of website and wait 1 sec so that it can all be loaded
            self.driver.get(url)
            timer.sleep(2)

            # Accept cookie disclaimer
            self.driver.find_element_by_css_selector('body > div.cc-window.cc-floating.cc-type-info.cc-theme'
                                                     '-classic.cc-bottom.cc-right.cc-color-override-1019874493 > '
                                                     'div > a').click()
            timer.sleep(1)

            # Remove footer
            self.driver.find_element_by_css_selector('#page-wrapper > div.extension-installer.container > div > div > span > i').click()
            timer.sleep(1)

            self._scroll_bottom()
            self._click_more_btn(pages)

            # Parse content
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            return soup

        def _soupify(self, articles):
            """Creates a strained soup object that filters through
            all tags and only keeps img tags as these are the only
            ones that are of interest. This is a private function
            only to be used in the context of the download function.

            Args:
                articles (list[str]): List with one article

            Returns:
                list[BeautifulSoup]: List of BeautifulSoup objects
                that only contain img links.
            """
            # Get only img tags
            img_filter = SoupStrainer('img')
            soups = []

            for article in articles:
                # Get content
                self.driver.get(article)
                timer.sleep(1)
                soups.append(BeautifulSoup(self.driver.page_source, "html.parser", parse_only=img_filter))

            return soups

        def download(self, articles):
            """Downloads images from articles given a list of article URLs.

            Args:
                articles (list[str]): List of article URLs.
            """
            soups = self._soupify(articles)
            images = []

            # Get all img tags, extract image links and save to list
            for soup in soups:
                soup_images = soup.findAll('img')

                for image in soup_images:
                    if re.match('https://images.pubpeer.com', image['src']):
                        images.append(image)

            # Create iterable for the starmap function
            downloads_iterable = [(image['src'], fr'{PUBPEER_IMG_PATH}/Pubpeer_{index}.jpg') for index, image in enumerate(images, start=1)]

            # Download the images
            try:
                with ThreadPool(self.threads) as tp:
                    tp.starmap(urllib.request.urlretrieve, downloads_iterable)
            except HTTPError:
                return HTTPError

        def _click_more_btn(self, pages=None):
            """Clicks the "Load more" button on Pubpeer's site.
            This is a private function and is not supposed to
            be used outside the context of the download function.

            Args:
                pages (int, optional): How many pages to load. Defaults to None.
            """
            if pages is None:
                pages = 1

            # The limit is 27 clicks, which gives 280 results.
            # To get around this, you need to contact Pubpeer.
            if pages > 27:
                print('The limit is 27 clicks because Pubpeer only allows 280 results for public searches.')
                return
            elif pages <= 0:
                print('n can not be 0 or below.')
                return

            for page_num in range(0, pages):
                self._scroll_bottom()

                # Wait a little bit to allow the site to load
                timer.sleep(1)

                # For some reason I need to scroll to the bottom twice
                # because otherwise it won't actually scroll to the bottom
                # in all iterations after the first.
                self._scroll_bottom()

                # Click "load more" button
                self.driver.find_element_by_css_selector("#page-wrapper > div.wrapper.wrapper-content > div > div > "
                                                         "div.col-md-12.publication-list > div > div.recent-comments > "
                                                         "div.publication-list > div.text-center > button").click()
                print(f'Clicked "Load more" button. Location is now page {page_num+1}.')

        def _scroll_bottom(self):
            """Scrolls to the bottom of the page using a simple javascript function."""
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        def get_links(self, soup):
            """Retrieves links from a given soup object.

            Args:
                soup (BeautifulSoup): A BeautifulSoup object containing
                the html code.

            Returns:
                list[str]: A list of URLs for found Pubpeer publications.
            """
            soup_links = [str(link.get('href')) for link in soup.find_all('a')]
            articles = []

            for link in soup_links:
                if link[0:13] == '/publications':
                    articles.append(f'https://pubpeer.com{link}')

            return articles

        def show_articles(self, articles):
            """Prints articles given a list of articles.

            Args:
                articles (list[str]): List of article URLs.
            """
            for index, paper in enumerate(articles, start=1):
                print(f'Paper {index}: {paper}')
