import json
from concurrent.futures import ThreadPoolExecutor
from typing import List

from scholarly import scholarly, ProxyGenerator

from .CustomScholarlyTypes import SimplifiedAuthor
from .utilities import JSONEncoder

MAX_RETRIES = 10


def set_new_proxy():
    """
    Set a new proxy for the scholarly library.
    :return: The new proxy.
    """

    pg = ProxyGenerator()

    for i in range(MAX_RETRIES):
        try:
            if pg.FreeProxies() and scholarly.use_proxy(pg):
                break
        except:
            pass
    return pg


def getAuthorData(scholarId: str):
    """
    Retrieve the author's data from Google Scholar.
    :param scholarId: The id of the author on Google Scholar.
    :return: The author's data.
    """
    # Retrieve the author's data
    author = scholarly.search_author_id(scholarId)

    # Cast the author to Author object
    return SimplifiedAuthor(author)


# Threaded function for queue processing.
def crawl(scholarID: str):
    """
    Crawl the author's data from Google Scholar.
    :param scholarID: A Google Scholar ID string.
    :return: The author's data or None if an error occurred.
    """
    data = None

    # Try to get the data 10 times at most
    for i in range(MAX_RETRIES):
        try:
            data = getAuthorData(scholarID)
            break
        # If an error occurred, try again with a new proxy
        except:
            set_new_proxy()

    return data


class ScholarScraper:
    """
    :class:`ScholarScraper <ScholarScraper>` object used to retrieve the data of a list of authors from Google Scholar.
    """

    def __init__(self, scholarIds: List[str] = [], max_threads: int = 10):
        """
        :param scholarIds: The list of the ids of the authors on Google Scholar.
        :param max_threads: The maximum number of threads to use for the scraping process.
        """

        self.scholarIds = scholarIds
        self.max_threads = max_threads
        self.authorsList = []
        self.threads = []

    def start_scraping(self, scholarIds: List[str] = None, max_threads: int = None):
        """
        Start the scraping process.
        :param scholarIds: The list of the ids of the authors on Google Scholar.
        :param max_threads: The maximum number of threads to use for the scraping process.
        :return: The list of the authors' data as JSON.
        """
        self.authorsList = []
        self.threads = []
        self.scholarIds = scholarIds if scholarIds else self.scholarIds
        self.max_threads = max_threads if max_threads else self.max_threads

        if self.max_threads == 1:
            for scholarId in self.scholarIds:
                self.authorsList.append(crawl(scholarId))
            return json.dumps(self.authorsList, cls=JSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)

        # Use many threads (self.max_threads max, or one for each scholarId)
        num_threads = min(self.max_threads, len(self.scholarIds))

        # Initialize a thread pool executor
        with ThreadPoolExecutor(max_workers=num_threads) as executor:

            # Submit the crawl function to the thread pool executor with each work item
            futures = [executor.submit(crawl, work) for work in self.scholarIds]

            # Retrieve the results of each crawl function
            for future in futures:
                if future.result() is not None:
                    self.authorsList.append(future.result())

            return json.dumps(self.authorsList, cls=JSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)
