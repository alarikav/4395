# Alarika Voora 

from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import certifi
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from collections import Counter

# scrapes URLs from starting sites
def create_url(urls):
    final_url_list = set()      # set ensures all URLs are unique
    i = 0
    
    while i < len(urls) and len(final_url_list) < 17:       # 17 URLs to accomodate for possible invalid URLs
        url = urls[i]
        r = requests.get(url)       
        data = r.text 
        soup = BeautifulSoup(data, "html.parser")   # using the Beautiful Soup html parser 
        counter = 0
        
        for link in soup.find_all('a'):     # finding all a tags
            string = str(link.get('href'))  # getting link from a tag
            # filtering sites to make sure only relevant URLs are included
            if ("http://" in string or "https://" in string) and "uber" in string and string not in final_url_list and "facebook" not in string and "twitter" not in string and "bloomberg" not in string and "uber." not in string: 
                urls.append(string)
                final_url_list.add(string)
                if counter > 6:     # to ensure all 15 URLs do not come from the same site 
                    break
                counter += 1
        i+=1
    
    return final_url_list

# creating text files with unfiltered URL content 
def create_text_files(final_url_list):
    counter = 0 
    
    # using a try - except block to accomodate for invalid URLs
    for url in final_url_list:
        try:
            html = urllib.request.urlopen(url,cafile=certifi.where())
        except URLError as e:
            print("invalid URL", url)
            continue
        
        with open(str(counter) + '.txt', 'w') as f:
            soup = BeautifulSoup(html, "html.parser")    # using the Beautiful Soup html parser 
            data = soup.findAll(text=True)  # getting all text data
            result = filter(visible, data)  # getting all visible components on page
            file_content_list = list(result)      # list from filter
            file_content = ' '.join(file_content_list)  # creating a string of all file content 
            f.write(file_content)
            counter +=1

# filtering and cleaning text files. 
def clean_text_files():
    counter = 15    # only using 15 files from the list 
    file_list = []  # list of files for next function 

    while counter >= 0:     # count down from 15 to 0
        with open(str(counter)+'.txt', 'r') as f:   # read from old text files
            text = f.read()
        sentences = sent_tokenize(text)     # tokenizing sentences
        
        if len(sentences) < 1:      # disregarding empty files
            continue
        new_sentences  = []     # list for sentences without tabs and spacing 
        for sentence in sentences:
            new_sentences.append(re.sub('\s+',' ',sentence))    # using regex to remove extra spacing
        
        with open(str(counter) + 'new.txt', 'w') as f:          # writing new sentences to new text files
            file_list.append(str(counter) + 'new.txt')
            f.write('\n'.join(new_sentences))
        counter -=1

    return file_list

# finding most the frequent words from the new text files
def find_most_frequent_words(file_list):
    frequency_counter = Counter([""])  # counter for frequency
    for file in file_list:      # file list from clean_text_files function
        with open(file, 'r') as f:
            text = f.read()
        tokens = word_tokenize(text)   # tokenize sentences from file
        # lowercase after removing punctuation and stopwords
        resultingTokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords.words('english')]
        frequency_counter += Counter(resultingTokens)   # adding frequency of current file to the frequency_counter 
    
    # print top 40 words
    for key, value in frequency_counter.most_common(40):
        print(key, value) 

    return frequency_counter

# helper function to check if html component is a visible one
def visible(element):
    # if meta data, return false
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']: 
        return False

    # if comment, return false
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    
    return True

# driver function 
def main():
    # starter urls for web crawler
    starter_url = "https://www.wired.com/story/uber-joe-sullivan-conviction/"
    starter_url2 = "https://techcrunch.com/2022/10/06/ubers-former-security-chief-found-guilty-of-covering-up-2016-data-breach/"
    
    # create url list to scrape 
    starter_urls = [starter_url, starter_url2]
    final_url_list = create_url(starter_urls)

    # create text files with original text from site 
    create_text_files(final_url_list)

    # clean original text files and create new file list
    file_list = clean_text_files()

    # create frequency counter for all files
    find_most_frequent_words(file_list)
    
    # manually selected words from 40 most frequent list
    selected_words = ["uber", "data", "security", "breach", "company", "privacy", "information", "hackers", "personal", "million"]
    print("******selected words******\n", "\n".join(selected_words))
    
    # knowledge base 
    # key : value -> term : fact
    knowledge_base = {"uber": "Over the past 5 years, uber had a number of encounters with hackers and law enforcement", "data": "A lot of customer data has been compromised in the Uber Data Breach", "security": "Proper security procedures are not followed at Uber", "breach": "Uber had a major security breach Earlier this year in September." , "company": "A lot of companies have been under fire for hackers, the most recent of which is Uber.", "privacy": "Customer privacy has been compromised at Uber.", "information": "The breach saw 57 million user's information including full names, email addresses, telephone numbers and driver's license numbers exposed.", "hackers" : "Uber paid the hackers $100,000 in Bitcoin in December 2016, despite not knowing their true identities to cover up the incident." , "personal": "Confidential personal information was leaked in the breach including sensitive information such as Drivers License Numbers", "million" : "Hackers stole the personal information of some 57 million customers and drivers."}
    for key, value in knowledge_base.items():
        print("Selected Word:", key.capitalize(), "\tFact:", value)


if __name__ == "__main__":
    main()
