from IPython import get_ipython
from IPython.display import display


!pip install nltk


!pip install newspaper3k


!pip install lxml_html_clean


from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt',quiet=True)


try:
    nltk.data.find('tokenizers/punkt_tab/english/')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


article = Article('https://my.clevelandclinic.org/health/diseases/15096-chronic-kidney-disease')
article.download()
article.parse()
article.nlp()
corpus=article.text



print(corpus)



text = corpus   #tokenization
sentence_list=nltk.sent_tokenize(text)# a list of sentence




print(sentence_list)  #print the list of sentence


# a function to return a random gretting  to the user
def greetting_response(text):
    text=text.lower()
    bot_greetings =['howdy' ,'hello', 'hi', 'hey','hola']
    User_greetings =['hi','hey','hello','whatssup']
    for word in text.split():
        if word in User_greetings:
            return random.choice(bot_greetings)




def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
          if x[list_index[i]]> x[list_index[j]]:
            temp = list_index[i]
            list_index[i] = list_index[j]
            list_index[j] = temp
    return list_index





    #bot response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)

    # Corrected the slicing syntax to get all indices except the first one
    index = index[1:]  # Get all elements from the second element onwards

    response_flag = 0

    j = 0
    # Looping through the sliced index list
    for i in range(len(index)):
        # Check if the similarity score for the current index is greater than 0
        if similarity_scores_list[index[i]] > 0.0:
            # Append the corresponding sentence to the bot response
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
            # If we have added 3 sentences, break the loop
            if j > 2:
                break

    # If no relevant sentences were found (response_flag is still 0)
    if response_flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I dont understand"

    # Remove the user input sentence from the list before returning the response
    sentence_list.remove(user_input)

    return bot_response





    #start the chat
print('Doc  : hey I am your doc today! ask me anything')
exit_list = ['exit', 'byee','see you again', 'break']
while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Doc : Bye Bye take care')
        break
    else:
        if greetting_response(user_input) != None:
            print('Doc : '+greetting_response(user_input))
        else:
            print('Doc : '+bot_response(user_input))

