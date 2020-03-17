import random
import time, os
from colorama import Fore, Style
from key_listener import getch

class Player:
    
    def __init__(self, name = 'player', money = 100):
        
        self.name = name
        self.money = money
        self.dices = [0, 0, 0, 0, 0]
        self.score = 0
        
    
    def do_turn(self):
        
        rer = input("input a,b,c,d,e to reroll dices: ")
        
        if len(rer) > 0:        
            if 'a' in rer:
                self.dices[0] = random.randrange(1, 7)
            if 'b' in rer:
                self.dices[1] = random.randrange(1, 7)
            if 'c' in rer:
                self.dices[2] = random.randrange(1, 7)
            if 'd' in rer:
                self.dices[3] = random.randrange(1, 7)
            if 'e' in rer:
                self.dices[4] = random.randrange(1, 7)        
        
    
    def do_bet(self):        
        
        bet = 0
        
        while True:
            
            print("Type bet from 1 to 5")
            
            try:
                bet = int(input("Your bet? "))
                
            except ValueError:
                print("Wrong number")
                continue
                
            if bet < 1 or bet > 5:
                print("From one to five. Type again")
                continue
            else:
                break
                
        return bet
            
    
    def throw_dices(self):
    
        dices = []
        for n in range(5):        
            rnd = random.randrange(1, 7)
            dices.append(rnd)
        dices.sort()
        self.dices = dices
        
class Bot(Player):
    
    def do_turn(self):
                
        dct={}
        index_to_roll=[]
        for i in self.dices:
            if i in dct:
                dct[i] += 1
            else:
                dct[i] = 1    
        for key in dct:
            if dct[key] == 1:
                for i,x in enumerate(self.dices):
                    if x == key:                    
                        index_to_roll.append(i)    
        for i in index_to_roll:                
            self.dices[i] = random.randrange(1, 7)        
                        
        
    def do_bet(self):
        
        bet = 5
        return bet
            

def help():
    
    print(
'''
Покер ----------> все пять костей с одинаковым количеством очков.
Каре -----------> четыре кости с одинаковым количеством очков.
Фул Хаус -------> пара и три кости одного достоинства.
Стрейт Большой -> пять костей с разным достоинством в послед-сти от 2 до 6.
Стрейт Малый ---> пять костей с разным достоинством в послед-сти от 1 до 5.
Сет ------------> три кости одного достоинства.
Две пары -------> две пары костей одного достоинства каждая.
Пара -----------> две кости одного достоинства.
''')
    print("\n\nPress enter to continue")
    input()
    return ' '


def start_menu():
    
    print("1. One player")
    print("2. Two player\n")
    print("5. Instructions\n")
    print("0. Exit")
    
    while True:

        char = getch()
        
        if (char == '1'):       
        
            player_one = Player(input("Your name? "), 100)
            player_two = Bot('cpu', 100)
            new_game(player_one, player_two)
        
        elif (char == '2'):
        
            player_one = Player(input("Player one name? "), 100)
            player_two = Player(input("Player two name? "), 100)
            new_game(player_one, player_two)
            
        elif (char == '5'):
            
            print(help())
            start_menu()                 
            
        elif (char == '0'):
            print("See ya!")
            exit(0)


def check_comb(player):
    
    player.sort()    
    dct = {}
    comb_name = ''
    scores = 0
    for i in player:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1
    for key in dct:
        if dct[key] == 5:
            comb_name = 'Five of a kind'
            scores = 1000 + int(key)
        if dct[key] == 4:
            comb_name = 'Four of a kind'
            scores = 900  + int(key)
        if dct[key] == 3:
            comb_name += 'Three of a kind'
            scores = 400  + int(key)
        if dct[key] == 2:
            comb_name += 'One pair'
            scores = 100  + int(key)
    if comb_name == 'One pairOne pair':
        comb_name = 'Two pair'
        scores += 200
    if comb_name ==  'Three of a kindOne pair':
        comb_name = 'Full house'
        scores += 400
    if comb_name == 'One pairThree of a kind':
        comb_name = 'Full house'
        scores += 400
    low_straight = [1, 2, 3, 4, 5]
    high_straight = [2, 3, 4, 5, 6]
    if player == high_straight:
        comb_name = 'High straight'
        scores = 600
    if player == low_straight:
        comb_name = 'Low straight'
        scores = 500
    return comb_name, scores  
  
    
def new_game(player_one, player_two):
    
    os.system('clear')    
    bank = 0
    player_one_win = 0
    player_two_win = 0
    
    print(f'{Fore.YELLOW}################################################################################{Style.RESET_ALL}')
    
    for _round in range(3):     
        bet = player_one.do_bet()        
        player_one.money = player_one.money - bet
        player_two.money = player_two.money - bet
        bank = bank + bet
        
        player_win = 0
        ai_win = 0
        
        print("Bank: ", bank)        
        print(player_one.name,": ", player_one.money)
        print(player_two.name,": ", player_two.money)
        print("Round: ", _round + 1)
        player_one.throw_dices()        
        player_two.throw_dices()
        
        print(f"{Fore.YELLOW}################################################################################{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{player_one.name}{Style.RESET_ALL}")        
        print("[a, b, c, d, e]")
        p_one_comb, player_one.score = check_comb(player_one.dices)
        print(player_one.dices, " " ,p_one_comb, "\n")
        player_one.do_turn()
        p_one_comb, player_one.score = check_comb(player_one.dices)
        print(player_one.dices, " ", p_one_comb, "\n")
        
        print(f"{Fore.YELLOW}################################################################################{Style.RESET_ALL}")        
        print(f"{Fore.RED}{player_two.name}{Style.RESET_ALL}")
        print("[a, b, c, d, e]")
        p_two_comb, player_two.score = check_comb(player_two.dices)
        print(player_two.dices, " ", p_two_comb, "\n")
        player_two.do_turn()
        p_two_comb, player_two.score = check_comb(player_two.dices)
        print(player_two.dices, " ", p_two_comb, "\n")
        
        if player_one.score > player_two.score:
            player_win += 1
            print(f"{Fore.BLUE}{player_one.name} win this round!{Style.RESET_ALL}")
        else:
            ai_win += 1
            print(f"{Fore.RED}{player_two.name} win this round!{Style.RESET_ALL}")
        input("Press enter to continue")
        os.system('clear')
    if player_win > ai_win:
        player_one.money += bank
        print(f"{Fore.BLUE}{player_one.name} win this game!{Style.RESET_ALL}")
    else:
        player_two.money += bank
        print(f"{Fore.RED}{player_one.name} win this game!{Style.RESET_ALL}")
    input(f"{Fore.GREEN}Press enter to next game{Style.RESET_ALL}")
    if player_one.money <= 0:
        player_one.money = 100
    if player_two.money <= 0:
        player_two.money = 100         
    os.system('clear')
    new_game(player_one, player_two)


def main():
    
    start_menu()
    
    
if __name__ == '__main__':
    
    try:
        main()
        
    except KeyboardInterrupt:
        print()
        print("Shutting down, bye!")
