from fnmatch import fnmatch

WORDLE_GUESSES = 5

def updatePossibleAnswers(possibleAnswers, guess, result):
    yLetters = []
    nLetters = []
    gToken = "?????"
    yToken = "?????"
    for i in range(len(guess)):
        match result[i]:
            case 'G':
                gToken = gToken[:i] + guess[i] + gToken[i+1:]
            case 'Y':
                yLetters.append(guess[i])
                yToken = yToken[:i] + guess[i] + yToken[i+1:]
            case 'N':
                nLetters.append(guess[i])
    
    if yToken != "?????":
        possibleAnswers = [word for word in possibleAnswers if not fnmatch(word, yToken)]
    
    newPossibleAnswers = []
    for word in possibleAnswers:
        if all(letter in word for letter in yLetters) and \
            all(letter not in word for letter in nLetters) and \
            fnmatch(word, gToken):
            newPossibleAnswers.append(word)

    return newPossibleAnswers

def main():
    with open("valid-wordle-words.txt", "r") as fValid:
        allValidWords = [line.strip('\n') for line in fValid.readlines()]
    fValid.close()

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
                    possibleAnswers = updatePossibleAnswers(possibleAnswers, guess, result)
                    print("You should guess:", possibleAnswers[0])

                    invalidInput = False

            numGuesses += 1
        else:
            print("Error: word not found in dictionary")

if __name__ == "__main__":
    main()
