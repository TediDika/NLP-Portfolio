import openai
import spacy
import csv
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
from nltk.stem import WordNetLemmatizer

# Used to download dependencies, uncomment if needed
# nltk.download('book')
# nltk.download('omw-1.4')
# spacy.cli.download("en_core_web_sm")

openai.api_key = "Enter API Key Here"

messages = [
    {"role": "system", "content": "You are SweetBot, a dessert recipe chatbot. "
                                  "You will give the user recipes and instructions for making various desserts. "
                                  "Keep your responses brief. "},
]

# Sends API calls to the Open AI GPT-3.5 model then prints out response
def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print("SweetBot: " + reply)

# Perform NER on provided text and returns dict of words and their labels
def NER_comparison(all_txt):
    nlp = spacy.load('en_core_web_sm')
    NER = {}
    doc = nlp(all_txt)
    for ent in doc.ents:
        NER[ent.text] = ent.label_
    return NER

# NLTK processing and POS Tagging
def nltk_POS(raw_text):
    # Uses a list comprehension to remove non alphas and make lower case
    tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
    # Remove stop words and words with length 2 or less
    removedStops = [t for t in tokens if t not in stopwords and len(t) > 2]
    # Lemmatizing tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in removedStops]
    uniqueLemmas = set(lemmatized)
    # POS Tagging, uses regex to find POS that start with N to filter for nouns
    tags = nltk.pos_tag(uniqueLemmas)
    # print(tags)
    nounLemmas = [token for token, pos in tags if re.match(r'^N', pos)]

    return nounLemmas


if __name__ == '__main__':
    print('SweetBot: Hi there! I am SweetBot, a dessert recipe chatbot. What is your name?')
    name_input = input()
    ner = NER_comparison(name_input)

    # Keep asking user for name until valid input is entered
    # Uses NER to find a word with PERSON tag
    name = ''
    name_check = False
    while name_check is False:
        for text, label in ner.items():
            if label == 'PERSON':
                name_check = True
                name = text
                break
        if name_check is False:
            print('SweetBot: Sorry, I could not recognize a name. Please try to input it again.')
            name_input = input()
            ner = NER_comparison(name_input)
    # print(ner)

    # Load the user database from the csv file into a dictionary
    user_db = {}
    with open('user_model.csv', mode='r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            names = row['Name']
            allergies = row['Allergies']
            user_db[names] = allergies
    # print(user_db)

    # If user is in the database list their allergies and then prompt for dessert type
    if name in user_db:
        if user_db[name] != '':
            print('SweetBot: It\'s good to see you again, ' + name + '! You are allergic to ' + user_db[name] + '.')
        else:
            print('SweetBot: It\'s good to see you again, ' + name + '! You have no food allergies')

        # Loops indefinitely until quit is typed
        while True:
            print('SweetBot: What dessert would you like a recipe for?')
            dessert = input()
            if dessert.lower() == 'quit':
                break
            # Send request to GPT-3.5
            # If user has no allergies then we send a different request with no food restrictions
            if user_db[name] != '':
                chatbot(name + ' has requested a recipe for (' + dessert + '). If possible, find a recipe that excludes'
                                                                           ' the following food items: ' + user_db[
                            name])
            else:
                chatbot(name + ' has requested a recipe for (' + dessert + ').')
    # If new user, prompt for allergies, use NLTK POS Tagging to extract food items
    else:
        print('SweetBot: Hi there ' + name + "! Please list any foods you are allergic to or say \'None\'.")
        allergies_input = input()
        allergies_text = ''
        if allergies_input.lower() == 'none':
            pass
        else:
            nouns = nltk_POS(allergies_input)
            # print(nouns)
            for text in nouns:
                allergies_text += text + ', '

        # Add the new user and their allergies to the csv data model
        with open('user_model.csv', mode='a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csvfile.write('\n')
            csv_writer.writerow([name, allergies_text])

        while True:
            print('SweetBot: What dessert would you like a recipe for?')
            dessert = input()
            if dessert.lower() == 'quit':
                break

            if allergies_text != '':
                chatbot(
                    name + ' has requested a recipe for (' + dessert + '). If possible, find a recipe that excludes '
                                                                       'the following food items: ' + allergies_text)
            else:
                chatbot(name + ' has requested a recipe for (' + dessert + ').')
