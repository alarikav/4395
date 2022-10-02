## Alarika Voora 
## Oct, 2, 2022
## NLP

from nltk.util import ngrams
from nltk import word_tokenize
import pickle

# function to calculate probability
# laplace smoothing is used 
def calculate_probability(line, unigram_dict, bigram_dict, v):
    unigrams_test = word_tokenize(line)
    bigrams_test = list(ngrams(unigrams_test, 2))
    
    p = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0     # frequency of bigram
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0     # frequency of unigram
        p = p * ((b + 1) / (u + v))

    return p        # return probability

# driver function 
def main():
    # opening pickle files
    english_unigram_dict = pickle.load(open('english_unigram_dict.p', 'rb'))
    english_bigram_dict = pickle.load(open('english_bigram_dict.p', 'rb'))
    french_unigram_dict = pickle.load(open('french_unigram_dict.p', 'rb'))
    french_bigram_dict = pickle.load(open('french_bigram_dict.p', 'rb'))
    italian_unigram_dict = pickle.load(open('italian_unigram_dict.p', 'rb'))
    italian_bigram_dict = pickle.load(open('italian_bigram_dict.p', 'rb'))

    # open test and solution files
    fp = open('/Users/alarikavoora/4395/ngrams/LangId.test', 'r')
    test = open('/Users/alarikavoora/4395/ngrams/LangId.sol.txt', 'r')
    # read test and solution files simultaniously 
    line = fp.readline()
    test_line = test.readline()

    incorrect = []  # list to keep track of incorrect numbers 
    v = len(english_unigram_dict) + len(french_unigram_dict) + len(italian_unigram_dict) 
    number = 0      # total number of test lines
    correct = 0     # number of correct lines
    while line:
        # probability english 
        p_en = calculate_probability(line, english_unigram_dict, english_bigram_dict, v)
        # probability french 
        p_fr = calculate_probability(line, french_unigram_dict, french_bigram_dict, v)
        # probability italian 
        p_it = calculate_probability(line, italian_unigram_dict, italian_bigram_dict, v)
        
        # get max of 3 language probabilities 
        maxi = max(p_en, p_fr, p_it)

        # check if test line matches calculated probability line
        if maxi is p_en and "English" in test_line:
            correct += 1 
        elif maxi is p_fr and "French" in test_line:
            correct += 1 
        elif maxi is p_it and "Italian" in test_line:
            correct += 1 
        else: 
            incorrect.append(number + 1)    # add to incorrect list, if match not found

        line = fp.readline()
        test_line = test.readline()
        number +=1

    # close files
    fp.close()  
    test.close()
    print("Accuracy: ", correct/number)     # print accuracy
    print("Incorrect: ", *incorrect)        # print incorrect line numbers 


if __name__ == "__main__":
    main()
