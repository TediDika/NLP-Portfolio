from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from pathlib import Path
import pickle

'''
Extracts unigrams and bigrams from training file
and creates dictionaries which contain the
frequency of each unigram/bigram
'''
def make_bigram_unigram(filename):
    file = open(filename, "r", encoding = 'utf-8')
    text = file.read()
    processed_text = text.replace('\n', ' ')

    unigrams = word_tokenize(processed_text)
    bigrams = list(ngrams(unigrams, 2))
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}
    
    return bigram_dict, unigram_dict

'''
Calls 'make_bigram_unigram' function for each
training file to extract the unigram/bigram dicts
which the function returns. The dicts are then 
pickled to be used in program2.
'''
if __name__ == '__main__':
    # Ensures compatibility with different OS's
    english_filename = Path('data/LangId.train.English')
    french_filename = Path('data/LangId.train.French')
    italian_filename = Path('data/LangId.train.Italian')

    english_bigram_dict, english_unigram_dict = make_bigram_unigram(english_filename)
    french_bigram_dict, french_unigram_dict = make_bigram_unigram(french_filename)
    italian_bigram_dict, italian_unigram_dict = make_bigram_unigram(italian_filename)


    with open('english_bigram_dict.pickle', 'wb') as file:
        pickle.dump(english_bigram_dict, file)

    with open('english_unigram_dict.pickle', 'wb') as file:
        pickle.dump(english_unigram_dict, file)

    with open('french_bigram_dict.pickle', 'wb') as file:
        pickle.dump(french_bigram_dict, file)

    with open('french_unigram_dict.pickle', 'wb') as file:
        pickle.dump(french_unigram_dict, file)

    with open('italian_bigram_dict.pickle', 'wb') as file:
        pickle.dump(italian_bigram_dict, file)

    with open('italian_unigram_dict.pickle', 'wb') as file:
        pickle.dump(italian_unigram_dict, file)