import json
import sys

from scholarly import scholarly

from CustomTypes import SimplifiedAuthor
from utilities import JSONEncoder

# Check that there is a least one parameter
if len(sys.argv) < 2:
    print('Usage: python3 __init__.py <query>')
    sys.exit(1)

authorsList = []

# For each argument, search for the author
for scholarId in sys.argv[1:]:
    try:
        # Retrieve the author's data
        author = scholarly.search_author_id(scholarId)

        # Cast the author to Author object
        newauthor = SimplifiedAuthor(author)
        authorsList.append(newauthor)
    finally:
        pass

print(json.dumps(authorsList, cls=JSONEncoder, sort_keys=True, indent=4, ensure_ascii=False))
