import json
from queue import Queue
from threading import Thread
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
def crawl(queue: Queue, results: List):
    """
    Crawl the author's data from Google Scholar.
    :param queue: The queue to fetch the work from.
    :param results: The list to append the results to.
    :return: Always true.
    """
    while not queue.empty():
        # Fetch new work from the Queue
        work = queue.get()

        try:
            data = getAuthorData(work[1])
            results.append(data)
        except:
            pass

        # Signal to the queue that task has been processed
        queue.task_done()
    return True


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

        # Initialize an infinite queue
        queue = Queue(maxsize=0)

        # Use many threads (self.max_threads max, or one for each scholarId)
        num_theads = min(self.max_threads, len(self.scholarIds))

        # Iterate over all the scholarIds using index
        for index_id, scholarId in enumerate(self.scholarIds):
            queue.put((index_id, scholarId))

        # Starting worker threads on queue processing
        for i in range(num_theads):
            worker = Thread(target=crawl, args=(queue, self.authorsList))
            worker.start()

        # Now we wait until the queue has been processed
        queue.join()

        return json.dumps(self.authorsList, cls=JSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)
