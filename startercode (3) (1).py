from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""
consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p',
    'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}


def readDictionaryFile():
    global dictionary
    opendictionary = open(dictionaryloc)
    readdictionary = opendictionary.read().splitlines()
    dictionary = readdictionary
    
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
      
    
def readTurnTxtFile():
    global turntext   
    openturntext = open(turntextloc)
    turntext = openturntext.read()
    #read in turn intial turn status "message" from file

        
def readFinalRoundTxtFile():
    global finalroundtext   
    openfinalround = open(finalRoundTextLoc)
    finalroundtext = openfinalround.read()
    #read in turn intial turn status "message" from file

def readRoundStatusTxtFile():
    global roundstatus
    openroundstatus = open(roundstatusloc)
    roundstatus = openroundstatus.read()
    # read the round status  the Config roundstatusloc file location 

def readWheelTxtFile():
    global wheellist
    openwheellist = open(wheeltextloc)
    readwheellist = openwheellist.read().splitlines()
    wheellist = readwheellist
    # read the Wheel name from input using the Config wheelloc file location 
    
def getPlayerInfo():
    global players
    fillname = False
    for i in range (0,len(players)):
        while (not fillname):
            playername = input(str(f"Please enter name for player {i + 1}:"))
            players[i]['name'] = playername
            i += 1
            if (i ==3):
                fillname = True
    # read in player names from command prompt input


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    roundUnderscoreWord = []
    blank = "_"
    roundWord = random.choice(dictionary)
    for i in range (0,len(roundWord)):
        roundUnderscoreWord.append(blank)
    #choose random word from dictionary
    #make a list of the word with underscores instead of letters.
    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    for i in range(0,len(players)):
        players[i]["roundtotal"] = 0
    initPlayer = random.choice([0,len(players)])
    roundWord, blankWord = getWord()
    # Return the starting player number (random)
    # Use getWord function to retrieve the word and the underscore word (blankWord)

    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels

    num = random.randint(0,len(wheellist)-1)
    stillinTurn = True
    wheelspin = wheellist[num]
    if(wheelspin == 'BANKRUPT'):
        print("The result is BANKRUPT. Nice going, now your round total is 0.")
        players[playerNum]["roundtotal"] = 0
        stillinTurn = False
    elif(wheelspin == "LOSE A TURN"):
        print("The wheel landed on LOSE A TURN. Nice try, you'll get em on the next one.")
        stillinTunr = False
    else:
        wheelspin.isdigit() == True
        vowelguess = True
        print(f"You landed on {wheelspin}!")
        while vowelguess:
            letter = input(str(f"For ${wheelspin}, please guess a letter:"))
            if letter in vowels:
                print("You may only guess a consonant")
            elif letter in consonants:
                vowelguess = False
        goodGuess, count = guessletter(letter, playerNum)
        if goodGuess == True:
            players[playerNum]["roundtotal"] += int(wheelspin)
            print(f"You have guessed correctly and earned ${wheelspin}!")
            stillinTurn = True
           
        else:
            print("Nice try but incorrect!")
            stillinTurn = False
           
    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.     
    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global blankWord
    count = 0
    goodGuess = False
    for i in range(0,len(roundWord)):
        if letter == roundWord[i]:
            blankWord[i] = letter
            count = roundWord.count(letter)
            goodGuess = True
    print(blankWord)        
    print(f"You have guessed correctly. The letter {letter} occurs {count} times!") 
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    global consonants
    goodGuess = False
    if players[playerNum]["roundtotal"] >= vowelcost:
        print(f"You have enough money to buy a vowel! Vowels cost $250.")
        vowelpurchase = input("Enter vowel:")
        while not goodGuess:
            if vowelpurchase in consonants:
                print("That is not a vowel. Try again.")
            elif vowelpurchase in vowels:
                players[playerNum]['roundtotal'] -= vowelcost
                goodGuess = True
                break
        goodGuess, Count = guessletter(vowelpurchase, playerNum)

    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    print(f"Here is the word: {blankWord}")
    word = input("Enter a word:")
    if word == roundWord:
        for i in range (len(roundWord)):
            if word == roundWord:
                players[playerNum]["gametotal"] = players[playerNum]["roundtotal"]
                blankWord = roundWord
    else:
        print("Incorrect answer sorry!")

    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    readRoundStatusTxtFile()
    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    stillinTurn = True
    while stillinTurn:
        if '_' not in blankWord:
            stillinTurn = False
            break
        choice = input("Enter 'S' to spin the wheel \nEnter 'B' to buy a vowel \nEnter 'G' to guess the word")
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    roundplayer = initPlayer
    round = True
    while round:
        round = wofTurn(roundplayer)
        if round == False:
            break
        if roundplayer > 2:
            roundplayer = 0
        else:
            roundplayer += 1
    print(roundstatus.format(word=roundWord, name=players[roundplayer]["name"]))
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    for i in players.keys():
        if players[i]["gametotal"] > players[winplayer]["gametotal"]:
            winplayer = i
    print(finalroundtext.format(name = players[winplayer]['name'], bank = amount))
    print(f"For the final round {players[winplayer]['name']} must guess one last word with the letters R, S, T, L, N, E given for FREE.") 
    print("Also we will give 3 consonants and a vowel for free as well!")
    roundWord, blankWord = getWord()
    freeletters = ["R", "S", "T", "L", "N", "E"]
    for j in freeletters:
        guessletter(j, winplayer)
    print(f"Here is your word to guess with the free letters:",blankWord)
    
    finalguesses = []
    firstconsonant = input("First consonant guess:")
    secconsonant = input("Second consonant guess:")
    thirdconsonant = input("Third consonant guess:")
    firstvowel = input("Vowel guess:")

    finalguesses.append(firstconsonant)
    finalguesses.append(secconsonant)
    finalguesses.append(thirdconsonant)
    finalguesses.append(firstvowel)
    guessWord(winplayer)
    if "_" not in blankWord:
        print(f"YOU HAVE WON! The correct word was {roundWord}!")
        players[winplayer["gametotal"]] += 100000
        print(f"{players[winplayer]['name']} has won {players[winplayer]['gametotal']} dollars!")
    else:
        print(f"GAME OVER. The word was {roundWord}.")
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won 


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
