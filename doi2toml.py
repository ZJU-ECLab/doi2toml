from pybliometrics.scopus import AbstractRetrieval
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
    try:
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
        toml_dict['article'][str(i + 1)]['title'] = article.title
        toml_dict['article'][str(i + 1)]['authors'] = ', '.join(authors)
        toml_dict['article'][str(i + 1)]['journal'] = article.publicationName
        toml_dict['article'][str(i + 1)]['abstract'] = abstract
        toml_dict['article'][str(i + 1)]['keywords'] = keywords
        print(f'article.{i + 1} succeeded with scopus')
    except:
        try:
            bib = subprocess.run(['doi2bib', doi], stdout = subprocess.PIPE).stdout
            article = bibtexparser.parse_string(bib.decode('utf-8')).entries[0].fields_dict
            toml_dict['article'][str(i + 1)]['title'] = article['title'].value
            toml_dict['article'][str(i + 1)]['authors'] = ', '.join(article['author'].value.split(' and '))
            toml_dict['article'][str(i + 1)]['journal'] = article['journal'].value
            print(f'article.{i + 1} succeeded with doi2bib')
        except:
            print(f'article {i + 1} failed with all methods')

with open('out.toml', 'w') as f:
    dump(toml_dict, f)
