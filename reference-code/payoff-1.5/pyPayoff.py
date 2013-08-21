#Application to calculate how
#deep users search given parameters
#Author: Sean Galbraith
#Last updated 15/03/13

import os
import random
import time

raw = 0
queries = 20
results = 10
begtok = 40
restok = 1
quertok = 2

def splashscreen():
    os.system('clear')
    print("Welcome to the game. Enter N to begin.")
    print("Enter R to read the rules.")
    print("Enter Q to quit")
    postypes = ["High","Mid","Low"]
    random.shuffle(postypes)
    userin = input()
    while userin != "Q" and userin != "q":
        if userin == "N" or userin == "n":
            pregame(postypes)
        elif userin == "R" or userin == "r":
            rules()
        else:
            userin = input()
    raise SystemExit(0)

def pregame(postypes):
    os.system('clear')
    print("You will play 9 games in total, 3 for each yield type.")
    print("The first 3 games' yield will be " +postypes[0])
    print("The second 3 games' yield will be " +postypes[1])
    print("The final 3 games' yield will be " +postypes[2])
    print("")
    print("Enter N when you are ready to begin")
    userin = input()
    while userin != "N" and userin != "n":
        userin = input()
    for x in postypes:
        os.system('clear')
        print(x + " yield game beginning in 5 seconds.")
        time.sleep(5)
        game(x, 1, True, 1)
    os.system('clear')
    print("Thanks for playing.")
    print("In 5 seconds you will return to the home screen")
    print("where you may play again or quit")
    time.sleep(5)
    splashscreen()
    

def rules():
    os.system('clear')
    print("Payoff is an abstract search game.")
    print("The aim of the game is to score as many points as possible.")
    print("You have a limited amount of tokens.")
    print("Uncovering a result earns you its value in points")
    print("But both reading a result and moving to a new query costs tokens.")
    print("")
    print("There are 3 types of games: High, Medium and Low yields")
    print("High suggests a high average payoff, medium less so and low the lowest")
    print("Use the yield information to your advantage to beat the game and earn a high score!")
    print("")
    print("Enter R to return to the splash screen")
    userin = input()
    while userin != "R" and userin != "r":
        userin = input()
    splashscreen()

def getquer(fi):
    f = open(fi)
    allquer = []
    for query in f:
        count = 0
        quer = []
        while count < results:
            quer += query[count]
            count += 1
        quer += [query[len(quer):]]
        allquer += [quer]
    f.close()
    return allquer

def printscreen(totalgames,totalpoints,tokens,curq,curr,allquer,querystring,game,points):
    os.system('clear')
    dotline = "-"*40
    print(dotline)
    print("Game " + str(game) + " of " + str(totalgames) + "          Overall points: " +str(totalpoints))
    print(dotline)
    print("Current Game")
    print("Tokens remaining: " + str(tokens) + "         " + "Points: " + str(points))
    print(dotline)
    print("N: To view next result costs " +str(restok)+ " tokens.")
    print("Q: To move to next query costs " +str(quertok)+ " tokens.")
    print(dotline)
    print("You are currently on query " +str(curq+1)+ " out of " + str(len(allquer)) +".")
    print(str(curq+1) + ": " + querystring)
    print(dotline)

def gensnippets():
    ##test stub for generating snippers per game
    avalue = 10
    qpos = qget()
    snippets = (["Q"] * avalue*qpos) + (["R"] * avalue*(1-qpos))
    return snippets

def qget():
    ##return likelihood of snippet accuracy based on formula
    test = 0.6
    return test
                                        

def game(gtype, revtype, strue, snippets):
    tokens = begtok
    points = 0
    
    curq = 0
    curr = 0
    qlist = []
    thisq = ""
    countdep = 0
    countdepl = []
    countprec = []
    game = 1
    totalgames = 3
    totalpoints = 0
    allpos = [1,2,3,4,5]
    random.shuffle(allpos)
    posgames = []
    posgames += [allpos[0]]
    posgames += [allpos[1]]
    posgames += [allpos[2]]
    first = True
    s = open('results.txt', 'a')
    s.write("\n")
    s.write("====================\n")
    s.write("Begin results set\n")
    s.write("Cost of Result: " + str(restok) +"\n")
    s.write("Cost of Query: " + str(quertok)+"\n")
    s.write("Games in this set: " + str(totalgames)+"\n")
    s.write("--------------------\n")
    for x in posgames:
            if x == 1:
                if gtype == "High":
                    allquer = getquer("high1.txt")
                elif gtype == "Mid":
                    allquer = getquer("mid1.txt")
                elif gtype == "Low":
                    allquer = getquer("low1.txt")                    
            elif x == 2:
                if gtype == "High":
                    allquer = getquer("high2.txt")
                elif gtype == "Mid":
                    allquer = getquer("mid2.txt")
                elif gtype == "Low":
                    allquer = getquer("low2.txt")  
            elif x == 3:
                if gtype == "High":
                    allquer = getquer("high3.txt")
                elif gtype == "Mid":
                    allquer = getquer("mid3.txt")
                elif gtype == "Low":
                    allquer = getquer("low3.txt")
            elif x == 4:
                if gtype == "High":
                    allquer = getquer("high4.txt")
                elif gtype == "Mid":
                    allquer = getquer("mid4.txt")
                elif gtype == "Low":
                    allquer = getquer("low4.txt")
            elif x == 5:
                if gtype == "High":
                    allquer = getquer("high5.txt")
                elif gtype == "Mid":
                    allquer = getquer("mid5.txt")
                elif gtype == "Low":
                    allquer = getquer("low5.txt") 
            querystring = "X "*(len(allquer[curq])-1)
            first = True
            onquery = 1
            querreslist = []
            finalstatelist = []
            while tokens > 0:
                if first == True:
                    querres = ""
                    quercount = 0
                    for y in allquer[curq]:
                        if quercount < results:
                            querres += str(y)
                            quercount += 1
                    querreslist += [querres]
                    first = False
                printscreen(totalgames,totalpoints,tokens,curq,curr,allquer,querystring,game,points)
                userin = input()
                if userin == "N" and "X" not in querystring or userin == "n" and "X" not in querystring:
                    print("No more results for this query. Q to move to next.")
                    userin = input()
                if userin == "Q" and "X" not in querystring or userin == "q" and onquery == queries:
                    print("There are no more queries. N to read next result.")
                    userin = input()
                if userin == "N" or userin == "n" and "X" in querystring:
                    countdep += 1
                    if allquer[curq][curr] == "0":
                        thisq += str(allquer[curq][curr]) + " "
                        querystring = thisq + querystring[(countdep*2):]
                        curr += 1
                        tokens -= restok
                        if tokens < 0 or tokens == 0:
                            countdepl += [countdep]
                            finalstatelist += [querystring]
                            countprec += [allquer[curq][-1]]
                    elif allquer[curq][curr] == "1" or allquer[curq][curr] == "2" or allquer[curq][curr] == "3":
                        points += int(allquer[curq][curr])
                        thisq += str(allquer[curq][curr]) + " "
                        querystring = thisq + querystring[(countdep*2):]
                        curr += 1
                        tokens -= restok
                        if tokens < 0 or tokens == 0:
                            countdepl += [countdep]
                            finalstatelist += [querystring]
                            countprec += [allquer[curq][-1]]                
                elif userin == "Q" or userin == "q" and onquery != queries:
                    onquery += 1
                    finalstatelist += [querystring]
                    querystring = "X "*((len(allquer[curq]))-1)
                    countdepl += [countdep]
                    countdep = 0
                    countprec += [allquer[curq][-1]]
                    curr = 0
                    curq += 1
                    thisq = ""
                    first = True
                    tokens -= quertok
                    querres = ""
                    quercount = 0
                    for y in allquer[curq]:
                        if quercount < results:
                            querres += str(y)
                            quercount += 1
                    querreslist += [querres]

            printscreen(totalgames,totalpoints,tokens,curq,curr,allquer,querystring,game,points)            
            print("End of game " +str(game)+ ". Please wait 5 seconds.")
            time.sleep(5)
            game += 1
            tokens = begtok
            curq = 0
            curr = 0
            totalpoints += points
            points = 0
            countdep = 0
            thisq = ""
            rescount = 0
            s.write("Game ID: " + str(x) +"\n")
            s.write("Queries looked at: "+"\n")
            s.write("Full Query      Final State        Depth Ended\n")
            for z in countdepl:
                s.write(str(querreslist[rescount]) + "    " + str(finalstatelist[rescount]) + "      " + str(z) + "      \n")
                rescount += 1
            countdepl = []
    s.write("Overall game points: "+ str(totalpoints)+"\n")
    s.write("End results set\n")
    s.write("====================\n")
    s.write("")
    s.close()
    if raw == 1:
            s = open('rawresults.txt', 'a')
            s.write("====================\n")
            s.write(str(querreslist[rescount]) + " : " + str(finalstatelist[rescount]) + " : " + str(z) + "\n")
            s.write("====================\n")
            s.close()
splashscreen() #Start the program
