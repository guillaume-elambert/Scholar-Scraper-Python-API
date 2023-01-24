from typing import List

from scholarly import scholarly
from scholarly.author_parser import AuthorParser
from scholarly.data_types import Author, Publication, CitesPerYear

from utilities import getObjectPublicAttributes


class SimplifiedPublication:
    """
    :class:`SimplifiedPublication <SimplifiedPublication>` object used to represent a simplified publication
    entry on Google Scholar.
    """

    author_id: List[str] = None
    """
    List of the corresponding author ids of the authors that contributed to the Publication. 
    (source: PUBLICATION_SEARCH_SNIPPET)
    """

    num_citations: int = None
    "Number of citations of this Publication."

    cites_per_year: CitesPerYear = None
    "A dictionary containing the number of citations per year for this Publication. (source: AUTHOR_PUBLICATION_ENTRY)"

    pub_url: str = None
    "URL of the website providing the publication."

    author_pub_id: str = None
    """
    The id of the paper on Google Scholar from an author page. Comes from the
    parameter "citation_for_view=PA9La6oAAAAJ:YsMSGLbcyi4C". It combines the
    author id, together with a publication id. It may corresponds to a merging
    of multiple publications, and therefore may have multiple "citedby_id"
    values. (source: AUTHOR_PUBLICATION_ENTRY)
    """

    url_related_articles: str = None
    "The URL containing link for related articles of a publication. (needs fill() for AUTHOR_PUBLICATION_ENTRIES)"

    _class_attributes: List[str] = None
    "List of all the public attributes of the class."

    #
    # From there, the attributes are obtained from the BibEntry object : "bib" attribute of a publication.
    #
    pub_type: str = None
    "The type of entry for this bib (for example 'article'). (source: PUBLICATION_SEARCH_SNIPPET)"

    bib_id: str = None
    "Bib entry id. (source: PUBLICATION_SEARCH_SNIPPET)"

    abstract: str = None
    "Description of the publication."

    title: str = None
    "Title of the publication."

    author: str = None
    "List of the author names that contributed to this publication."

    pub_year: str = None
    "The year the publication was first published."

    venue: str = None
    "The venue of the publication. (source: PUBLICATION_SEARCH_SNIPPET)"

    journal: str = None
    "Journal Name. (source: PUBLICATION_SEARCH_SNIPPET)"

    volume: str = None
    "Number of years a publication has been circulated."

    number: str = None
    "NA number of a publication."

    pages: str = None
    "Range of pages."

    publisher: str = None
    "The publisher's name."

    citation: str = None
    """
    Formatted citation string, usually containing journal name, volume and page numbers.
    (source: AUTHOR_PUBLICATION_ENTRY)
    """

    def __init__(self, publication: Publication):
        # Get all the public attributes of the class
        self._class_attributes = getObjectPublicAttributes(self)

        if publication['container_type'] != "Publication":
            raise ValueError("The given object is not a Publication object.")

        if not publication['filled']:
            scholarly.fill(publication)

        # Remove the attributes that are defined by the "bib" attribute of the publication,
        # since it is a BibEntry object, and we want it right in the object
        attributes_to_use = self._class_attributes.copy()
        bib_attributes = None
        if 'bib' in publication:
            bib_attributes = list(publication['bib'])
            for attribute in bib_attributes:
                if attribute in attributes_to_use:
                    attributes_to_use.remove(attribute)

        # Copy all the needed attributes to the object
        for attribute in self._class_attributes:
            if attribute in publication:
                self.__dict__[attribute] = publication[attribute]

        # Handle the specificity of the attributes of the bib: Copy them to the root of the object
        if bib_attributes:
            for attribute in bib_attributes:
                if attribute in self._class_attributes:
                    self.__dict__[attribute] = publication['bib'][attribute]


    def __str__(self):
        """
        Simple string representation of the object.
        :return: The string representation of the object
        """
        return str(self.__dict__)


class SimplifiedCoauthor:
    """
    :class:`SimplifiedCoauthor <SimplifiedCoauthor>` object used to represent a simplified coauthor entry on Google Scholar.
    """

    scholar_id: str = None
    "The id of the author on Google Scholar."

    name: str = None
    "The name of the author."

    affiliation: str = None
    "The affiliation of the author."

    _class_attributes: List[str] = None
    "List of all the public attributes of the class."

    def __init__(self, coauthor: dict):
        # Get all the public attributes of the class
        self._class_attributes = getObjectPublicAttributes(self)

        if coauthor['container_type'] != "Author":
            raise ValueError("The given object is not an Author object.")

        # Copy all the needed attributes to the object
        for attribute in self._class_attributes:
            if attribute in coauthor:
                self.__dict__[attribute] = coauthor[attribute]

    def __str__(self):
        """
        Simple string representation of the object.
        :return: The string representation of the object
        """
        return str(self.__dict__)


class SimplifiedAuthor(SimplifiedCoauthor):
    """
    :class:`SimplifiedAuthor <SimplifiedAuthor>` object used to represent a simplified author entry on Google Scholar.
    """

    organization: int = None
    "A unique ID of the organization. (source: AUTHOR_PROFILE_PAGE)"

    homepage: str = None
    "URL of the homepage of the author."

    citedby: int = None
    "The number of citations to all publications. (source: SEARCH_AUTHOR_SNIPPETS)."

    interests: List[str] = None
    "Fields of interest of this Author. (sources: SEARCH_AUTHOR_SNIPPETS, AUTHOR_PROFILE_PAGE)"

    cites_per_year: CitesPerYear = None
    "Breakdown of the number of citations to all publications over the years. (source: SEARCH_AUTHOR_SNIPPETS)"

    publications: List[SimplifiedPublication] = None
    "A list of publications objects. (source: SEARCH_AUTHOR_SNIPPETS)"

    coauthors: List[SimplifiedCoauthor] = None  # List of authors. No self dict functionality available
    "A list of coauthors (list of Author objects). (source: SEARCH_AUTHOR_SNIPPETS)"

    def __init__(self, author: Author = None):
        # Call super constructor
        super().__init__(author)

        if author['container_type'] != "Author":
            raise ValueError("The given object is not an Author object.")

        if len(author['filled']) != len(AuthorParser(None)._sections):
            scholarly.fill(author)

        # Remove the attributes 'publications' and 'coauthors' from the list, since they are lists of
        # SimplifiedPublication and SimplifiedCoauthor objects. Make sure the original list is not modified.
        attributes_to_use = self._class_attributes.copy()
        attributes_to_use.remove('publications')
        attributes_to_use.remove('coauthors')

        # Copy all the needed attributes to the object
        for attribute in attributes_to_use:
            if attribute in author:
                self.__dict__[attribute] = author[attribute]

        # Casting the publications to SimplifiedPublication objects if they exist and are of type list
        if 'publications' in author and isinstance(author['publications'], list):
            self.publications = [SimplifiedPublication(pub) for pub in author['publications']]

        # Casting the coauthors to SimplifiedCoauthor objects if they exist and are of type list
        if 'coauthors' in author and isinstance(author['coauthors'], list):
            self.coauthors = [SimplifiedCoauthor(coauthor) for coauthor in author['coauthors']]

    def __str__(self):
        """
        Simple string representation of the object.
        :return: The string representation of the object
        """
        return str(self.__dict__)
