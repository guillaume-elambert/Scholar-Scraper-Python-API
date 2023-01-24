import json
import sys
from queue import Queue
from threading import Thread
from typing import List

from scholarly import scholarly

from CustomScholarlyTypes import SimplifiedAuthor
from utilities import JSONEncoder


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


if __name__ == '__main__':
    """
    Main function.
    """

    # Check that there is a least one parameter
    if len(sys.argv) < 2:
        print('Usage: python3 __init__.py <query>')
        sys.exit(1)

    scholarIds = sys.argv[1:]
    authorsList = []
    threads = []

    # Initialize an infinite queue
    queue = Queue(maxsize=0)

    # Use many threads (50 max, or one for each scholarId)
    num_theads = min(2, len(scholarIds))

    # Iterate over all the scholarIds using index
    for index_id, scholarId in enumerate(scholarIds):
        queue.put((index_id, scholarId))

    # Starting worker threads on queue processing
    for i in range(num_theads):
        worker = Thread(target=crawl, args=(queue, authorsList))
        worker.start()

    # Now we wait until the queue has been processed
    queue.join()

    print(json.dumps(authorsList, cls=JSONEncoder, sort_keys=True, indent=4, ensure_ascii=False))
