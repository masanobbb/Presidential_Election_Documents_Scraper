from urllib import request
from bs4 import BeautifulSoup
import time
import pandas as pd
from dateutil import parser


class Pedspy(object):
    """
    Presidential Election Documents Scraper

    Attributes:
        name: presidential candidate name
        year: the year of the election
        doc_urls: the dictionary {doc_type : url}
        documents: Pandas DataFrame with columns: date, doc_type, text, title, source
    """
    def __init__(self, candidate_name, year):
        self.name = candidate_name
        self.year = year
        self.doc_urls = self.__get_documents_urls()
        self.documents = self.__get_documents()  # takes time

    def __get_documents_urls(self):
        """

        :return:
            the dictionary of the documents' type and url where many docs exists
            such as the candidate's campaign speeches, statements, press releases, so on.
        """
        root_url = 'http://www.presidency.ucsb.edu/'
        target_url = root_url + str(self.year) + '_election.php'

        response = request.urlopen(target_url)
        body = response.read()
        soup = BeautifulSoup(body, "html.parser")

        # find urls where any kind of the president candidate's documents are sleeping
        doc_urls = {}
        for a in soup.find_all('a'):
            last_name = self.name.split()[-1]
            if last_name in a.get('href').lower():
                doc_type = a.get_text().replace(' ', '_')
                url = root_url + a.get('href')
                doc_urls[doc_type] = url

        return doc_urls

    def __get_documents(self):
        """

        :return:            the pandas dataframe
                            columns: date, text, doc_type, title, source
        """
        documents_df = pd.DataFrame()
        root_url = "http://www.presidency.ucsb.edu"
        count = 0

        # get the documents' text data
        for doc_type, url in self.doc_urls.items():
            response = request.urlopen(url)
            body = response.read()
            soup = BeautifulSoup(body, "html.parser")

            for link in soup.find_all('a'):

                href = link.get('href')

                if 'index.php' in href and 'ws' in href:
                    href = href.replace('..', root_url)

                    # keep the stating time
                    start_time = time.time()

                    page_response = request.urlopen(href)
                    page_body = page_response.read()
                    soup = BeautifulSoup(page_body, "html.parser")

                    title = ""
                    date = ""
                    text = ""
                    source_url = href

                    for display_text in soup.find_all("span", class_="displaytext"):
                        text = text + display_text.text
                        break

                    for papers_title in soup.find_all("span", class_="paperstitle"):
                        title = papers_title.text
                        break

                    for doc_date in soup.find_all("span", class_="docdate"):
                        date = parser.parse(doc_date.text).strftime('%Y-%m-%d')
                        break

                    documents_df = pd.concat([documents_df,
                                              pd.DataFrame({"date": date,
                                                            "text": text,
                                                            "doc_type": doc_type,
                                                            "title": title,
                                                            "source": source_url},
                                                           index=[count])])
                    count += 1

                    # take some time to get next documents
                    end_time = time.time()
                    if (end_time - start_time) > 1:
                        time.sleep(1)

        return documents_df
