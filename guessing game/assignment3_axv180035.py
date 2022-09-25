# Alarika Voora
# Assignment 3
# CS 4395

import sys, nltk, random, re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# driver function
def main():
    # checking that an argument is provided, exiting code if it is not
    if len(sys.argv) <= 1:
        print("sys arg not defined, please run again and specify location of csv file with data")
        exit()

    fp = open(sys.argv[1], 'r')  # open file
    rawText = fp.read()
    fp.close()  # close file
    tokens = [t.lower() for t in rawText.split()]
    uniqueTokens = set(tokens)
    print("** Lexical Diversity **")
    print("Lexical diversity: %.2f" % (len(uniqueTokens) / len(tokens)))

    resultingTokens, nouns = preProcess(tokens)

    # stem remaining tokens so affixes do not affect accurate counts
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(t) for t in resultingTokens]

    # populate nounCount dict of {noun: noun count}
    nounCount = {}
    for noun in nouns:
        count = stemmed.count(noun)
        nounCount[noun] = count

    # sort nounCount dict 
    res = list(sum(sorted(nounCount.items(), key = lambda x:x[1]), ()))
    ind = res[-100:]
    guessingList = []
    i = 0

    # create guessing game list
    print("\n** Top 50 Words **")
    print('%-5s %-20s %s' % ('rank' ,'word' , 'count'))
    while i < len(ind) - 1:
        print('%-5s %-20s %s' % ((50 - int (i/ 2)), ind[i], ind[i+1]))
        guessingList.append(ind[i])
        i+=2
    
    guessingGame(guessingList)  # run guessing game function 

# pre-processing function
def preProcess(tokens):
    resultingTokens = [t for t in tokens if t.isalpha() and
           t not in stopwords.words('english') and len(t) > 5]
    
    # lemmatizing words 
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    uniqueLemmas = set(lemmas)      # set of unique lemmas 
    tags = nltk.pos_tag(uniqueLemmas)   # pos tagging 
    print("\n** First 20 Tags **")
    print('', *tags[:20], sep='\n ')    # print first 20 tagged items 

    # list of nouns
    nouns =[]
    for token, pos in tags:
        if pos == 'NN' or pos == 'NNP':
            nouns.append(token)
    
    # print original number of tokens vs number of nouns 
    print("\n** Tokens vs Nouns **")
    print("Original Number of Tokens: ", len(tokens), "Number of Nouns: ", len(nouns))
    return resultingTokens, nouns

# guessing game function
def guessingGame(guessingList):
    print("\n** Guessing Game **")
    totalScore = 0      # original cumulative score is 0
    print("Let's play a guessing game!")
    while True:     
        score = 5       # score is originally 5 for this round 
        word = random.choice(guessingList)      # randomly choosing a word from guessing list
        currentList = ['-'] * len(word)
        guess = ''      #   inputted char
        guessSet = set()
        guessed = 0     # number of letters guessed
        while guessed < len(word) and score >= 0 and guess != '!': 
            print(*currentList)     # print current guessing state 
            
            # get guessing input and complete input validation 
            guess =  input('Guess a letter: ')
            while len(guess) != 1 and not guess.isalpha():    
                guess =  input('Invalid input, Guess a letter or type ! to end game: ')
                if guess == '!':        # exit game if ! 
                    print("Correct word is" ,word)
                    print("Final score: ", score)
                    exit()
            guess.lower()

            # find any and all instances of guessed character in word
            instances = [m.start() for m in re.finditer(guess, word)]

            # if the letter is found, populate the appropriate spaces with said letter
            if len(instances) > 0 and guess not in guessSet:
                score +=1
                print("Right! Score is ", score)
                guessed += len(instances)
                for i in instances:
                    currentList[i] = guess
                guessSet.add(guess)
            
            # else if the letter was already guessed
            elif guess in guessSet:  
                score -=1
                print("Sorry, letter already guessed. Score is ", score)

            # else subtract score by 1 
            else:
                score -=1
                guessSet.add(guess)
                if score < 0:
                    totalScore += score     # add round score to total score
                    if totalScore < 0:
                        print("\nScore" , totalScore , "below 0, better luck next time!")
                        print("Correct word is" ,word)
                        exit()
                    print("Score below 0, better luck next round!")
                    print("Correct word is" ,word)
                else:
                    print("Sorry, guess again. Score is ", score)

        # when word is successfully guessed
        if guessed == len(word):
            print(*currentList)
            print("You solved it!")

        totalScore += score     # add round score to total score
        if totalScore < 0:
            print("Your score" , totalScore , "is below 0, better luck next time!")
            exit()
        else:
            print("\nCurrent Score:", totalScore)

        # ask user if they would like to continue to the next round or end the game
        quit = input("press any key to continue, Q to quit: ")
        if quit == 'Q':
            print("\nYour final score is: ", score)
            exit()
        else:
            print("Guess another word")


if __name__ == "__main__":
    main()
