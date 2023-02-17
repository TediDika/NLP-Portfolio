import sys
import pathlib
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
from nltk.stem import WordNetLemmatizer




def preprocess(raw_text):
    # Uses a list comprehension to remove non alphas and make lower case
    tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
    # Remove stop words and words with length 5 or less
    removedStops = [t for t in tokens if t not in stopwords and len(t) > 5]
    # Lemmatizing tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in removedStops]
    uniqueLemmas = set(lemmatized)
    # POS Tagging
    tags = nltk.pos_tag(uniqueLemmas)
    print("\nFirst 20 tagged words: ", tags[:20])
    nounLemmas = [token for token, pos in tags if pos == 'NN']

    print("len of tokens after preprocessing ", len(removedStops))
    print("len of nouns after preprocessing ", len(nounLemmas))

    return removedStops, nounLemmas





if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: Please enter a filename as a system arg')
        quit()

    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read()
    tokenizedText = word_tokenize(text_in)

    print("\nThe number of tokens in text4: ", len(tokenizedText))
    set1 = set(tokenizedText)
    print("\nThe number of unique tokens in text4:", len(set1))
    # lexical diversity
    print("\nLexical diversity: %.2f" % (len(set1) / len(tokenizedText)))

    partATokens, nouns = preprocess(text_in)

    # Make a dictionary
    counts = {t:partATokens.count(t) for t in nouns}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("50 most common words:")
    listOfWords = []
    for i in range(50):
        print(sorted_counts[i])
        listOfWords.append(sorted_counts[i][0])

    # Guessing Game #
    print("Lets play a word guessing game!")
    PlayerPoints = 0
    while True:
        while PlayerPoints >= 0:
            

        print("Guess another word")






