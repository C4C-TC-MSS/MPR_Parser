from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import io
import re


# Set the browser in headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# open the chrome web browser
full_urls = []
driver = webdriver.Chrome("/Users/MellynDS/projects/chromedriver", chrome_options=options)
base_url = 'https://laws-lois.justice.gc.ca/eng/regulations/sor-2007-115/FullText.html'


driver.get(base_url)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Definitions
definitions = open("txt/definitions.txt", "w")
for dd in soup.findAll('dd'):
    definedTerm = dd.find('span', class_='DefinedTerm')
    if definedTerm is not None:
        word = definedTerm.get_text()
        definition = dd.get_text().replace(word, '').strip()
        definitions.write(word)
        definitions.write('\r\n')
        definitions.write(definition.encode('utf8', 'replace'))
        definitions.write('\r\n')
        definitions.write('\r\n')
definitions.close()

# Certificates
certificates = open("txt/certificates.txt", "w")
for certificateLetter in soup.find_all("a", id=lambda value: value and value.startswith("s-100p")):
    # TODO: Split out the (a) so we can grab the titles of certificates for later
    certificateName = certificateLetter.previous_element.get_text()
    certificateName = certificateName.encode('utf-8').replace(';','').replace("\xc2\xa0", " ").replace('.','')
    certificateName = re.sub(' and$', '', certificateName).strip()
    certificateNameSplit = certificateName.split(' ')
    certificateNameParts = certificateNameSplit[1:]
    certificateName = ' '.join(certificateNameParts).strip().replace('\r\n', '')
    certificates.write(certificateName)
    certificates.write('\r\n')

certificates.close()

# List of functions possibly put them in their own files at some point
def clean_html_certificate_header(header):
    return header.strip().replace('\r\n', '').encode('utf-8').replace("\xc2\xa0", " ")

def repeat_character(character, times):
    string_character = character
    for i in range(0, times):
        string_character += character
    print(string_character)

def parse_certificate_information(certificateName, html):
    hasData = False
    repeat_character('=', 70)
    print(certificateName)
    repeat_character('-', 70)

    for CertificatesList in soup.find_all("h4", text=lambda value: value and clean_html_certificate_header(value).startswith(certificateName)):    
        hasData = False
        if CertificatesList.next_sibling.find('table') is not None:
            for tableRow in CertificatesList.next_sibling.find('table').find_all('tr'):
                for tableData in tableRow.find_all('td'):
                    print (tableData.get_text())
                #print ('\r\n')
                hasData = True
        else:
            for tableRow in CertificatesList.next_sibling.next_sibling.find('table').find_all('tr'):
                for tableData in tableRow.find_all('td'):
                    print (tableData.get_text())
                #print ('\r\n')  
                hasData = True
    if not hasData:
        print('no data found')
    repeat_character('=', 70)

# Certificate Requirements

certificateNames = open("txt/certificates.txt", "r")
lines = certificateNames.readlines() 
for line in lines: 
    hasData = False
    parse_certificate_information(line.replace('\r\n', ''), soup)
certificateNames.close()
