
"""
Scrapes quotes from 'https://creativequotations.com

"""


from lxml import html
import requests
import re
import math
from log3 import log
import csv


def get_matches_found(keyword):
    """ Get total number of matching quotes for an specific keyword

    Args:
        keyword (str): The topic or subject of interest

    Returns:
        int: Integer representing amount of matches found

    """

    params = {
        'keyword': keyword,
        'boolean': 'and',
        'field': 'all',
        'frank': 'all',
        'database': 'all',

    }
    resp = requests.get('https://creativequotations.com/cgi-bin/sql_search3.cgi', params=params)

    doc = html.fromstring(resp.content)

    matches_found = doc.xpath('//b[contains(text(), "matches found")]/text()')[0]

    rx = re.compile('\d+')

    return int(re.search(rx, matches_found)[0])


def fetch_quotes(keyword, start=0):
    """ Fetch quotes from keyword

    Args:
        keyword (str): The topic or subject of interest
        start (int): Location to start fetching quotes. 50, 100, 150, etc

    Yields:
          quote, author: A tuple containing quote, and author

    """
    params = {
        'keyword': keyword,
        'boolean': 'and',
        'field': 'all',
        'frank': 'all',
        'database': 'all',
        'start': start

    }
    log.info('Fetching quotes for keyword %s' % keyword)
    resp = requests.get('https://creativequotations.com/cgi-bin/sql_search3.cgi', params=params)

    doc = html.fromstring(resp.content)

    quotes = [quote.text_content().strip("\"") for quote in doc.xpath('//li/b')]
    authors = [author.split('(')[0].strip() for author in doc.xpath('//li/b/following-sibling::text()[2]')]
    matches_found = doc.xpath('//b[contains(text(), "matches found")]/text()')[0]

    rx = re.compile('\d+')

    matches_found = re.search(rx, matches_found)[0]

    for quote, author in zip(quotes, authors):
        yield quote, author


def fetch_all_quotes(keyword):
    """ Scrape all quotes for an specific given keyword

    Args:
        keyword (str): The topic or subject of interest

    Returns:
        list: A list of quote tuples


    """

    quotes = []

    # Fetch it once to get how many matches are found
    matches_found = get_matches_found(keyword)

    for i in range(0, math.ceil(matches_found), 50):
        for quote, author in fetch_quotes(keyword, start=i):
            quotes.append((quote, author))

    return quotes


def write_to_csv(quotes, filename="out.csv"):
    """ Write quote list tuple to csv. Defaults to csv

    Args:
        quotes (list): List of quote tuples
        filename: Filename of output csv

    """
    with open(filename, 'w+') as file:
        writer = csv.writer(file, quotechar='"')
        writer.writerows(quotes)
        log.success("File was writen to %s" % filename )


if __name__ == '__main__':

    nature_quotes = fetch_all_quotes('god')
    write_to_csv(nature_quotes, filename="god.csv")

