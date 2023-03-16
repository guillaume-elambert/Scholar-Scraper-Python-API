# Scholar Scraper

This is a simple script to scrape the Google Scholar page of given authors and extract all the information about them (
publications, cites per year, etc.).

The script is written in Python 3 and uses the [`scholarly`](https://github.com/scholarly-python-package/scholarly)
library.

<br/>

## Installation

The script can be installed through `pip` and PyPI:

```bash
pip install scholar-scraper
```

Or via Github sources:

```bash
pip install git+https://github.com/guillaume-elambert/Scholar-Scraper-Python-API.git
```

<br/>

Or it can be installed by cloning the repository:

```bash
git clone https://github.com/guillaume-elambert/Scholar-Scraper-Python-API.git
cd Scholar-Scraper-Python-API
pip install -e .
```

<br/>

## Usage

The script is simple to use. It takes a list of authors Google Scholar IDs as input and outputs a JSON file with all the
information about the authors.

```python
from scholar_scraper import scholar_scraper

# Define the list of authors Google Scholar IDs
scholarIds = [ 
    '1iQtvdsAAAAJ',
    'dAKCYJgAAAAJ'
]

# Start scraping and print the resulted JSON to the console
print(scholar_scraper.start_scraping(scholarIds))
```

<br/>

To reduce the time needed to scrape the authors, the script uses multithreading (one thread per user).<br/>
The number of threads can be set using the `max_threads` parameter, which default value 10 :

```python
from scholar_scraper import scholar_scraper

# Define the maximum number of threads to use
max_threads = 5

# Define the list of authors Google Scholar IDs
scholarIds = [ 
    '1iQtvdsAAAAJ',
    'dAKCYJgAAAAJ'
]

# Start scraping with maximum 5 threads and print the resulted JSON to the console
# Since the number of authors is 2, the number of threads used will be reduced to 2
# If the number of authors is 10, the number of threads used will be reduced to 5
# If you don't pass any value to the max_threads parameter, the default value of 10 will be used
print(scholar_scraper.start_scraping(scholarIds, max_threads))
```

<br/>

## Output example

The output is a JSON file containing all the information about the authors.<br/>
Here is an example of the simplified output for the authors with the Google Scholar IDs `1iQtvdsAAAAJ` and `dAKCYJgAAAAJ`:

```json
[
  {
    "affiliation": "Tenure-Track Assistant Professor, DIEM, University of Salerno",
    "citedby": 796,
    "cites_per_year": {
      "2013": 2,
      "2014": 9,
      "2015": 21,
      "2016": 34,
      "2017": 46,
      "2018": 83,
      "2019": 127,
      "2020": 124,
      "2021": 182,
      "2022": 140,
      "2023": 22
    },
    "coauthors": [
      {
        "affiliation": "University of Salerno, Dept. of Information and Electrical Engineering and Applied Math (DIEM)",
        "name": "Prof. Mario Vento, Ph.D.",
        "scholar_id": "3PwXGpgAAAAJ"
      },
    ],
    "interests": [
      "Pattern Recognition",
      "Artificial Intelligence",
      "Graph Based Representation"
    ],
    "name": "Vincenzo Carletti, Ph.D.",
    "organization": 8098754970055108159,
    "publications": [
      {
        "abstract": "Graph matching is essential in several fields that use structured information, such as biology, chemistry, social networks, knowledge management, document analysis and others. Except for special classes of graphs, graph matching has in the worst-case an exponential complexity; however, there are algorithms that show an acceptable execution time, as long as the graphs are not too large and not too dense. In this paper we introduce a novel subgraph isomorphism algorithm, VF3, particularly efficient in the challenging case of graphs with thousands of nodes and a high edge density. Its performance, both in terms of time and memory, has been assessed on a large dataset of 12,700 random graphs with a size up to 10,000 nodes, made publicly available. VF3 has been compared with four other state-of-the-art algorithms, and the huge experimentation required more than two years of processing time. The results …",
        "author": "Vincenzo Carletti and Pasquale Foggia and Alessia Saggese and Mario Vento",
        "author_pub_id": "1iQtvdsAAAAJ:uJ-U7cs_P_0C",
        "citation": "IEEE transactions on pattern analysis and machine intelligence 40 (4), 804-818, 2017",
        "cites_per_year": {
          "2018": 10,
          "2019": 20,
          "2020": 21,
          "2021": 28,
          "2022": 31,
          "2023": 4
        },
        "journal": "IEEE transactions on pattern analysis and machine intelligence",
        "num_citations": 114,
        "number": "4",
        "pages": "804-818",
        "pub_url": "https://ieeexplore.ieee.org/abstract/document/7907163/",
        "pub_year": 2017,
        "publisher": "IEEE",
        "title": "Challenging the time complexity of exact subgraph isomorphism for huge and dense graphs with VF3",
        "url_related_articles": "/scholar?oi=bibs&hl=en&oe=ASCII&q=related:8y95I731FVoJ:scholar.google.com/",
        "volume": "40"
      },
      {
        "abstract": "The actual research activity at MIVIA (Machine Intelligence for recognition of Video, Images and Audio) lab involves the study of innovative methods for behavioral analysis in surveillance videos and for events detection in audio streams, the development of techniques for biomedical images analysis and algorithms for graph matching. Moreover, in the last years, part of the research activity of the MIVIA lab is dedicated to the implementation of those approaches on embedded systems.",
        "author": "Vincenzo Carletti and Luca Del Pizzo and Rosario Di Lascio and Pasquale Foggia and Gennaro Percannella and Alessia Saggese and Nicola Strisciuglio and Mario Vento",
        "author_pub_id": "1iQtvdsAAAAJ:eQOLeE2rZwMC",
        "citation": "",
        "cites_per_year": {},
        "num_citations": 0,
        "pub_url": "https://girpr2014.unisa.it/files/MIVIA2014.pdf",
        "title": "Research Activities@ MIVIA Lab",
        "url_related_articles": "/scholar?oi=bibs&hl=en&oe=ASCII&q=related:fXoMTa-V5boJ:scholar.google.com/"
      }
    ],
    "scholar_id": "1iQtvdsAAAAJ"
  },
  {
    "affiliation": "Laboratoire d'Informatique Fondamentale et Appliquée de Tours (Polytech' Tours)",
    "citedby": 3319,
    "cites_per_year": {
      "2004": 12,
      "2005": 37,
      "2006": 31,
      "2007": 74,
      "2008": 68,
      "2009": 90,
      "2010": 112,
      "2011": 142,
      "2012": 158,
      "2013": 219,
      "2014": 244,
      "2015": 254,
      "2016": 257,
      "2017": 256,
      "2018": 225,
      "2019": 280,
      "2020": 240,
      "2021": 292,
      "2022": 244,
      "2023": 28
    },
    "coauthors": [
      {
        "affiliation": "Professor of Computer Engineering, University of Salerno",
        "name": "Pasquale Foggia",
        "scholar_id": "P9eeLD8AAAAJ"
      },
    ],
    "homepage": "https://www.univ-tours.fr/m-donatello-conte--554674.kjsp",
    "interests": [
      "Structural Pattern Recognition",
      "Graph Matching",
      "Video Surveillance Systems",
      "Image Quality Assessment",
      "Affective Computing"
    ],
    "name": "Donatello Conte",
    "organization": 9820397017780423431,
    "publications": [
      {
        "abstract": "A recent paper posed the question: \"Graph Matching: What are we really talking about?\". Far from providing a definite answer to that question, in this paper we will try to characterize the role that graphs play within the Pattern Recognition field. To this aim two taxonomies are presented and discussed. The first includes almost all the graph matching algorithms proposed from the late seventies, and describes the different classes of algorithms. The second taxonomy considers the types of common applications of graph-based techniques in the Pattern Recognition and Machine Vision field.",
        "author": "Donatello Conte and Pasquale Foggia and Carlo Sansone and Mario Vento",
        "author_pub_id": "dAKCYJgAAAAJ:u5HHmVD_uO8C",
        "citation": "International journal of pattern recognition and artificial intelligence 18 …, 2004",
        "cites_per_year": {
          "2004": 10,
          "2005": 29,
          "2006": 25,
          "2007": 60,
          "2008": 50,
          "2009": 62,
          "2010": 78,
          "2011": 97,
          "2012": 115,
          "2013": 127,
          "2014": 147,
          "2015": 157,
          "2016": 152,
          "2017": 144,
          "2018": 121,
          "2019": 128,
          "2020": 108,
          "2021": 109,
          "2022": 84,
          "2023": 9
        },
        "journal": "International journal of pattern recognition and artificial intelligence",
        "num_citations": 1834,
        "number": "03",
        "pages": "265-298",
        "pub_url": "https://www.worldscientific.com/doi/abs/10.1142/S0218001404003228",
        "pub_year": 2004,
        "publisher": "World Scientific Publishing Company",
        "title": "Thirty years of graph matching in pattern recognition",
        "url_related_articles": "/scholar?oi=bibs&hl=en&oe=ASCII&q=related:Up-aWBC_pBYJ:scholar.google.com/",
        "volume": "18"
      },
      {
        "abstract": "3 Lyon Research Center for Images and Information Systems UMR CNRS 5205 Bat. J. Verne INSA Lyon 69621 Villeurbanne Cedex, France jolion@ rfv. insa-lyon. fr",
        "author": "Donatello Conte and Pasquale Foggia and Jean-Michel Jolion and Mario Vento",
        "author_pub_id": "dAKCYJgAAAAJ:MXK_kJrjxJIC",
        "citation": "",
        "cites_per_year": {},
        "num_citations": 0,
        "pub_url": "https://scholar.google.com/scholar?cluster=1028334572382745959&hl=en&oi=scholarr",
        "title": "pyramides de graphes",
        "url_related_articles": "/scholar?oi=bibs&hl=en&q=related:Z3UgYdhgRQ4J:scholar.google.com/"
      }
    ],
    "scholar_id": "dAKCYJgAAAAJ"
  }
]
```