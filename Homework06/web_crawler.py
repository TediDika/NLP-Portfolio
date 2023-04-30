# Tedi Dika
# txd190008

import pathlib
import nltk
import requests
import re
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pickle


# Crawls through starter page and extracts max of 15 links
def web_crawl():
    starter_url = 'https://en.wikipedia.org/wiki/Attack_on_Titan_(TV_series)'
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    # Puts all found urls into list
    url_list = []
    for link in soup.find_all('a'):
        if len(url_list) > 14:
            break
        # Filters links for relevant terms
        link_str = str(link.get('href'))
        if 'Titan' in link_str or 'titan' in link_str and 'manga' not in link_str and 'archive' not in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if 'wikipedia' in link_str and 'en' not in link_str:
                pass
            elif link_str.startswith('http') and 'google' not in link_str:
                url_list.append(link_str)
                print(link_str)
    # end of program
    print("end of crawler")
    return url_list

# Scrapes text off of provided links and then stores them into text files
def scrape_page(urls):
    counter = 1
    for url in urls:
        page = requests.get(url)
        file = open(('text' + str(counter) + '.txt'), 'w', encoding="utf-8")
        soup = BeautifulSoup(page.content, 'html.parser')

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        for p in soup.select('p'):
            file.write(p.get_text() + '\n')

        counter += 1
    print("end of scraper")


# Reads in previously created text files, cleans them up, and outputs new text files
def clean_text(urls):
    counter = 1
    for url in urls:
        with open(('text' + str(counter) + '.txt'), 'r', encoding="utf-8") as page:
            text = page.read()

        # Delete newlines and tabs first
        no_tabs = re.sub('\s+', ' ', text)
        #  Extract sentences with NLTK’s sentence tokenizer
        sentences = sent_tokenize(no_tabs)
        # Write the sentences for each file to a new file
        with open(('clean' + str(counter) + '.txt'), 'w', encoding="utf-8") as cleaned_text:
            for sentence in sentences:
                cleaned_text.write(sentence + '\n')
        counter += 1

    print("end of cleaner")

# Output top 25 words based on tf, then create a knowledge base manually
def important_terms(urls):
    # Combine text from all cleaned files
    combined_text = ""
    counter = 1
    for url in urls:
        with open(('clean' + str(counter) + '.txt'), 'r', encoding="utf-8") as page:
            text = page.read()
        combined_text += text
        counter += 1

    # Extract all tokens, make text lowercase and remove non alphas and stop words
    tokens = word_tokenize(combined_text)
    tokens = [t.lower() for t in word_tokenize(combined_text) if t.isalpha()]
    stop_words = stopwords.words('english')
    tokens = [token for token in tokens if token not in stop_words]

    # Creating tf dict, get term frequencies
    tf_dict = {}
    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # Normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    # Sort by highest occurring words and print
    sorted_tf = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    print('\nTop 25 terms using tf:')
    for i in range(25):
        print(sorted_tf[i])

    # Knowledge Base Creation
    top_10 = {'anime': [], 'attack': [], 'titan': [], 'season': [], 'film': [], 'theme': [], 'funimation': [],
              'isayama': [], 'eren': [], 'television': []}

    sentences = sent_tokenize(combined_text.lower())
    # Iterate through every sentence in the text extracted from the hyperlinks.
    # If the word was in the sentence, add that sentence to the respective term’s array in the dictionary.
    for sentence in sentences:
        for key, value in top_10.items():
            if key in sentence:
                value.append(sentence)

    # Print out knowledge base
    print("\nFirst five sentences contained for each term in the Knowledge Base:\n")
    for key, value in top_10.items():
        print(key + ":")
        for i in range(0, 5):
            print(value[i] + "\t")
        print("")

    # Pickle the knowledge base
    pickle.dump(top_10, open('top_10.pickle', 'wb'))


if __name__ == '__main__':
    url_list = web_crawl()
    scrape_page(url_list)
    clean_text(url_list)
    important_terms(url_list)
