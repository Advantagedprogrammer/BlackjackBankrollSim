import random
import time
import math
import sys
sys.setrecursionlimit(200000)  # make this big enough so we can run the sim
cansplit = 1
multiplehandtotals = []  # When player splits and has to stand on one hand, hand total gets added here
multiplebettotals = []  # When player splits and has to stand on one hand, bet for that hand gets added here
canblackjack = 1  # by default this is 1 meaning yes, but if a player splits aces, they cannot get blackjack
playersplit = [0, 0]  # [x,y] x is what they split, y increases as they split more, signifying more hands to play.
acecount = 0  # how many aces the player has
dealeracecount = 0  # how many aces the dealer has
ogbankroll = 0  # how much bankroll originally entered in
bankroll = 0  # how much bankroll the player has
truecounttoplay = 0  # the minimum truecount the player will play and won't wong out.
minimumbet = 0  # the minimum bet used when TC is bellow 1
tc1 = 0  # Tcnumber is used to determine bet sized based on true count
tc2 = 0
tc3 = 0
tc4 = 0
tc5 = 0
tc6 = 0
numberofsims = 0  # the number of times a computer will run thru. 1 means that the computer will play untill it either
# loses all of its money or wins a certain amount of profit ($2000). used to calculate Risk of Ruin.
runningcount = 0  # the number calculated by HI LOW system of card counting
truecount = 0  # running count divded by the number of decks remaining
simstep = 0  # this is the stepper, it will increase once the player wins a profit of 2000, or loses all its money
playerhand = [0, 0]  # tuple to signify the cards in player's hand
dealerhand = [0, 0]  # tuple to signify the cards in dealer's hand.
cardinshoe = 0  # this is which card is ready to be dealt, it acts as a stepper to be used as in deck[cardinshoe]
bet = 0  # how much the comp is actually betting on the simulated hand, changes based on true count and bankroll.
ogbet = 0  # the original bet played at a hand, used when splitting and one hand's bet changes because DAS
canstand = 0  # if 1 it means the player is standing and can't take any more cards
candouble = 1  # if 1 it means the player can double
handtotal = 0  # used when player doesn't have an Ace, for the hard totals
deck = []  # creates and empty deck that will be filled with 6 decks in bankrollsim()
simwins = 0
simloss = 0
doubled = 0
simisdone = 0
profit = 0
hands = 0
handsToWin = []
handsToLose = []


def bankrollsim():  # Establishes how much the player will be betting, what the bankroll is etc and moves on to
    global ogbankroll
    global bankroll
    global tc1
    global tc2
    global tc3
    global tc4
    global tc5
    global tc6
    global truecounttoplay
    global minimumbet
    global numberofsims
    global deck
    global profit

    print("The rules: Whenever dealer has any 17 they stay. Blackjack pays 3 to 2. 6 decks per shoe.")
    print("Deck penetration: Only 2 decks are left before a shuffle. The player plays perfect basic Strategy. ")
    print("Risk of Ruin will be calculated after you answer the questions. Min simulations recommended is 5000")
    print("The more simulations you do the more time it will take")
    print("Money made per hour is calculated based off of a rate of 100 hands per hour.")
    bankroll = input("How much money do you have in your bankroll? ")
    profit = input("How much money do you want to profit by?")
    truecounttoplay = input("What is the minimum TC that you are willing to play? ")
    minimumbet = input("While you are playing, what is your minimum bet at negative True counts? ")
    tc1 = input(" At TC1 how much are you betting? ")
    tc2 = input(" At TC2 how much are you betting? ")
    tc3 = input(" At TC3 how much are you betting? ")
    tc4 = input(" At TC4 how much are you betting? ")
    tc5 = input(" At TC5 how much are you betting? ")
    tc6 = input(" At TC6 how much are you betting? ")
    numberofsims = input("How many simulations will you run? (recommended max 200) ")
    z = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "A", "A", "A", "A"]
    x = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "A", "A", "A", "A"]
    y = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "A", "A", "A", "A"]
    w = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "A", "A", "A", "A"]
    v = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "A", "A", "A", "A"]
    u = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "A", "A", "A", "A"]
    deck = []
    deck = (z + x + y + w + v + u)  # There are 6 * 52 cards per deck = 312 cards
    random.shuffle(deck)  # Shuffles the deck and sets deck to that newly shuffled deck
    # I have to convert the inputs up above into integers so that I can do comparisons between them in later code.
    bankroll = int(bankroll)
    ogbankroll = bankroll
    tc1 = int(tc1)
    tc2 = int(tc2)
    tc3 = int(tc3)
    tc4 = int(tc4)
    tc5 = int(tc5)
    tc6 = int(tc6)
    minimumbet = int(minimumbet)
    truecounttoplay = int(truecounttoplay)
    numberofsims = int(numberofsims)
    profit = int(profit)
    print("Calculating, Please Wait...")
    play()


def play():
    global simisdone
    global hands
    global handsToWin
    global handsToLose
    global profit
    global ogbankroll
    for n in range(numberofsims):
        simisdone = 0
        play1()
    simisdone = 1
    aa = len(handsToWin)
    bb = len(handsToLose)
    print("Sim Complete...")
    time.sleep(1)
    print("Sim Losses: ", simloss)
    print("Sim Wins: ", simwins)
    if simwins > 0:
        averagewins = sum(handsToWin)/len(handsToWin)
        winningperhour = (profit/(averagewins/100))
        print(" Average Hands played before profiting: ", averagewins)
        print("Average amount winning per hour, ", winningperhour)
    if simloss > 0:
        averagelose = sum(handsToLose) / len(handsToLose)
        loseperhour = (ogbankroll/(averagelose/100))
        print(" Average Hands played before losing: ", averagelose)
        print(" Average amount losing per hour, ", loseperhour)
    input("Press any key to exit")


def play1():
    global simisdone

    def playgame():
        global candouble
        global canstand
        global canblackjack
        global playersplit
        global truecount
        global truecounttoplay
        global simstep
        global numberofsims
        global bankroll
        global bet
        global playerhand
        global dealerhand
        global handtotal
        global cardinshoe
        global minimumbet
        global deck
        global runningcount
        global ogbet
        global doubled
        global cansplit
        global ogbankroll
        global cardinshoe
        global numberofsims
        global profit
        global multiplebettotals
        global multiplehandtotals
        multiplebettotals = []
        multiplehandtotals = []
        cansplit = 1
        doubled = 0
        ogbet = 0
        bet = 0
        canblackjack = 1
        playersplit = []
        handtotal = 0
        playerhand = []
        dealerhand = []
        candouble = 1
        canstand = 1
        if bankroll <= 0:  # just a double check to make sure the bankroll is greater than 0
            simlost()
        elif bankroll >= ogbankroll + profit:
            simwin()
        else:
            # elif simstep != numberofsims:  # This is the section of code in charge of the actual games.
            if cardinshoe >= 250:  # This means we have to shuffle, and so RC and TC are reset
                cardinshoe = 0
                runningcount = 0
                truecount = 0
                random.shuffle(deck)
                random.shuffle(deck)
                random.shuffle(deck)
                # print("shuffeling")
            if truecount < truecounttoplay - 1:  # Will shuffle if TC is too low
                cardinshoe = 0  # shuffles the deck resetting all the relevant info so we can count again.
                runningcount = 0
                truecount = 0
                random.shuffle(deck)
                random.shuffle(deck)
                random.shuffle(deck)
                # print("shuffeling")
            truecount = (runningcount / math.ceil(((312 - cardinshoe) / 52)))
            truecount = math.floor(truecount)
            if truecount >= truecounttoplay:  # If true the player will be betting something.
                if truecount <= 0 and bankroll >= minimumbet:  # This whole mess is making sure that the computer dont
                    bet = minimumbet  # bet more than it has in its bankroll and that if
                elif truecount <= 0 and bankroll <= minimumbet:  # the bet is supposed to be high and if there isn't enough
                    bet = bankroll  # then the computer will bet as much as it can, its remaining
                elif truecount == 1 and bankroll >= tc1:  # bankroll.
                    bet = tc1
                elif truecount == 1 and bankroll <= tc1:
                    bet = bankroll
                elif truecount == 2 and bankroll >= tc2:
                    bet = tc2
                elif truecount == 2 and bankroll <= tc2:
                    bet = bankroll
                elif truecount == 3 and bankroll >= tc3:
                    bet = tc3
                elif truecount == 3 and bankroll <= tc3:
                    bet = bankroll
                elif truecount == 4 and bankroll >= tc4:
                    bet = tc4
                elif truecount == 4 and bankroll <= tc4:
                    bet = bankroll
                elif truecount == 5 and bankroll >= tc5:
                    bet = tc5
                elif truecount == 5 and bankroll <= tc5:
                    bet = bankroll
                elif truecount >= 6 and bankroll >= tc6:
                    bet = tc6
                elif truecount >= 6 and bankroll <= tc6:
                    bet = bankroll
            else:
                bet = 0  # Wonging out
            playerhand = [deck[cardinshoe], deck[(cardinshoe + 2)]]  # Deals cards in order of IRL,
            dealerhand = [deck[(cardinshoe + 1)], deck[(cardinshoe + 3)]]
            cardinshoe = cardinshoe + 4  # Sets the next card in shoe to be ready to be taken
# TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# playerhand[0] = "A"  ########## THIS IS A TEST DELETE AFTER TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# playerhand[1] = "A"  ########## THIS IS A TEST DELETE AFTER TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# dealerhand[0] = 8
# dealerhand[1] = "A"
# TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# This section updates the running count based off the players hand, has to be updated when player hits/doubles.
            if playerhand[0] == "A":
                runningcount = runningcount - 1
            elif playerhand[0] <= 6:
                runningcount = runningcount + 1
            elif playerhand[0] == 10:
                runningcount = runningcount - 1
            if playerhand[1] == "A":
                runningcount = runningcount - 1
            elif playerhand[1] == 10:
                runningcount = runningcount - 1
            elif playerhand[1] <= 6:
                runningcount = runningcount + 1
# This section updates the exposed dealer card to the running count, remember to update it again for the 2nd card or [1]
            if dealerhand[0] == "A":
                runningcount = runningcount + -1
            elif dealerhand[0] == 10:
                runningcount = runningcount - 1
            elif dealerhand[0] <= 6:
                runningcount = runningcount + 1
            # print("got through 1st block")
            ogbet = bet
            howtoplay()  # Now the basic strategy function takes over to play the hand.

    def dealerhit():
        global dealerhand
        global runningcount
        global bet
        global bankroll
        global cardinshoe
        global deck
        # print("dealer's turn'")

        def dhit():
            global dealerhand
            global runningcount
            global bet
            global bankroll
            global cardinshoe
            global deck
            # print("dealers hand is ", dealerhand[0], " ", dealerhand[1])
            # This section deals with [A, something]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if dealerhand[0] == "A":
                if dealerhand[1] <= 5:  # this covers ranges 1 through 5
                    if deck[cardinshoe] == "A":  # If dealer hits an Ace
                        runningcount = runningcount - 1  # Update running count
                        dealerhand[1] = dealerhand[1] + 1  # a 2nd ace means add by one
                        # print("Dealer got an Ace")
                        cardinshoe = cardinshoe + 1
                        dhit()
                    elif deck[cardinshoe] <= 6:
                        runningcount = runningcount + 1
                        dealerhand[1] = dealerhand[1] + deck[cardinshoe]
                        # print("Dealer got a ", deck[cardinshoe])
                        cardinshoe = cardinshoe + 1
                        dhit()
                    elif deck[cardinshoe] == 10:
                        runningcount = runningcount - 1
                        dealerhand[1] = dealerhand[1] + deck[cardinshoe]
                        # print("dealer got a 10")
                        cardinshoe = cardinshoe + 1
                        dhit()
                    elif deck[cardinshoe] < 10:  # this range is 7, 8, 9,
                        dealerhand[1] = dealerhand[1] + deck[cardinshoe]
                        # print("Dealer got a ", deck[cardinshoe])
                        cardinshoe = cardinshoe + 1
                        dhit()
                    else:
                        print("ERROR CODE 140")
                elif dealerhand[1] <= 10:  # This covers ranges 6 through 10
                    dealerstand()
                elif dealerhand[1] >= 21:  # This covers 21 through sideways 8
                    dealerbust()
                elif dealerhand[1] >= 16:
                    dealerhand = [1, dealerhand[1]]  # This covers ranges 16 through 20
                    dealerstand()
                elif dealerhand[1] <= 15:  # this covers ranges 11 through 15
                    if deck[cardinshoe] == "A":  # If dealer hits an Ace
                        runningcount = runningcount - 1  # Update running count
                        # print("dealer got an ace")
                        dealerhand[1] = dealerhand[1] + 1
                    elif deck[cardinshoe] <= 6:
                        runningcount = runningcount + 1
                        dealerhand[1] = dealerhand[1] + deck[cardinshoe]
                        # print("dealer got a ", deck[cardinshoe])
                    elif deck[cardinshoe] == 10:
                        runningcount = runningcount - 1
                        dealerhand[1] = dealerhand[1] + deck[cardinshoe]
                        # print("dealer got a ", deck[cardinshoe])
                    elif deck[cardinshoe] > 6:
                        dealerhand[1] = dealerhand[1] + deck[cardinshoe]
                        # print("dealer got a ", deck[cardinshoe])
                    else:
                        print("Else error: 164 ???")
                    cardinshoe = cardinshoe + 1
                    dhit()
            # End of [A, something] section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            elif dealerhand[0] + dealerhand[1] > 21:
                dealerbust()
            elif dealerhand[0] + dealerhand[1] >= 17:
                dealerstand()
            elif dealerhand[0] + dealerhand[1] < 17:  # dealer is hitting here
                dealerhand[1] = dealerhand[0] + dealerhand[1]
                dealerhand[0] = deck[cardinshoe]
                if deck[cardinshoe] == "A":  # Dealer hits an ace
                    runningcount = runningcount - 1
                elif deck[cardinshoe] <= 6:
                    runningcount = runningcount + 1
                elif deck[cardinshoe] == 10:
                    runningcount = runningcount - 1
                cardinshoe = cardinshoe + 1
                dhit()

        # This section exposes the other card and then also deals with [A, A]
        if dealerhand[1] == "A":
            runningcount = runningcount - 1
        elif dealerhand[1] == 10:
            runningcount = runningcount - 1
        elif dealerhand[1] <= 6:
            runningcount = runningcount + 1
        if dealerhand[0] == "A" and dealerhand[1] == "A":  # we turn the 2nd ace into +1
            dealerhand = [dealerhand[0], 1]  # It becomes [A, 1]
        elif dealerhand[1] == "A":
            dealerhand = [dealerhand[1], dealerhand[0]]  # reaarranges so it is A, something
        if dealerhand[0] == "A":
            if dealerhand[1] >= 6:
                if dealerhand[1] == 6:
                    dealerstand()
                elif dealerhand[1] == 10:
                    dealerstand()
                else:
                    dealerstand()
            elif dealerhand[1] == 1:
                dhit()
            elif dealerhand[1] < 6:
                dhit()
        elif dealerhand[1] <= 6:  # numbers 2 through 6
            if dealerhand[0] + dealerhand[1] > 21:
                print("Impossible Error 366")
                dealerbust()
            if dealerhand[0] + dealerhand[1] >= 17:
                dealerstand()
            else:
                dhit()
        elif dealerhand[1] == 10:  # number 10
            if dealerhand[0] + dealerhand[1] > 21:
                dealerbust()
            if dealerhand[0] + dealerhand[1] >= 17:
                dealerstand()
            else:
                dhit()
        elif dealerhand[1] < 10:  # numbers 7 through 9
            if dealerhand[0] + dealerhand[1] > 21:
                dealerbust()
            if dealerhand[0] + dealerhand[1] >= 17:
                dealerstand()
            else:
                dhit()
        else:
            print("error 231, dealer hit")

    def stand():
        global playerhand
        global playersplit
        global handtotal
        global dealerhand
        global bet
        global multiplehandtotals
        global ogbet
        global multiplebettotals
        global candouble
        global doubled
        # ogbet = bet I dont think this is right :/
        if playerhand[1] == "A":
            print("Something has gone terribly wrong... ERROR 391")
        if playerhand[0] == "A":  # If there is an ace at this point it has to be worth 11 otherwise it already is added +1
            handtotal = 11 + playerhand[1]
        else:
            handtotal = playerhand[0] + playerhand[1]
        if playersplit == []:
            # print("you stand on ", handtotal)
            dealerhit()
        elif playersplit[1] == 0:  # playersplit[1] if 0 means that there are no more split hands to play
            # print("you stand on ", handtotal)
            dealerhit()

        else:  # this means the player has more hands ( cuz of split) and we have to store his current hand in an array
            # print("Going to store it")
            if multiplehandtotals == []:
                multiplehandtotals = [handtotal]
            else:
                multiplehandtotals = multiplehandtotals + [handtotal]  # storing this hands total
            if multiplebettotals == []:
                multiplebettotals = [bet]
                # print("241")
            else:
                # print("242")
                multiplebettotals = multiplebettotals + [bet]  # Storing this bet's total
            if bankroll >= ogbet:  # make sure there is enough money to bet
                bet = ogbet  # Make sure that the next hand has the original bet since it is now new because of split
                playersplit[1] = playersplit[1] - 1  # Signifies that we are moving on to the next split hand
                playerhand = [playersplit[0], 0]
                # print("you stand on ", handtotal)
                # print("got more hands left")
                # print("Stored value", multiplebettotals[0])
                candouble = 1
                doubled = 0
                hit()
            else:  # If there isn't enough money to play the next hand you lose this sim.
                simlost()

    def hit():  # What happens when a player hits
        global playerhand
        global handtotal
        global deck
        global cardinshoe
        global bankroll
        global bet
        global runningcount
        global simstep
        global simwins
        global simloss
        global playersplit
        global candouble
        global canblackjack
        global doubled
        global cansplit
        # print("at hit")
        canblackjack = 0  # Whenever you hit, even if you are reciving a card for a split 10, you cannot get blackjack.
        # this section is when the player is coming to hit() after splitting a pair. if not true moves on to other code.~~~~~~
        if playerhand[1] == 0:  # When true it means we have just split and need a new card.
            playerhand[1] = deck[cardinshoe]
            cardinshoe = cardinshoe + 1  # sets up the next card in shoe.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Updates running count ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if playerhand[1] == "A":
                runningcount = runningcount - 1
            elif playerhand[1] == 10:
                runningcount = runningcount - 1
            elif playerhand[1] <= 6:
                runningcount = runningcount + 1
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if playerhand[0] == "A":
                candouble = 0  # You can't double after splitting aces
                howtoplay()
            else:
                # candouble = 1  unnecesary since we do this at split()
                howtoplay()
        # End of section about hitting after splits, next section is hitting after you haven't split~~~~~~~~~~~~~~~~~~~~~~~~~~
        # This next section is when you have to hit when you have a soft total EX: [A 5]
        elif playerhand[0] == "A":
            if deck[cardinshoe] == "A":  # if the next card drawn is an Ace add 1 too the soft total
                playerhand[1] = playerhand[1] + 1
                cardinshoe = cardinshoe + 1  # sets up next card in shoe
                runningcount = runningcount - 1  # updates running count
                if doubled == 0:
                    candouble = 0  # you can no longer double after hitting
                    cansplit = 0
                    howtoplay()
                else:  # if you came to hit from double, after hitting you must stand.
                    stand()

            elif deck[cardinshoe] <= 10:  # This next section sees if you have to turn the Ace into a 1 or not
                if deck[cardinshoe] + playerhand[1] + 11 > 21:  # if ace as 11 plus other cards would bust, turn into 1
                    playerhand = [1 + deck[cardinshoe], playerhand[1]]  # changes your hand where you now use ace as 1
                else:
                    playerhand[1] = deck[cardinshoe] + playerhand[1]
                if deck[cardinshoe] == 10:  # Updates running count ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    runningcount = runningcount - 1
                elif deck[cardinshoe] <= 6:
                    runningcount = runningcount + 1  # End of section updating running count~~~~~~~~~~~~~~~~~~~~~~~~~
                cardinshoe = cardinshoe + 1
                if doubled == 0:
                    candouble = 0  # You cannot double after you hit
                    cansplit = 0
                    howtoplay()
                else:  # if you came to hit from double, after hitting you must stand.
                    stand()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of Section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        else:  # this section is simple total EX: 7, 9
            handtotal = playerhand[0] + playerhand[1]
            playerhand = [handtotal, (deck[cardinshoe])]
            cardinshoe = cardinshoe + 1  # sets the next card to be ready to be dealt
            # updates running count based on what card the player just got dealt, which is in playerhand[1] as seen above
            if playerhand[1] == "A":
                runningcount = runningcount - 1
            elif playerhand[1] == 10:
                runningcount = runningcount - 1
            elif playerhand[1] <= 6:
                runningcount = runningcount + 1
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if playerhand[1] == "A":  # if the player gets an ace. Remember player will NEVER bust when hits and gets an ace
                playerhand = [playerhand[1], playerhand[0]]  # Rearranges, so it is Ace, number
                if playerhand[1] + 11 > 21:
                    playerhand = [1, playerhand[1]]
                    if doubled == 0:
                        candouble = 0
                        cansplit = 0
                        howtoplay()
                    else:
                        stand()  # If you came here from double() you have to stay
                else:
                    if doubled == 0:
                        candouble = 0
                        cansplit = 0
                        howtoplay()
                    else:
                        stand()  # If you came here from double() you have to stay
            elif playerhand[0] + playerhand[1] > 21:  # if the player busts
                bust()
            else:
                if doubled == 0:
                    candouble = 0
                    cansplit = 0
                    # print("you hit and now have ", playerhand[0], " ", playerhand[1])
                    howtoplay()
                else:
                    stand()  # If you came here from double() you have to stay

    # TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

    def simlost():
        global playersplit
        global truecount
        global bet
        global playerhand
        global dealerhand
        global handtotal
        global cardinshoe
        global deck
        global runningcount
        global simloss
        global simstep
        global bankroll
        global ogbankroll
        global simisdone
        global handsToLose
        global hands
        # clears the values for the next simulation
        playersplit = []
        bankroll = ogbankroll
        truecount = 0
        bet = 0
        playerhand = []
        dealerhand = []
        handtotal = 0
        cardinshoe = 0
        runningcount = 0
        random.shuffle(deck)  # Shuffles the deck multiple times to ensure randomness.
        random.shuffle(deck)
        random.shuffle(deck)
        random.shuffle(deck)
        # Updates the running total of sim lost and sim step
        simloss = simloss + 1
        simstep = simstep + 1
        if handsToLose == []:
            handsToLose = [hands]
        else:
            handsToLose = handsToLose + [hands]
        hands = 0
        simisdone = 1
        # print("SIM LOST")


    def simwin():
        global playersplit
        global truecount
        global bet
        global playerhand
        global dealerhand
        global handtotal
        global cardinshoe
        global deck
        global runningcount
        global simwins
        global simstep
        global bankroll
        global ogbankroll
        global simisdone
        global handsToWin
        global hands
        # Clears the values for the next simulation
        playersplit = 0
        bankroll = ogbankroll
        truecount = 0
        bet = 0
        playerhand = []
        dealerhand = []
        handtotal = 0
        cardinshoe = 0
        runningcount = 0
        random.shuffle(deck)  # Shuffles the deck multiple times to ensure randomness.
        random.shuffle(deck)
        random.shuffle(deck)
        random.shuffle(deck)
        # Updates the running total of sim wins and sim step
        simwins = simwins + 1
        simstep = simstep + 1
        if handsToWin == []:
            handsToWin = [hands]
        else:
            handsToWin = handsToWin + [hands]
        hands = 0
        simisdone = 1
        # print("SIMWIN")


    def double():
        global candouble
        global bet
        global doubled
        doubled = 1
        if candouble == 1:
            bet = bet * 2
            candouble = 0
            # print("double")
            hit()
        else:
            hit()

    def blackjack():
        global bankroll
        global bet
        global dealerhand
        global runningcount
        global hands
        if dealerhand[1] == "A":
            runningcount = runningcount - 1
        elif dealerhand[1] == 10:
            runningcount = runningcount - 1
        elif dealerhand[1] <= 6:
            runningcount = runningcount + 1
        # print("runningcount == ", runningcount)
        bet = 1.5 * bet
        bet = math.trunc(bet)
        bankroll = bankroll + bet
        hands = hands + 1

        # print("You won, ", bet)
        # print("bankrol is now, ", bankroll)
        # print("player has blackjack")
        # playgame()

    def dealerstand():
        global multiplehandtotals
        global dealerhand
        global playerhand
        global bet
        global bankroll
        global multiplebettotals
        global handtotal
        global runningcount
        global hands
        # print("dealer stands")
        # print(dealerhand[0], " ", dealerhand[1])
        # print("running count == ", runningcount)
        if dealerhand[0] == "A":
            dealerhand[0] = 11
        # The first section checks if we have to check multiple hands or if player only has 1 hand IE there was no splitting
        if multiplehandtotals == []:
            if handtotal == dealerhand[0] + dealerhand[1]:
                push()
            elif handtotal > dealerhand[0] + dealerhand[1]:
                # print("Player Wins an extra ", bet)
                hands = hands + 1
                bankroll = bankroll + bet
                # print("bankroll now equals ", bankroll)
                # playgame()
            else:
                # print("Dealer wins, lose ", " ", bet)
                hands = hands + 1
                bankroll = bankroll - bet
                # print("bankroll now equals ", bankroll)
                # playgame()
        # This next section is when the player has split and now we have to check each hand and bet and act accordingly
        else:
            if handtotal <= 21:
                if handtotal > dealerhand[0] + dealerhand[1]:
                    # print("You Win ", bet)
                    # print("bankroll = ", bankroll + bet)
                    bankroll = bankroll + bet
                elif handtotal == dealerhand[0] + dealerhand[1]:
                    agg = 0
                    # print("push for hand total ", handtotal)
                else:
                    # print("You lost ", bet)
                    # print("bankroll = ", bankroll - bet)
                    bankroll = bankroll - bet
            a = len(multiplehandtotals)
            for n in range(a):
                # if dealerhand[0] + dealerhand[1] == multiplehandtotals[n]:
                    # print("PUSH for hand ", multiplehandtotals[n])
                if dealerhand[0] + dealerhand[1] > multiplehandtotals[n]:
                    # print("Loss for hand ", multiplehandtotals[n])
                    # print("You LOST, ", multiplebettotals[n])
                    # print("bankroll = ", bankroll - multiplebettotals[n])
                    bankroll = bankroll - multiplebettotals[n]
                elif dealerhand[0] + dealerhand[1] < multiplehandtotals[n]:
                    # print("WIN for hand ", multiplehandtotals[n])
                    # print("You WON, ", multiplebettotals[n])
                    # print("bankroll = ", bankroll + multiplebettotals[n])
                    bankroll = bankroll + multiplebettotals[n]
            hands = hands + 1
            # print("Playgame() is next...")
            # print(bankroll)
            #playgame()

    def dealerbust():
        global multiplehandtotals
        global bet
        global bankroll
        global multiplebettotals
        global handtotal
        global hands
        # print("runningcount == ", runningcount)
        # print("Dealer Busts with: ")
        # print(dealerhand[0], " ", dealerhand[1])
        if multiplehandtotals == []:
            # print("WIN for hand ", handtotal)
            # print("You WON, ", bet)
            # print("bankroll = ", bankroll + bet)
            # print("Play Game next.")
            bankroll = bankroll + bet
            hands = hands + 1
            #playgame()
        elif multiplehandtotals[0] == 0:
            # print("WIN for hand ", handtotal)
            # print("You WON, ", bet)
            # print("bankroll = ", bankroll + bet)
            # print("Play Game next.")
            bankroll = bankroll + bet
            hands = hands + 1
            #playgame()
        else:  # This means we have several hands from splitting we must award.
            if handtotal <= 21:
                # print("You Win ", bet)
                # print("bankroll = ", bankroll + bet)
                bankroll = bankroll + bet
            a = len(multiplehandtotals)
            for n in range(a):
                # print("WIN for hand ", multiplehandtotals[n])
                # print("You WON, ", multiplebettotals[n])
                # print("bankroll = ", bankroll + multiplebettotals[n])
                bankroll = bankroll + multiplebettotals[n]
            hands = hands + 1
            # print(bankroll)
            # print("Play Game next.")
            #playgame()

    def dealerblackjack():
        global bankroll
        global bet
        global runningcount
        global hands
        runningcount = runningcount - 1  # update running count
        # print("dealer has blackjack")
        # print("runningcount == ", runningcount)
        # print(dealerhand[0], " ", dealerhand[1])
        bankroll = bankroll - bet
        hands = hands + 1
        # print("You Lost, ", bet)
        # print("Bankroll is now , ", bankroll)
        # print("playgame is next...")
        #playgame()

    def bust():
        global playersplit
        global bet
        global bankroll
        global multiplebettotals
        global multiplehandtotals
        global playerhand
        global candouble
        global doubled
        global runningcount
        global hands
        # print("runningcount == ", runningcount)
        if playersplit == []:  # checking if this is the end of the hand for player or if they have another hand off split
            bankroll = bankroll - bet
            if dealerhand[1] == "A":
                runningcount = runningcount - 1
            elif dealerhand[1] == 10:
                runningcount = runningcount -1
            elif dealerhand[1] <= 6:
                runningcount = runningcount + 1
            if bankroll <= 0:  # if you lost all your money
                # print("Simlost")
                hands = hands + 1
                simlost()
            else:
                # print("You busted")
                # print("You had", playerhand[0], " ", playerhand[1])
                # print(bankroll)
                #playgame()  # move on to the next game
                hands = hands + 1
        elif playersplit[1] == 0:  # this means playersplit and stand on the first card
            bankroll = bankroll - bet
            if bankroll <= 0:  # if you lost all your money
                # print("Simlost")
                hands = hands + 1
                simlost()
            elif multiplehandtotals == []:
                # print("bust")
                dealerhit()
                    # print("You lost this hand")
                    # print(bankroll)
                    #playgame()  # move on to the next game
                    #pg = 1
            else:
                if bankroll <= 0:  # if you lost all your money
                    # print("Simlost")
                    hands = hands + 1
                    simlost()
                # print("You busted with ", playerhand[0], " ", playerhand[1])
                # print(bankroll)
                dealerhit()
        else:
            # print("You busted but since you split you have more hands to play.")
            bankroll = bankroll - bet
            if bankroll <= 0:  # if you lost all your money
                # print("Simlost")
                hands = hands + 1
                simlost()
            # print("bankroll is now ", bankroll)
            elif bankroll >= ogbet:  # make sure there is enough money to bet
                bet = ogbet  # Make sure that the next hand has the original bet since it is now new because of split
                playersplit[1] = playersplit[1] - 1  # Signifies that we are moving on to the next split hand
                # print("you busted on ", playerhand[0], " ", playerhand[1])
                # print("got more hands left")
                playerhand = [playersplit[0], 0]
                candouble = 1
                doubled = 0
                hit()
            else:  # If there isn't enough money to play the next hand you lose this sim.
                hands = hands + 1
                simlost()

    def split():
        global truecount
        global runningcount
        global cardinshoe
        global dealerhand
        global playersplit
        global canblackjack
        global bankroll
        global ogbet
        global candouble
        global multiplebettotals
        global cansplit
        candouble = 1
        cansplit = 1
        # print("players plitting")
        if playersplit == []:
            playersplit = [playerhand[0], 1]  # x, shows what is being split, y is extra hands to play
        else:
            playersplit = [playerhand[0], playersplit[1] + 1]
        canblackjack = 0
        playerhand[1] = 0  # This means that since we split we need to have a 0 in the 2nd card slot for hit()
        hit()

    def push():
        global hands
        a = 1
        # print("PUSH")
        # print("No money was lost or won this hand")
        # print("playgame next...")
        # playgame()
        hands = hands + 1

    def rearrangehand():
        global playerhand
        playerhand = [playerhand[1], playerhand[0]]  # this makes sure the ace is in playerhand[0]
        howtoplay()

    def splitaces():
        global canblackjack
        global playersplit
        global bet
        global bankroll
        global playerhand
        global ogbet
        # print("splitaces")
        if playersplit == []:
            playersplit = ["A", 1]
        else:
            playersplit = ["A", playersplit[
                1] + 1]  # sets that player is splitting aces, and has split 1 additional time
        canblackjack = 0
        # if bankroll >= ogbet:  # do we have enough money to split
        # bet = bet + bet
        # else:
        # bet = bet + bankroll  # if we don't, we split all in
        playerhand = ["A", 0]  # sets up so that when we hit, we are ready to take another card in [1]
        hit()

    def acecard():  # This is when player gets Ace and another non ace.
        global bet
        global playerhand
        global dealerhand
        # print("acecard")
        if playerhand[1] == 10:
            # print("acecard1")
            if canblackjack == 0:
                stand()
            else:
                blackjack()
        elif playerhand[1] == 9:
            # print("acecard2")
            stand()
        elif playerhand[1] == 8 and dealerhand[0] == "A":
            # print("acecard3")
            stand()
        elif playerhand[1] <= 7 and dealerhand[0] == "A":
            # print("acecard4")
            hit()
        elif playerhand[1] == 8 and dealerhand[0] == 10:
            # print("acecard5")
            stand()
        elif playerhand[1] <= 7 and dealerhand[0] == 10:
            # print("acecard6")
            hit()
        elif playerhand[1] == 8 and dealerhand[0] == 9:
            stand()
        elif playerhand[1] <= 7 and dealerhand[0] == 9:
            hit()
        elif playerhand[1] == 8 and dealerhand[0] == 8:
            stand()
        elif playerhand[1] == 7 and dealerhand[0] == 8:
            stand()
        elif playerhand[1] <= 6 and dealerhand[0] == 8:
            hit()
        elif playerhand[1] == 8 and dealerhand[0] == 7:
            stand()
        elif playerhand[1] == 7 and dealerhand[0] == 7:
            stand()
        elif playerhand[1] <= 6 and dealerhand[0] == 7:
            hit()
        elif playerhand[1] <= 8 and dealerhand[0] == 6:
            double()
        elif playerhand[1] == 8 and dealerhand[0] == 5:
            stand()
        elif playerhand[1] <= 7 and dealerhand[0] == 5:
            double()
        elif playerhand[1] == 8 and dealerhand[0] == 4:
            stand()
        elif playerhand[1] == 7 and dealerhand[0] == 4:
            double()
        elif playerhand[1] == 6 and dealerhand[0] == 4:
            double()
        elif playerhand[1] == 5 and dealerhand[0] == 4:
            double()
        elif playerhand[1] == 4 and dealerhand[0] == 4:
            double()
        elif playerhand[1] <= 3 and dealerhand[0] == 4:
            hit()
        elif playerhand[1] == 8 and dealerhand[0] == 3:
            stand()
        elif playerhand[1] == 7 and dealerhand[0] == 3:
            double()
        elif playerhand[1] == 6 and dealerhand[0] == 3:
            double()
        elif playerhand[1] <= 5 and dealerhand[0] == 3:
            stand()
        elif playerhand[1] == 8 and dealerhand[0] == 2:
            stand()
        elif playerhand[1] == 7 and dealerhand[0] == 2:
            double()
        elif playerhand[1] <= 6 and dealerhand[0] == 2:
            hit()
        else:
            print("is it going to else?")

    def howtoplay():  # Programs the basic strategy for the computer, dealer and player already have hand
        global handtotal
        global playerhand
        global dealerhand
        global bet
        global playersplit
        global acecount
        global canblackjack
        global candouble
        global cansplit
        global runningcount
        # print("got to howtoplay")
        # print("playerhand", playerhand[0], " ", playerhand[1], " Dealer hand ", dealerhand[0], " ", dealerhand[1])
        # print("Your bet is, ", bet)
        # # This section checks if the dealer has blackjack~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if dealerhand[0] == "A" and dealerhand[1] == 10 and canblackjack == 1:
            if playerhand[0] == "A" and playerhand[1] == 10:
                push()
                runningcount = runningcount - 1
            elif playerhand[1] == "A" and playerhand[0] == 10:
                push()
                runningcount = runningcount - 1
            else:
                dealerblackjack()
        elif dealerhand[1] == "A" and dealerhand[0] == 10 and canblackjack == 1:
            if playerhand[0] == "A" and playerhand[1] == 10:
                push()
                runningcount = runningcount - 1
            elif playerhand[1] == "A" and playerhand[0] == 10:
                push()
                runningcount = runningcount - 1
            else:
                dealerblackjack()
        # End End of section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif playerhand[0] == "A" and playerhand[1] == "A":  # goes to split aces
            splitaces()

        elif playerhand[1] == "A" and playerhand[0] != "A":
            rearrangehand()  # this makes sure the ace is in playerhand[0]

        elif playerhand[0] == "A":
            acecard()
        elif playerhand[0] == playerhand[1] and cansplit == 1:  # split
            if playerhand[0] == 2:  # if we have split 2
                if dealerhand[0] == "A":
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]  # handtotal is the same, but [0] != [1].
                    howtoplay()
                elif dealerhand[0] <= 7:
                    split()
                else:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
            elif playerhand[0] == 3:
                if dealerhand[0] == "A":
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                elif dealerhand[0] <= 7:
                    split()
                else:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
            elif playerhand[0] == 4:
                if dealerhand[0] == "A":
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                elif dealerhand[0] == 5 or 6:
                    split()
                else:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
            elif playerhand[0] == 5:
                playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                howtoplay()
            elif playerhand[0] == 6:
                if dealerhand[0] == "A":
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                elif dealerhand[0] <= 6:
                    split()
                else:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
            elif playerhand[0] == 7:
                if dealerhand[0] == "A":
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                elif dealerhand[0] <= 7:
                    split()
                else:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
            elif playerhand[0] == 8:
                split()
            elif playerhand[0] == 9:
                if dealerhand[0] == "A":
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                elif dealerhand[0] == 10:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                elif dealerhand[0] == 7:
                    playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                    howtoplay()
                else:
                    split()
            elif playerhand[0] == 10:
                playerhand = [playerhand[0] - 1, playerhand[1] + 1]
                howtoplay()
        else:  # this means that there is no splitting and no aces to be messed with rn
            # print("No splitting and no aces")
            handtotal = playerhand[0] + playerhand[1]  # sets the handtotal
            if dealerhand[0] == dealerhand[0]:
                if handtotal >= 17:  # This ensures that player stands on 17 b4 it checks any other if statement.
                    stand()
                elif dealerhand[0] == "A" and handtotal == 11:
                    double()
                elif dealerhand[0] == "A":
                    hit()
                elif dealerhand[0] == 2 and handtotal <= 9:
                    hit()
                elif dealerhand[0] == 2 and handtotal == 10:
                    double()
                elif dealerhand[0] == 2 and handtotal == 11:
                    double()
                elif dealerhand[0] == 2 and handtotal == 12:
                    hit()
                elif dealerhand[0] == 2 and handtotal >= 13:
                    stand()
                elif dealerhand[0] == 3 and handtotal <= 8:
                    hit()
                elif dealerhand[0] == 3 and handtotal == 9:
                    double()
                elif dealerhand[0] == 3 and handtotal == 10:
                    double()
                elif dealerhand[0] == 3 and handtotal == 11:
                    double()
                elif dealerhand[0] == 3 and handtotal == 12:
                    hit()
                elif dealerhand[0] == 3 and handtotal >= 13:
                    stand()
                elif dealerhand[0] == 4 and handtotal <= 8:
                    hit()
                elif dealerhand[0] == 4 and handtotal == 9:
                    double()
                elif dealerhand[0] == 4 and handtotal == 10:
                    double()
                elif dealerhand[0] == 4 and handtotal == 11:
                    double()
                elif dealerhand[0] == 4 and handtotal >= 12:
                    stand()
                elif dealerhand[0] == 5 and handtotal <= 8:
                    hit()
                elif dealerhand[0] == 5 and handtotal == 9:
                    double()
                elif dealerhand[0] == 5 and handtotal == 10:
                    double()
                elif dealerhand[0] == 5 and handtotal == 11:
                    double()
                elif dealerhand[0] == 5 and handtotal >= 12:
                    stand()
                elif dealerhand[0] == 6 and handtotal <= 8:
                    hit()
                elif dealerhand[0] == 6 and handtotal == 9:
                    double()
                elif dealerhand[0] == 6 and handtotal == 10:
                    double()
                elif dealerhand[0] == 6 and handtotal == 11:
                    double()
                elif dealerhand[0] == 6 and handtotal >= 12:
                    stand()
                elif dealerhand[0] == 7 and handtotal <= 9:
                    hit()
                elif dealerhand[0] == 7 and handtotal == 10:
                    double()
                elif dealerhand[0] == 7 and handtotal == 11:
                    double()
                elif dealerhand[0] == 7 and handtotal >= 12:
                    hit()
                elif dealerhand[0] == 8 and handtotal <= 9:
                    hit()
                elif dealerhand[0] == 8 and handtotal == 10:
                    double()
                elif dealerhand[0] == 8 and handtotal == 11:
                    double()
                elif dealerhand[0] == 8 and handtotal >= 12:
                    hit()
                elif dealerhand[0] == 9 and handtotal <= 9:
                    hit()
                elif dealerhand[0] == 9 and handtotal == 10:
                    double()
                elif dealerhand[0] == 9 and handtotal == 11:
                    double()
                elif dealerhand[0] == 9 and handtotal >= 12:
                    hit()
                elif dealerhand[0] == 10 and handtotal <= 10:
                    hit()
                elif dealerhand[0] == 10 and handtotal <= 10:
                    hit()
                elif dealerhand[0] == 10 and handtotal == 11:
                    double()
                elif dealerhand[0] == 10 and handtotal >= 12:
                    hit()
    while simisdone == 0:
        playgame()


    # def # printtest():
        # print("test")


bankrollsim()
