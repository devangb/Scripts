################
# Script for downloading research papers of google publications
# https://research.google.com/pubs/
#
################

from bs4 import BeautifulSoup as beautifulsoup
import requests, sys, os

baseurl = 'https://research.google.com'
res = requests.get('https://research.google.com/pubs/BrainTeam.html')
res.raise_for_status()

soup = beautifulsoup(res.text)
#titles = soup.find_all('p', class_="pub-title")
#pdfs = soup.find_all('a', href=True, class_="pdf-icon")
#print soup.prettify(), pdfs, titles, len(titles), len(pdfs)
undone_files = open("problem_links.txt",'a')
listings = soup.find_all('li')
for listing in listings:
    try:
        filename = str(listing.find('p', class_="pub-title").find('a').contents[0]).replace('\n','').replace(' ','').replace(',','').replace(':','_').replace('-','_')
        print filename
        link = listing.find('a', href=True, class_="pdf-icon").get('href')
        print link
        if link[0]=='/':
            url = baseurl + link
            res = requests.get(url)
            res.raise_for_status()
            print 'Downloading ..'
            pdf = open(os.path.join('brain',os.path.basename(filename+'.pdf')), 'wb')
            for chunk in res.iter_content(100000):
                pdf.write(chunk)
            pdf.close
            print filename + '\n done'
        else:
            undone_files.write(filename + '\n')
    except:
        continue
