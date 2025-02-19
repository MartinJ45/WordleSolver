'''
author: @MartinJ45
'''
from fnmatch import fnmatch
from random import randrange

WORDLE_GUESSES = 5

def getBestGuess(possibleAnswers, guess):
    bestGuess = ""
    bestDifference = 0
    guess_ascii = sum([ord(letter) for letter in guess])
    for word in possibleAnswers:
        penalty = 0
        for i in range(len(word)):
            w = word
            letter = word[i]
            w = w[:i] + w[i+1:]
            if letter in w:
                penalty += 10

        word_ascii = sum([ord(letter) for letter in word])
        difference = abs(guess_ascii - word_ascii) - penalty
        if difference > bestDifference:
            bestDifference = difference
            bestGuess = word

    return bestGuess

def getPossibleAnswers(possibleAnswers, guess, result):
    yLetters = {}
    nLetters = []
    gLetters = []
    gToken = "?????"
    yToken = "?????"
    nToken = "?????"
    for i in range(len(guess)):
        match result[i]:
            case 'G':
                gLetters.append(guess[i])
                gToken = gToken[:i] + guess[i] + gToken[i+1:]
            case 'Y':
                if yLetters.get(guess[i]):
                    yLetters[guess[i]] += 1
                else:
                    yLetters[guess[i]] = 1
                yToken = yToken[:i] + guess[i] + yToken[i+1:]
            case 'N':
                nLetters.append(guess[i])
                nToken = nToken[:i] + guess[i] + nToken[i+1:]
    
    if yToken != "?????":
        for i in range(len(yToken)):
            token = "?????"
            if yToken[i] != '?':
                token = token[:i] + yToken[i] + token[i+1:]
                possibleAnswers = [word for word in possibleAnswers if not fnmatch(word, token)]
    
    if nToken != "?????":
        possibleAnswers = [word for word in possibleAnswers if not fnmatch(word, nToken)]
    
    newPossibleAnswers = []

    for word in possibleAnswers:
        isIncluded = True
        for letter in yLetters:
            if (yLetters[letter] + gLetters.count(letter)) > word.count(letter):
                isIncluded = False
        for letter in nLetters:
            if letter in word and not yLetters.get(letter) and letter not in gLetters:
                isIncluded = False
        if not fnmatch(word, gToken):
            isIncluded = False
        
        if isIncluded:
            newPossibleAnswers.append(word)

    return newPossibleAnswers

def main():
    with open("valid-wordle-words.txt", "r") as fValid:
        allValidWords = [line.strip('\n') for line in fValid.readlines()]
    fValid.close()

    '''
    There is no static list of answers for Wordle, but this list is a collection
    of frequent/past answers that the wordle will most likely be.
    '''
    with open("wordle-answers.txt", "r") as fAnswers:
        allAnswers = [line.strip('\n') for line in fAnswers.readlines()]
    fAnswers.close()

    possibleAnswers = allAnswers.copy()

    numGuesses = 0
    while numGuesses < WORDLE_GUESSES:
        guess = input("Input wordle guess: ")

        if guess in allValidWords:
            invalidInput = True
            while invalidInput:
                print("What was the result of your guess?")
                if numGuesses == 0:
                    print("G - green")
                    print("Y - yellow")
                    print("N - none")
                result = input()
                if len(result) == 5 and ('G' in result or 'Y' in result or 'N' in result):
                    if result == "GGGGG": 
                        print("You guessed the wordle!")
                        return
                    possibleAnswers = getPossibleAnswers(possibleAnswers, guess, result)

                    bestGuess = getBestGuess(possibleAnswers, guess)
                    if bestGuess == "":
                        bestGuess = possibleAnswers[randrange(len(possibleAnswers))]
                    print(f"You should guess:", bestGuess)

                    invalidInput = False

            numGuesses += 1
        else:
            print("Error: word not found in dictionary")

if __name__ == "__main__":
    main()
