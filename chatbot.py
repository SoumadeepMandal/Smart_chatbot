!pip install newspaper3k lxml[html_clean]

import random
import nltk
import numpy as np
from newspaper import Article
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings


warnings.filterwarnings('ignore')

varOcg = "chronic kidney disease expert assistant"

nltk.download('punkt')
nltk.download('wordnet')
# Download the punkt_tab resource which might be required by newspaper's nlp()
nltk.download('punkt_tab')


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def normalize(text):
    tokens = nltk.word_tokenize(text.lower())
    return ' '.join([lemmatizer.lemmatize(token) for token in tokens])

url = 'https://en.wikipedia.org/wiki/Kidney_disease'
article = Article(url)
article.download()
article.parse()
article.nlp()
corpus = article.text



sentence_list = nltk.sent_tokenize(corpus)



user_greetings = ['hi', 'hello', 'hey', 'whatsup', 'howdy', 'hola']
bot_greetings = ['Hello!', 'Hi there!', 'Hey!', 'Howdy!', 'Greetings!']

def greeting_response(text):
    for word in text.lower().split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    return None


exit_list = ['exit', 'bye', 'see you', 'break', 'quit']


fallbacks = [
    "I'm not sure I understand. Could you rephrase?",
    "Sorry, I didn't catch that. Ask something else about kidney disease.",
    "I can help with symptoms, causes, or treatment. Try asking something specific."
]








def bot_response(user_input):
    user_input = normalize(user_input)
    sentence_list.append(user_input)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentence_list)
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    similarity_scores_list = similarity_scores.flatten()
    index_scores = similarity_scores_list.argsort()[::-1]

    response = ''
    response_found = False
    added = 0

    for index in index_scores:
        if index != len(sentence_list) - 1 and similarity_scores_list[index] > 0:
            response += sentence_list[index] + ' '
            response_found = True
            added += 1
        if added >= 2:
            break

    sentence_list.pop()

    if not response_found:
        return random.choice(fallbacks)
    return response.strip()




print("Doc 🤖: Hi! I'm your health assistant. Ask me anything about chronic kidney disease. Type 'exit' to leave.")

while True:
    user_input = input("You: ")
    if any(exit_word in user_input.lower() for exit_word in exit_list):
        print("Doc 🤖: Bye! Take care.")
        break
    elif greeting_response(user_input):
        print("Doc 🤖:", greeting_response(user_input))
    else:
        print("Doc 🤖:", bot_response(user_input))





