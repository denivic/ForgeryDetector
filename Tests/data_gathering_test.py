# Custom
import time
from ForgeryDetector.core.classifying.classify import ImageClassifier
from ForgeryDetector.core.preprocessing.download import DownloadManager

if __name__ == '__main__':
    classifier = ImageClassifier()
    download = DownloadManager(threads=8)

    ########################################################################################
    # Step 1: Download articles, extract images, and filter them using ML model (optional) #
    ########################################################################################
    '''Pubmed
       for best results of western blots look up biomaterial journals e.g.:
       (("Biomaterials Research"[Journal]) AND western blot[Body - All Words]) OR western blots[Body - All Words]
       However as of now, there is an issue with advanced searches like the one above and I have
       not been able to fix it.
    '''
    parameters = {'db': 'pmc',
                  'retmax': 50,
                  'datetype': 'pdat',
                  'mindate': '2000/01/01',
                  'maxdate': '2021/01/01',
                  'term': 'western blot[Body - All Words] OR western blots[Body - All Words]',
                  'usehistory': 'y'}

    start = time.time()
    articles, _ = download.PubMed.get_links(**parameters)        # Get links given search terms
    download.PubMed.download(articles, rm=True)                  # Download said articles
    end = time.time()
    print(f'Elapsed time PubMed via Entrez API (50 articles): {round(end - start, 2)}s')

    '''Pubpeer'''
    start = time.time()
    soup = download.PubPeer.get_soup('western blot', 4)        # Get PubPeer page content
    articles = download.PubPeer.get_links(soup)                 # Get links for the content
    download.PubPeer.download(articles)                         # Download the images
    end = time.time()
    print(f'Elapsed time PubPeer via webscraping (40 articles): {round(end - start, 2)}s')

    '''Filter images'''
    start = time.time()
    classifier.filter(classifier.DatabaseType.PubMed, delete=True)
    classifier.filter(classifier.DatabaseType.PubPeer, delete=False)
    end = time.time()
    print(f'Elapsed time filtering PubMed & PubPeer images: {round(end - start, 2)}s')
