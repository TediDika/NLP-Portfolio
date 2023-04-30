import pickle
from nltk import word_tokenize
from nltk.util import ngrams
from pathlib import Path

# With our 'trained' language models, we can compute probabilities
# that test data is a part of one of these models using Laplace smoothing
def compute_prob(text, unigram_dict, bigram_dict, V):
    # V is the vocabulary size in the training data (unique tokens)

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

        p_laplace = p_laplace * ((b + 1) / (u + V))
    return p_laplace


if __name__ == '__main__':
        # Load in trained models created in program 1
        EngUnigram = pickle.load(open('english_unigram_dict.pickle', 'rb'))
        EngBigram = pickle.load(open('english_bigram_dict.pickle', 'rb'))

        FrenUnigram = pickle.load(open('french_unigram_dict.pickle', 'rb'))
        FrenBigram = pickle.load(open('french_bigram_dict.pickle', 'rb'))

        ItalUnigram = pickle.load(open('italian_unigram_dict.pickle', 'rb'))
        ItalBigram = pickle.load(open('italian_bigram_dict.pickle', 'rb'))

        V = len(EngUnigram) + len(FrenUnigram) + len(ItalUnigram)

        # Retrieving text from test file
        langid_filename = Path('data/LangId.test')
        text = open(langid_filename)
        text = text.read().splitlines()

        # Clearing out the output file before we write to it
        wordlangid_filename = Path('data/wordLangId.out')
        with open(wordlangid_filename, 'w') as file:
            pass

        file_line_count = 1
        my_solutions = []
        for line in text:
            EngProb = compute_prob(line, EngUnigram, EngBigram, V)
            FrenProb = compute_prob(line, FrenUnigram, FrenBigram, V)
            ItalProb = compute_prob(line, ItalUnigram, ItalBigram, V)

            # The language with the highest probability is appended to output file and solution list
            f = open(wordlangid_filename, 'a')
            if EngProb > FrenProb and EngProb > ItalProb:
                f.write(str(file_line_count) + " English\n")
                my_solutions.append(str(file_line_count) + " English")
            elif FrenProb > EngProb and FrenProb > ItalProb:
                f.write(str(file_line_count) + " French\n")
                my_solutions.append(str(file_line_count) + " French")
            else:
                f.write(str(file_line_count) + " Italian\n")
                my_solutions.append(str(file_line_count) + " Italian")
            file_line_count += 1

        # Computing accuracy by comparing my solutions with the actual solutions
        solution_filename = Path('data/LangId.sol')
        solution_file = open(solution_filename, 'r')
        solutions = solution_file.read().split('\n')
        correct_count = 0
        incorrect_lines = []
        for i in range(len(my_solutions)):
            if solutions[i] == my_solutions[i]:
                correct_count += 1
            else:
                incorrect_lines.append(my_solutions[i])

        print("Accuracy: %.2f" % + ((correct_count/len(my_solutions)) * 100) + "%")
        print("Line numbers that were incorrect: ", incorrect_lines)
