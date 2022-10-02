## Alarika Voora 
## Oct, 2, 2022
## NLP

from nltk import word_tokenize
from nltk.util import ngrams
import pickle

# function to create each language model
def model(filename):
    fp = open(filename, 'r')  # open file
    rawtext = fp.read()     # read in file as raw text 
    fp.close()      # close file 
    rawtext.replace('\n', ' ')      # remove new lines
    tokens = word_tokenize(rawtext)   # tokenize 

    # unigrams 
    unigrams = list(tokens)     # list of unigrams
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)} # dict of (unigram) : count

    # bigrams 
    bigrams = list(ngrams(tokens, 2))      # list of bigrams
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}    # dict of (bigram) : count

    return unigram_dict, bigram_dict

# driver function 
def main():
    english_unigram_dict, english_bigram_dict,  = model('/Users/alarikavoora/4395/ngrams/LangId.train.English')
    french_unigram_dict,french_bigram_dict = model('/Users/alarikavoora/4395/ngrams/LangId.train.French')
    italian_unigram_dict,italian_bigram_dict = model('/Users/alarikavoora/4395/ngrams/LangId.train.Italian')

    # write to pickle files 
    pickle.dump(english_unigram_dict, open('english_unigram_dict.p', 'wb'))
    pickle.dump(english_bigram_dict, open('english_bigram_dict.p', 'wb'))
    pickle.dump(french_unigram_dict, open('french_unigram_dict.p', 'wb'))
    pickle.dump(french_bigram_dict, open('french_bigram_dict.p', 'wb'))
    pickle.dump(italian_unigram_dict, open('italian_unigram_dict.p', 'wb'))
    pickle.dump(italian_bigram_dict, open('italian_bigram_dict.p', 'wb'))



if __name__ == "__main__":
    main()
