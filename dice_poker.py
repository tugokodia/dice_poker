# TODO: класс игрока, компа наследовать, сохранения
import random
import time, os
from colorama import Fore, Style
from key_listener import getch
player = [0, 0, 0, 0, 0]
ai = [0, 0, 0, 0, 0]
    
def throw_dices():
    dices = []
    for n in range(5):        
        rnd = random.randrange(1, 7)
        dices.append(rnd)
    dices.sort()
    return dices

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
    print('\n\nPress enter to continue')
    input()
    return ' '


def start_menu():
    print('1. Начать')
    print('2. Инструкция')
    
    while True:
        char = getch()
        if (char == "1"):
            player_money = 100
            ai_money = 100
            new_game(player_money, ai_money)
            
        if (char == "2"):
            print(help())
            start_menu()
            
def get_bet():
    bet = 0
    while True:
        print('Введите ставку от 1 до 5')
        try:
            bet = int(input('Ваша ставка? '))
        except ValueError:
            print('Введена неверная сумма')
            continue
        if bet < 1 or bet > 5:
            print('Нарушены приделы возможной ставки')
            continue
        else:
            break
    return bet
    
def reroll__player_dices(dices):    
    rer = input('input a,b,c,d,e to reroll dices: ')
    if len(rer) > 0:        
        if 'a' in rer:
            dices[0] = random.randrange(1, 7)
        if 'b' in rer:
            dices[1] = random.randrange(1, 7)
        if 'c' in rer:
            dices[2] = random.randrange(1, 7)
        if 'd' in rer:
            dices[3] = random.randrange(1, 7)
        if 'e' in rer:
            dices[4] = random.randrange(1, 7)
    return dices

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
    
def reroll_ai_dices(dices):
    dct={}
    index_to_roll=[]
    for i in dices:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1    
    for key in dct:
        if dct[key] == 1:
            for i,x in enumerate(dices):
                if x == key:                    
                    index_to_roll.append(i)    
    for i in index_to_roll:                
        dices[i] = random.randrange(1, 7)
    return dices                
    
def new_game(player_money, ai_money):
    os.system('clear')    
    bank = 0
    ai_win = 0
    player_win = 0
    print(f'{Fore.YELLOW}################################################################################{Style.RESET_ALL}')
    for _round in range(3):     
        bet = get_bet()
        player_money -= bet
        ai_money -= bet
        bank = bank + bet
        print("БАНК: ", bank)
        print("Противник: ", ai_money)
        print("Игрок: ", player_money)
        print("Раунд: ", _round + 1)
        print(f'{Fore.YELLOW}################################################################################{Style.RESET_ALL}')
        print(f'{Fore.BLUE}PLAYER{Style.RESET_ALL}')
        player = throw_dices()        
        ai = throw_dices()
        print("[a, b, c, d, e]")
        player_comb, player_score = check_comb(player)
        print(player, " " ,player_comb, "\n")
        player = reroll__player_dices(player)
        player_comb, player_score = check_comb(player)
        print(player, " ", player_comb, "\n")
        print(f'{Fore.YELLOW}################################################################################{Style.RESET_ALL}')
        print(f'{Fore.RED}AI{Style.RESET_ALL}')
        ai_comb, ai_score = check_comb(ai)
        print(ai, " ", ai_comb, "\n")
        ai = reroll_ai_dices(ai)
        ai_comb, ai_score = check_comb(ai)
        print(ai, " ", ai_comb, "\n")
        if player_score > ai_score:
            player_win += 1
            print(f'{Fore.BLUE}Player win this round!{Style.RESET_ALL}')
        else:
            ai_win += 1
            print(f'{Fore.RED}AI win this round!{Style.RESET_ALL}')
        input("Press enter to continue")
        os.system('clear')
    if player_win > ai_win:
        player_money += bank
        print(f'{Fore.BLUE}Player win this game!{Style.RESET_ALL}')
    else:
        ai_money += bank
        print(f'{Fore.RED}AI win this game!{Style.RESET_ALL}')
    input(f'{Fore.GREEN}Press enter to next game{Style.RESET_ALL}')
    if player_money <= 0:
        player_money = 100
    if ai_money <= 0:
        ai_money = 100         
    os.system('clear')
    new_game(player_money, ai_money)

start_menu()
