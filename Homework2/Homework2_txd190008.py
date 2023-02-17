import re
import sys
import pathlib
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint
seed(1234)


def preprocess(raw_text):
    # Uses a list comprehension to remove non alphas and make lower case
    tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
    # Remove stop words and words with length 5 or less
    removedStops = [t for t in tokens if t not in stopwords and len(t) > 5]
    # Lemmatizing tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in removedStops]
    uniqueLemmas = set(lemmatized)
    # POS Tagging, uses regex to find POS that start with N to filter for nouns
    tags = nltk.pos_tag(uniqueLemmas)
    print("\nFirst 20 tagged words: ", tags[:20])
    nounLemmas = [token for token, pos in tags if re.match(r'^N', pos)]

    print("len of tokens after preprocessing", len(removedStops))
    print("len of nouns after preprocessing", len(nounLemmas))

    return removedStops, nounLemmas


def guessing_game(listOfWords):
    print("\nLets play a word guessing game!")
    TotalPoints = 5
    while True:
        RoundPoints = 5
        printList = []
        # Picks random word from top 50
        # Print list will be the length of the random word and filled with "_"
        randomWord = listOfWords[randint(0, 49)]
        for i in randomWord:
            printList.append("_")
            print('_', end=" ")
        while True:
            guess = input("\nGuess a letter:")
            # Game ends when "!" is input
            if guess == '!':
                print("\nGame Over!")
                quit()
            # When they guess letter correctly, add that letter to the print list
            if guess in randomWord:
                RoundPoints += 1
                print("Right! Score is", RoundPoints)
                for i in range(len(randomWord)):
                    if randomWord[i] == guess:
                        printList[i] = guess
            else:
                # When they guess incorrectly, decrement Round points
                # Round ends when Round points hits negative, Total points decrements
                RoundPoints -= 1
                if RoundPoints < 0:
                    TotalPoints -= 1
                    print("Oops, Round Over!")
                    print("\nCurrent score:", TotalPoints)
                    break
                else:
                    print("Sorry, guess again. Score is", RoundPoints)
            # Prints letters guessed correctly so far
            for i in printList:
                print(i, end=" ")
            # Round ends when they have guessed all letters, Round points is added to Total points
            if "_" not in printList:
                print("\nYou solved it!")
                TotalPoints += RoundPoints
                print("\nCurrent score:", TotalPoints)
                break
        # Game ends when Total points hits negative
        if TotalPoints < 0:
            break
        else:
            print("\nGuess another word")
    print("\nGame Over!")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: Please enter a filename as a system arg')
        quit()

    # OS file reading compatibility
    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read()

    # Calculate Lexical Diversity, # of unique tokens/total # of tokens
    tokenizedText = word_tokenize(text_in)
    set1 = set(tokenizedText)
    print("\nLexical diversity: %.2f" % (len(set1) / len(tokenizedText)))

    partATokens, nouns = preprocess(text_in)

    # Make a dictionary of {noun:count of noun in tokens} and print 50 most common words
    counts = {t:partATokens.count(t) for t in nouns}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("\n50 most common words:")
    listOfWords = []
    for i in range(50):
        print(sorted_counts[i])
        listOfWords.append(sorted_counts[i][0])

    guessing_game(listOfWords)