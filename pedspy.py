from urllib import request
from bs4 import BeautifulSoup
import time
import pandas as pd
from dateutil import parser
import pickle
import re
import nltk


def getDocumentsUrl(person_name, year):
    """
    :param person_name: president candidate name
    :param year:        the year of election
    :return:            the list of the urls where there are the candidate's campaign speeches, statements, press releases, so on.
    """
    target_url = 'http://www.presidency.ucsb.edu/' + str(year) + '_election.php'

    response = request.urlopen(target_url)
    body = response.read()
    soup = BeautifulSoup(body, "html.parser")

    urls = []
    for a in soup.find_all('a'):
        last_name = person_name.split()[-1]
        if last_name in a.get('href').lower():
            # print(a.get('href'))
            urls.append(a.get('href'))

    return urls

