from pybliometrics.scopus import AbstractRetrieval
from semanticscholar import SemanticScholar
from toml import dump
import subprocess
import bibtexparser

toml_dict = {
    'editor': {'name': 'Shuoan Li', 'degree': 'Undergraduate, 2022'},
    'article': {},
}

dois = []
publishes = []
categories = []
summaries = []
with open('dois.txt') as f:
    lines = f.read().strip().split('\n')
    for line in lines:
        info = line.split('|')
        dois.append(info[0])
        publishes.append(info[1])
        categories.append(info[2])
        summaries.append(info[3])

def assign(field, value):
    if toml_dict['article'][str(i + 1)][field] == '' and value != None:
        toml_dict['article'][str(i + 1)][field] = value

for i in range(0, len(dois)):
    doi = dois[i]
    toml_dict['article'][str(i + 1)] = {
                'title': '',
                'doi': 'https://doi.org/{}'.format(doi),
                'authors': '',
                'journal': '',
                'publish': publishes[i],
                'category': categories[i],
                'summary': summaries[i],
                'abstract': '',
                'keywords': '',
            }
    article_n = f'article.{i + 1}'
    try:
        print(f'Trying scopus for {article_n}')
        article = AbstractRetrieval(doi, id_type='doi', view='FULL')
        keywords = ''
        authors = []
        abstract = ''
        if article.authkeywords != None:
            keywords = ', '.join(article.authkeywords)
        if article.authors != None:
            for author in article.authors:
                authors.append('{} {}'.format(author[3], author[2]))
        if article.abstract != None:
            abstract = article.abstract[article.abstract.find('.') + 1:]
        assign('title', article.title)
        assign('authors', ', '.join(authors))
        assign('journal', article.publicationName)
        assign('abstract', abstract)
        assign('keywords', keywords)
        print(f'{article_n} succeeded with scopus')
    except:
        print(f'{article_n} failed with scopus')
    try:
        print(f'Trying doi2bib for {article_n}')
        bib = subprocess.run(['doi2bib', doi], stdout = subprocess.PIPE).stdout
        article = bibtexparser.parse_string(bib.decode('utf-8')).entries[0].fields_dict
        assign('title', article['title'].value)
        assign('authors', ', '.join(article['author'].value.split(' and ')))
        assign('journal', article['journal'].value)
        print(f'article.{i + 1} succeeded with doi2bib')
    except:
        print(f'article {i + 1} failed with doi2bib')
    try:
        print(f'Trying semanticscholar for {article_n}')
        sch = SemanticScholar()
        article = sch.get_paper(doi)
        authors = ', '.join([a['name'] for a in article.authors])
        assign('title', article.title)
        assign('authors', authors)
        assign('journal', article.journal)
        assign('abstract', article.abstract)
        print(f'article.{i + 1} succeeded with semanticscholar')
    except:
        print(f'{article_n} failed with semanticscholar')

with open('out.toml', 'w') as f:
    dump(toml_dict, f)
