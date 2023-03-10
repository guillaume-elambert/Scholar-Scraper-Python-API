import json
from concurrent.futures import ThreadPoolExecutor
from typing import List

from scholarly import scholarly

from .CustomScholarlyTypes import SimplifiedAuthor
from .utilities import JSONEncoder


def getAuthorData(scholarId: str):
    """
    Retrieve the author's data from Google Scholar.
    :param scholarId: The id of the author on Google Scholar.
    :return: The author's data.
    """
    # Retrieve the author's data
    author = scholarly.search_author_id(scholarId)

    # Cast the author to Author object
    newauthor = SimplifiedAuthor(author)

    return newauthor


# Threaded function for queue processing.
def crawl(work: tuple):
    """
    Crawl the author's data from Google Scholar.
    :param work: A tuple containing the index and scholarId of the author to fetch.
    :return: The author's data or None if an error occurred.
    """
    data = None
    try:
        data = getAuthorData(work[1])
    finally:
        return data
        pass


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

        # Use many threads (self.max_threads max, or one for each scholarId)
        num_threads = min(self.max_threads, len(self.scholarIds))

        # Initialize a thread pool executor
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Create a list of tuples containing the index and scholarId of each author to fetch
            works = [(index_id, scholarId) for index_id, scholarId in enumerate(self.scholarIds)]

            # Submit the crawl function to the thread pool executor with each work item
            futures = [executor.submit(crawl, work) for work in works]

            # Retrieve the results of each crawl function
            results = [future.result() for future in futures if future.result() is not None]

        self.authorsList.extend(results)
        return json.dumps(self.authorsList, cls=JSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)
