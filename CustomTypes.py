from typing import List

from scholarly import scholarly
from scholarly.author_parser import AuthorParser
from scholarly.data_types import Author, Publication, CitesPerYear

from utilities import getObjectPublicAttributes


class SimplifiedPublication:
    """
    :class:`Publication <Publication>` object used to represent a simplified publication entry on Google Scholar.
    """

    author_id: List[str] = None
    """List of the corresponding author ids of the authors that contributed to the Publication. 
    (source: PUBLICATION_SEARCH_SNIPPET)"""

    num_citations: int = None
    """Number of citations of this Publication."""

    cites_per_year: CitesPerYear = None
    """A dictionary containing the number of citations per year for this Publication. 
    (source: AUTHOR_PUBLICATION_ENTRY)"""

    pub_url: str = None
    """URL of the website providing the publication."""

    author_pub_id: str = None
    """The id of the paper on Google Scholar from an author page. Comes from the
      parameter "citation_for_view=PA9La6oAAAAJ:YsMSGLbcyi4C". It combines the
      author id, together with a publication id. It may corresponds to a merging
      of multiple publications, and therefore may have multiple "citedby_id"
      values. (source: AUTHOR_PUBLICATION_ENTRY)"""

    url_related_articles: str = None
    """The URL containing link for related articles of a publication. (needs fill() for AUTHOR_PUBLICATION_ENTRIES)"""

    _class_attributes: List[str] = None
    """List of all the public attributes of the class."""

    def __init__(self, publication: Publication):
        # Get all the attributes of the class
        # self._class_attributes = [attr for attr in dir(self.__class__) if
        #                not callable(getattr(self.__class__, attr))
        #                and not attr.startswith("__")
        #                and not attr.startswith("_")
        #                and not attr.startswith("_" + self.__class__.__name__ + "__")]
        self._class_attributes = getObjectPublicAttributes(self)

        if publication['container_type'] != "Publication":
            raise ValueError("The given object is not a Publication object.")

        if not publication['filled']:
            scholarly.fill(publication)

        # Copy all the needed attributes to the object
        for key in self._class_attributes:
            self.__dict__[key] = publication[key] if key in publication else None

    def __str__(self):
        """
        Simple string representation of the object.
        :return: The string representation of the object
        """
        return str(self.__dict__)


class SimplifiedAuthor:
    """
    :class:`Author <Author>` object used to represent a simplified author entry on Google Scholar.
    """

    scholar_id: str = None
    """The id of the author on Google Scholar."""

    name: str = None
    """The name of the author."""

    affiliation: str = None
    """The affiliation of the author."""

    organization: int = None
    """A unique ID of the organization. (source: AUTHOR_PROFILE_PAGE)"""

    homepage: str = None
    """URL of the homepage of the author."""

    citedby: int = None
    """The number of citations to all publications. (source: SEARCH_AUTHOR_SNIPPETS)."""

    interests: List[str] = None
    """Fields of interest of this Author. (sources: SEARCH_AUTHOR_SNIPPETS, AUTHOR_PROFILE_PAGE)"""

    cites_per_year: CitesPerYear = None
    """Breakdown of the number of citations to all publications over the years. (source: SEARCH_AUTHOR_SNIPPETS)"""

    publications: List[SimplifiedPublication] = None
    """A list of publications objects. (source: SEARCH_AUTHOR_SNIPPETS)"""

    coauthors: List = None  # List of authors. No self dict functionality available
    """A list of coauthors (list of Author objects). (source: SEARCH_AUTHOR_SNIPPETS)"""

    _class_attributes: List[str] = None
    """List of all the public attributes of the class."""

    def __init__(self, author: Author = None):
        # Get all the attributes of the class
        # self._class_attributes = [attr for attr in dir(self.__class__) if
        #                not callable(getattr(self.__class__, attr))
        #                and not attr.startswith("__")
        #                and not attr.startswith("_")
        #                and not attr.startswith("_" + self.__class__.__name__ + "__")]
        self._class_attributes = getObjectPublicAttributes(self)

        if author['container_type'] != "Author":
            raise ValueError("The given object is not an Author object.")

        if len(author['filled']) != len(AuthorParser(None)._sections):
            scholarly.fill(author)

        # Remove the key 'publications' from the list of attributes, since it is a list of SimplifiedPublication objects
        # Make sure the original list is not modified (cannot directly copy it since it is a class variable)
        attributes_to_use = self._class_attributes
        self._class_attributes = attributes_to_use.copy()
        attributes_to_use.remove('publications')

        # Copy all the needed attributes to the object
        for key in attributes_to_use:
            self.__dict__[key] = author[key] if key in author else None

        # Casting the publications to SimplifiedPublication objects if they exist and are of type list
        if 'publications' in author and isinstance(author['publications'], list):
            self.publications = [SimplifiedPublication(pub) for pub in author['publications']]

    def __str__(self):
        """
        Simple string representation of the object.
        :return: The string representation of the object
        """
        return str(self.__dict__)
