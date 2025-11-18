import numpy as np
import time
import warnings
warnings.filterwarnings("ignore")

Card = 6

Cardpoor = np.ones(52*Card)
CardKind = ["Heart", "Spade" ,"Diamond" ,"Club"]
CardFace = ["", " A", " 2", " 3", " 4", " 5", " 6",
            " 7", " 8", " 9", "10", " J", " Q", " K"]

def hit():
    sample = np.random.randint(0, high=52*Card, size=1, dtype=int)[0]
    while Cardpoor[sample] == 0:
        sample = np.random.randint(0, high=52*Card, size=1, dtype=int).flatten()
    Cardpoor[sample] = 0
    
    sample_Kind = (sample // 13) % 4
    sample_number = sample % 13
    
    return sample_number+1, sample_Kind

def Blackjack():    
    status = np.zeros(2)
    gain = 0
    if np.any(DealerHand[:, 0, 0]==1)==True and np.any(DealerHand[:, 0, 0]>=10) ==True:
        status[0] = 1
    if np.any(PlayerHand[:, 0, 0]==1)==True and np.any(PlayerHand[:, 0, 0]>=10) ==True :    
        status[1] = 1
    
    if status[0] == 1 and status[1] == 1:
        PlayerSatus[0] = 0
        DealerSatus[0] = 3
        display()
        print('\nBoth have Black Jack')
        PlayerBet[0] = 0
    elif status[0] == 1 and status[1] == 0:
        PlayerSatus[0] = 0
        DealerSatus[0] = 3
        display()
        print('\nDealer has Black Jack, you lose!')
        gain = -PlayerBet[0]
        PlayerBet[0] = 0
    elif status[0] == 0 and status[1] == 1:
        PlayerSatus[0] = 0
        DealerSatus[0] = 3
        display()
        print('\nYou have Black Jack, you Win!')
        gain = PlayerBet[0] * 1.5
        PlayerBet[0] = 0    
    return gain

def operate():
    if PlayerSatus[0] < 3 and PlayerSatus[1] == 0 and PlayerHand[0, 0, 0] == PlayerHand[1, 0, 0]:
        act = 0
        while act != 'y' and act != 'n': 
            print('\nDo you want to split the cards?')
            act = str(input('y: yes / n: no \n')) 
            if act  == 'y':
                PlayerBet[1] = PlayerBet[0]
                PlayerHand[0, 0, 1] =  PlayerHand[1, 0, 0]
                PlayerHand[0, 1, 1] =  PlayerHand[1, 1, 0]           
                PlayerHand[1, 0, 0] = 0
                PlayerHand[1, 1, 0] = 0
                PlayerSatus[0] = 1
                PlayerSatus[1] = 1
                displayChips()
   
    for i in range(2):
        if PlayerSatus[i] >= 1 and PlayerSatus[i] < 20:
            act = 0  
            while act != 'h' and act != 's' and act != 'd':
                print('\nFor hand:  ' + str(i+1) + '  whats you act?' )
                act = str(input('h: Hit / s:stop / d:double\n'))
                if act == 'h':
                    PlayerHand[PlayerSatus[i], 0, i], PlayerHand[PlayerSatus[i], 1, i] = hit()
                    PlayerSatus[i] += 1
                elif act == 'd':
                    PlayerHand[PlayerSatus[i], 0, i], PlayerHand[PlayerSatus[i], 1, i] = hit()
                    PlayerSatus[i] = 20
                    PlayerBet[i] = PlayerBet[i]*2
                elif act == 's':
                    PlayerSatus[i] = 20

def CalculateScore(hand, split): 
    hand = np.copy(hand[:, 0, split])
    hand[hand>10] = 10
    if np.any(hand==1) == True:
        hand = np.repeat([hand], 2 , axis=0)
        hand[1, np.where(hand[0,:]==1)[0][0]] = 11
        score = np.sum(hand, axis=1)
        if np.any(score <= 21) == True:
            score = np.max(score[score <= 21])
        else:
            score = np.min(score)       
    else:
        score = np.sum(hand)
    
    return score

def Inventory_1():
    gain = 0
    for i in range(2):
        if PlayerSatus[i] > 0:
            PlayerSore[i] = CalculateScore(PlayerHand, i)
            if PlayerSore[i] > 21:
                gain = gain - PlayerBet[i]
                print('\n~~ Player lose! ~~\nHand: ' + str(i+1) + ' is over 21!\n')
                PlayerBet[i] = 0
                PlayerSatus[i] = 0
            elif PlayerSore[i] <= 21 and PlayerSatus[i] >= 5:
                gain = gain + PlayerBet[i]
                print('\n~~ Player win! ~~\nHand: ' + str(i+1) + ' is over 5 cards!\n')
                PlayerBet[i] = 0
                PlayerSatus[i] = 0
    return gain                    

def display():
    print('### Dealer:')
    card = DealerHand[DealerHand[:, 0, 0] != 0, :, 0].astype(int)
    if np.any(DealerSatus[0] < 2) == True:        
        print('1st card: ** - ***')
        for i in range(1, len(card) ):
            print(str(i+1) + 'st card: ' + CardFace[card[i, 0]] + ' - ' + CardKind[card[i, 1]])
    else:
        for i in range( len(card) ):
            print(str(i+1) + 'st card: ' + CardFace[card[i, 0]] + ' - ' + CardKind[card[i, 1]])
    
    print('\n### Player:')
    
    if PlayerSatus[1] == 0:
        card = PlayerHand[PlayerHand[:, 0, 0] != 0, :, 0].astype(int)
        for j in range(0, len(card) ):
            print(str(j+1) + 'st card: ' + CardFace[card[j, 0]] + ' - ' + CardKind[card[j, 1]])
    else:  
        for i in range(2):
            print('^^ hand: ' + str(i+1) )
            card = PlayerHand[PlayerHand[:, 0, i] != 0, :, i].astype(int)
            for j in range(0, len(card) ):
                print(str(j+1) + 'st card: ' + CardFace[card[j, 0]] + ' - ' + CardKind[card[j, 1]])

def displayChips():
    print('-----Chip on table-----\nH1: ' + str(PlayerBet[0]) + '   H2: ' + str(PlayerBet[1]))
    print('Total chips: ' + str(int(TotalBet)) )

TotalBet = float( input('How many chips in total?\n') )
BetUnit = TotalBet + 1

while BetUnit > TotalBet:
    print('The BetUnit should less than Total chips\n')
    BetUnit = int( input('BetUnit?\n') )

playtime = 0

while TotalBet >= BetUnit:
    playtime += 1
    print('\n\n====== Game ' + str(playtime) + ' start ======')
    
    DealerSatus = np.zeros(2).astype(int)
    PlayerSatus = np.zeros(2).astype(int)
    PlayerBet = np.zeros(2)
    
    PlayerHand = np.zeros(15*2*2).reshape(15, 2, 2).astype(int)
    PlayerSore = np.zeros(2).astype(int)
    DealerHand = np.zeros(15*2*2).reshape(15, 2, 2).astype(int)
    DealerSore = np.zeros(2).astype(int)  
    
    PlayerBet[0] = BetUnit
    DealerSatus[0] = 1
    PlayerSatus[0] = 2
    PlayerHand[0, 0, 0], PlayerHand[0, 1, 0] = hit()
    DealerHand[0, 0, 0], DealerHand[0, 1, 0] = hit()
    PlayerHand[1, 0, 0], PlayerHand[1, 1, 0] = hit()
    DealerHand[1, 0, 0], DealerHand[1, 1, 0] = hit()

    TotalBet = TotalBet + Blackjack()
    if PlayerSatus[0] == 0:
        displayChips()
    else:
        display()
        displayChips()

    while np.any(PlayerSatus[PlayerSatus<20]> 0) == True:
        operate()
        print('\n========================')
        display()
        displayChips()
        
        gain = Inventory_1()
        if gain != 0:
            TotalBet = TotalBet + gain
            displayChips()
            time.sleep(2)
 
    print('\n~~Dealer~~')
    time.sleep(1)
    DealerSatus[0] = 2  
    
    
    while np.any(PlayerSatus >= 20) == True:
        print('\n========================')
        display()
        displayChips()
        DealerSore[0] = CalculateScore(DealerHand, 0)
        
        if DealerSore[0] > 21:
            print('\n~~ Player win! ~~\n'
                    + 'Dealer : ' + str(DealerSore[0]) + ' is over 21!')
            
            TotalBet = TotalBet + np.sum(PlayerBet)
            PlayerBet = np.zeros(2)
            displayChips()
            PlayerSatus = 0
            
        elif DealerSore[0] <= 21 and DealerSatus[0] >= 5:
            print('\n~~ Dealer win! ~~\n'
                  + 'Dealer score: ' + str(DealerSore[0])
                  + '  Dealer card: ' + str(DealerSatus[0]) )
            TotalBet = TotalBet - np.sum(PlayerBet)
            PlayerBet = np.zeros(2)
            displayChips()
            PlayerSatus = 0
        
        elif DealerSore[0] <= 21 and DealerSatus[0] < 5:
            if DealerSore[0] < np.max(PlayerSore):
                DealerHand[DealerSatus[0], 0, 0], DealerHand[DealerSatus[0], 1, 0] = hit()
                DealerSatus[0] += 1
            else:
                for i in range(2):
                    if PlayerSatus[i] > 0:
                        if DealerSore[0] > PlayerSore[i]:
                            print('\n~~ Dealer win! ~~'
                                  + '\nDealer score: ' + str(DealerSore[0])
                                  + '\nPlayer Hand ' + str(i+1) + ' score: ' + str(PlayerSore[i]) )
                            TotalBet = TotalBet - PlayerBet[i]
                            PlayerBet[i] = 0
                            PlayerSatus[i] = 0
                            displayChips()
                            
                        elif DealerSore[0] < PlayerSore[i]:
                            print('\n~~ Player win! ~~'
                                  + '\nDealer score: ' + str(DealerSore[0])
                                  + '\nPlayer Hand ' + str(i+1) + ' score: ' + str(PlayerSore[i]) )
                            TotalBet = TotalBet + PlayerBet[i]
                            PlayerBet[i] = 0
                            PlayerSatus[i] = 0
                            displayChips()
                        elif DealerSore[0] == PlayerSore[i]:
                            print('\n~~ Draw! ~~'
                                  + '\nDealer score: ' + str(DealerSore[0])
                                  + '\nPlayer Hand ' + str(i+1) + ' score: ' + str(PlayerSore[i]) )
                            PlayerBet[i] = 0
                            PlayerSatus[i] = 0
                            displayChips()
                        else:
                            print('Error2')
              
        else:
            print('Error1')
        
        time.sleep(1)
    game = input('one more? any key (stop: s)')
    if game == 's':
        BetUnit = TotalBet +1

    if np.sum(Cardpoor) < (26*Card):
        print('\n\nThe card pool is less than half full, so its being reshuffled.')
        Cardpoor = np.ones(52*Card)

print('\n\n==============================')
print('==   You have play ' + str(playtime) + ' times  ==')        
print('==   Total chips left: ' + str(TotalBet) + '   ==')
print('==============================')          
