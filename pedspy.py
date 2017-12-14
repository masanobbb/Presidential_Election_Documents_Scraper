from urllib import request
from bs4 import BeautifulSoup
import time
import pandas as pd
from dateutil import parser


def get_documents_urls(candidate_name, year):
    """

    :param candidate_name: president candidate name
    :param year:        the year of election
    :return:            the list of the urls where there are the candidate's campaign speeches, statements, press releases, so on.
    """
    root_url = 'http://www.presidency.ucsb.edu/'
    target_url = root_url + str(year) + '_election.php'

    response = request.urlopen(target_url)
    body = response.read()
    soup = BeautifulSoup(body, "html.parser")

    # find urls where any kind of the president candidate's documents are sleeping
    urls = []
    for a in soup.find_all('a'):
        last_name = candidate_name.split()[-1]
        if last_name in a.get('href').lower():
            # print(a.get('href'))
            urls.append(root_url + a.get('href'))

    return urls


def get_document_type(url):
    """

    :param url: the url has a type of documents such as campaign speeches, statements, press releases, so on.
    :return: the document type of presidential election documents
    """
    doc_type = ""

    return doc_type


def get_documents(year, candidate_name):
    """

    :param candidate_name:  president candidate name
    :param year:            the year of election
    :return:                the list of the urls where there are the candidate's campaign speeches, statements, press releases, so on.
    """
    documents_df = pd.DataFrame()
    root_url = "http://www.presidency.ucsb.edu"
    count = 0

    # get the urls where "campaign speeches", "statements", "press releases", etc. are sleeping
    documentsUrls = get_documents_urls(year, candidate_name)

    # get the documents' text data
    for url in documentsUrls:

        response = request.urlopen(url)
        body = response.read*()
        soup = BeautifulSoup(body, "html,parser")

        # get the type of documents
        # such as "campaign speeches", "statements", "press releases", etc.
        doctype = get_document_type()

        for link in soup.find_all('a'):

            href = link.get('href')

            if 'index.php' in href and 'ws' in href:
                href = href.replace('..', root_url)

                # keep the stating time
                startTime = time.time()

                page_response = request.urlopen(href)
                page_body = page_response.read()
                soup = BeautifulSoup(page_body, "html.parser")

                speech = ""
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
                                                    "doctype": doctype,
                                                    "title": title,
                                                    "speech": speech,
                                                    "source": source_url},
                                                   index=[count])])

                # take some time to get next documents
                count += 1
                end_time = time.time()
                if (end_time - startTime) > 1:
                    time.sleep(1)

        return documents_df

