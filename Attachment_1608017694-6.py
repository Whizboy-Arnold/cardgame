#!/usr/bin/env python3

# The module "requests" needs to be installed:
# windows: py -m pip install requests
# macOS: python3 -m pip install requests
import requests
import random

CARD_ICONS = {
    'h': '♥',  # (h)eart
    'c': '♣',  # (c)lub
    'd': '♦',  # (d)iamond
    's': '♠'   # (s)pade
}

# Documentation of API: https://deckofcardsapi.com/
API_URL_NEW_DECK = "https://deckofcardsapi.com/api/deck/new/"
API_URL_DRAW_CARD = "https://deckofcardsapi.com/api/deck/{deck_deckid}/draw/"


 

def get_52_card_deck():
    response_from_api = requests.get(API_URL_NEW_DECK)
    if response_from_api.status_code != 200:
        raise Warning("The API ddeckid not answer with 'OK' status.")
    data_from_api = response_from_api.json()
    return data_from_api['deck_id']


def shuffle_deck(deckid):
    API_URL_SHUFFLE_DECK = "https://deckofcardsapi.com/api/deck/"+str(deckid)+"/shuffle/"
    response_from_api = requests.get(API_URL_SHUFFLE_DECK)
    if response_from_api.status_code != 200:
        raise Warning("The API deckid not answer with 'OK' status.")
    data_from_api = response_from_api.json()
    return data_from_api['shuffled']

def drawCards(deckid):
    API_DRAW_CARD="https://deckofcardsapi.com/api/deck/"+str(deckid)+"/draw/?count=16"
    response_from_api = requests.get(API_DRAW_CARD)
    if response_from_api.status_code != 200:
        raise Warning("The API ddeckid not answer with 'OK' status.")
    data_from_api = response_from_api.json()
    return data_from_api['cards']


def createPlayerPile(deckid,player, drawn):
    API_PILE ="https://deckofcardsapi.com/api/deck/"+str(deckid)+"/pile/PLAYER"+str(player)+"/add/?cards="+drawn
    response_from_api = requests.get(API_PILE)
    if response_from_api.status_code != 200:
        raise Warning("The API deckid not answer with 'OK' status.")
    data_from_api = response_from_api.json()
    return data_from_api['remaining']

def checkPlayerPile(deckid, player):
    API_CHECK="https://deckofcardsapi.com/api/deck/"+str(deckid)+"/pile/PLAYER"+str(player)+"/list/"
    response_from_api = requests.get(API_CHECK)
    if response_from_api.status_code != 200:
        raise Warning("The API deckid not answer with 'OK' status.")
    data_from_api = response_from_api.json() 
    return data_from_api['piles']["PLAYER"+str(player)]["remaining"]


def playPlayerPile(deckid,player):
    API_DRAW ="https://deckofcardsapi.com/api/deck/"+str(deckid)+"/pile/PLAYER"+str(player)+"/draw/?count=1"
    response_from_api = requests.get(API_DRAW)
    if response_from_api.status_code != 200:
        raise Warning("The API deckid not answer with 'OK' status.")
    data_from_api = response_from_api.json()
    
    return data_from_api["cards"][0]["code"]

def lastCardPlayerPile(deckid,player):
    API_LIST="https://deckofcardsapi.com/api/deck/"+str(deckid)+"/pile/PLAYER"+str(player)+"/list/"
    response_from_api = requests.get(API_LIST)
    if response_from_api.status_code != 200:
        raise Warning("The API deckid not answer with 'OK' status.")
    data_from_api = response_from_api.json()
    l=len(data_from_api['piles']["PLAYER"+str(player)]["cards"])
    return data_from_api['piles']["PLAYER"+str(player)]["cards"][l-1]
 
def drawCardNum(code, top):
    if(top):
        return "|   "+code[0]+"           |"
    else:
        return "|           "+code[0]+"   |"
def drawCardMid(code):
    return "|       "+CARD_ICONS[code[1].lower()]+"       |"
                                
def drawCardEdge():
    return " _______________ "
def drawCardPad():
    return "|               |"

def printPile(cards):
    rnge=len(cards)
    if(len(cards)>3): rnge=3 
        
    todraw=""
    for x in range(1):
        for x in range(rnge):
            todraw= todraw+drawCardEdge()+' '
        todraw=todraw+drawCardEdge()+"\n"
    for x in range(1):
        for x in range(rnge):
            todraw= todraw+drawCardNum(cards[x], True)+' '
        todraw=todraw+drawCardNum(cards[len(cards)-1], True)+'\n'
    for x in range(3):
        for x in range(rnge):
            todraw= todraw+drawCardPad()+' '
        todraw=todraw+drawCardPad()+"\n" 
    for x in range(1):
        for x in range(rnge):
            todraw= todraw+drawCardMid(cards[x])+' '
        todraw=todraw+drawCardMid(cards[len(cards)-1])+'\n'
    for x in range(3):
        for x in range(rnge):
            todraw= todraw+drawCardPad()+' '
        todraw=todraw+drawCardPad()+"\n"
    for x in range(1):
        for x in range(rnge):
            todraw= todraw+drawCardNum(cards[x], False)+' '
        todraw=todraw+drawCardNum(cards[len(cards)-1], False)+'\n'
    for x in range(1):
        for x in range(rnge):
            todraw= todraw+drawCardEdge()+' '
        todraw=todraw+drawCardEdge()+"\n"
    return todraw



print("Welcome to color and Value!\n\nCards - You: 16 Computers:16\n Points You:0 Computer:0 ")
    
deckid =get_52_card_deck() 
shuffled =shuffle_deck(deckid) 


cards = drawCards(deckid);
todraw = ""
 
for x in range(len(cards)-1): 
    todraw= todraw+cards[x]["code"]+','
todraw=todraw+cards[len(cards)-1]["code"]
 
pile=createPlayerPile(deckid,1,todraw)




cards = drawCards(deckid);
todraw = ""

for x in range(len(cards)-1): 
    todraw= todraw+cards[x]["code"]+','
todraw=todraw+cards[len(cards)-1]["code"]
 
pile=createPlayerPile(deckid,2,todraw)
 
print(printPile(todraw.split(",")))


pointsp1=0
pointsp2=0
userturn=True;
winsp1=0;
winsp2=0;


def play(check,g1):
    global pointsp1;
    global pointsp2;
    global userturn;
    if(g1=="RED"):
        if(check["code"][1]=='H' or check["code"][1]=='D'):
            correct=True
            g2=""
            if(userturn):
                pointsp1 += 1
                print("\nThe card was:"+CARD_ICONS[check["code"][1].lower()]+"well guessed - You get a point") 
                g2=input(" Guess the value: A for Ace,Q for Queen,K for King,J for Jack or n where n is a single number 2-9\n:")
            else:
                pointsp2 += 1
                numbers = ["A","Q","K","J","2","3","4","5","6","7","8","9"]
                g2= random.choice(numbers) 
                print("YAAY 1 POINT FOR ME!! I guess to try on the number so shoot:\n"+g2)
                
            if(g2==check["code"][0] ):
                print("The cards was: "+check["code"][0]+CARD_ICONS[check["code"][1].lower()]+" - You get 4 points!")
                return True
            else:
                print("You guessed wrong value!")
                return True
        else:
            print("You guessed wrong color!")
            return False
    else:
        if(g1=="BLACK"):
            if(check["code"][1]=='S' or check["code"][1]=='C'):
                correct=True
                g2=""
                if(userturn):
                    print("\nThe card was:"+CARD_ICONS[check["code"][1].lower()]+"well guessed - Iget a point") 
                    g2=input(" Guess the value: A for Ace,Q for Queen,K for King,J for Jack or n where n is a single number 2-9\n:")
                else:
                    pointsp2 += 1
                    numbers = ["A","Q","K","J","2","3","4","5","6","7","8","9"]
                    g2= random.choice(numbers) 
                    print("YAAY 1 POINT FOR ME!! I guess to try on the number so shoot:\n"+g2)
                
                if(g2==check["code"][0]  ):
                    print("The cards was: "+check["code"][0]+CARD_ICONS[check["code"][1].lower()]+" - I get 4 points!")
                    return True
                else:
                    print("You guessed wrong value!")
                    return True
            else:
                print("You guessed wrong color!")
                return False
        else:
            raise Exception("wrong input only accepts RED or BLACK in caps")
        

cont=True; 
while(cont):
    while(checkPlayerPile(deckid,1)>0 and checkPlayerPile(deckid,2)>0):
        if(userturn):
            g1 = input(" Guess the color (either BLACK or RED): ")
            check=lastCardPlayerPile(deckid, 1) 
            if(play(check,g1)):
                removed=playPlayerPile(deckid,1) ;
                check=lastCardPlayerPile(deckid, 1) 
                g1 = input("Guess the color (either BLACK or RED): ")
                play(check,g1)
                removed=playPlayerPile(deckid,1)
 
            else:
                print(" now its my Turn")
            userturn=False
        else:
            colors = ["RED", "BLACK"]
            g1= random.choice(colors) 
            print("I will guess your card color as\n: "+g1+"")
            
            check=lastCardPlayerPile(deckid, 2)
            print("sneek "+check["code"])
            if(play(check, g1)):
                removed=playPlayerPile(deckid,2)
                check=lastCardPlayerPile(deckid, 2)
                g1 = random.choice(colors) 
                play(check,g1)
                removed=playPlayerPile(deckid,2) 
            else:
                print(" i think its your Turn")
            userturn=True
            
        print("your points "+str(pointsp1)+" my points "+str(pointsp2))
        if(max(pointsp1,pointsp1)==pointsp1):
            winsp1=winsp1+1;
            print("YOU WON!")
        else:
            winsp2=winsp2+1;
            print("YOU LOST");
            
    val=input("do you want to play again? Y -yes or N- no")
    if(val=="N"):
        cont=false
    else:
        pointsp1=0;pointsp2=0
        
            
RESULTS={
"player" :{
        "wins": winsp1,
        "total_points": pointsp1        
    },
"computer" :{
        "Wins": winsp2,
        "total_points": pointsp2
    }
}

with open("game_statistics.json","w")as outfile:json.dump(data,outfile) 


