'''
It is suggested to turn font size down to 8 and use
the font 'Courier New'.
'''
import random
import time
import math
from SSSDpak import coyotebattle
from SSSDpak import maps
from SSSDpak import spiderbattle
from SSSDpak import cactusbattle
from SSSDpak import snakebattle
from SSSDpak import camelbattle
from SSSDpak import blank
import winsound
import music
import os


ui = '~'
vi = '~'
hi = '~'
wi = '~'
si = '~'
fi = '~'
omi = '~'

village = False
house = False
stats = False
shop = False
forge = False
inn = False
Farm = False
desert = False
t = False
Cactus = False
Coyote = False
Spider = False
Snake = False
Camel = False
Task = False
TaskCact = False
TaskCoyo = False
TaskSpid = False
TaskSnek = False
TaskCam = False

David = False
Thenttkil = False
Xehspfe = False
GK = False

Cacti = 10
Coyo_Fur = 8
Spooder_Kills = 6
Venom = 4
Camel_Souls = 2
ob = 0

money = 0
kappas = 0
investmoney = 0

p_lvl = 1
p_xp = 0
p_xp_lvl = 100
p_statpt = 0
p_str_b = 5
p_stm_b = 20
p_spd_b = 5
p_spd_b_w = 0
p_spd_b_u = 0
p_str = p_str_b
p_stm = p_stm_b
p_spd = p_spd_b
p_max_hp_b = p_stm*5
p_max_hp = p_max_hp_b
p_hp = p_max_hp
p_dmg_min = p_str+2
p_dmg_max = math.ceil(p_str*1.3+5)
p_crit_c = p_spd/100

cur_wep = 'Your Fist'
cur_arm = 'Your Shirt'
cur_uti = 'Your Feet'

pot_n = 0

Fist = 0
Shirt = 0
Feet = 0
Stick_t = False
Stick = 1
Woodsword_t = False
Woodsword = 4
Slingshot_t = False
Slingshot = 5
Clothes_t = False
Clothes = 1
Leather_t = False
Leather = 4
Chain_t = False
Chain = 10
Sandals_t = False
Sandals = 1
Shoes_t = False
Shoes = 4
Goggles_t = False
Goggles = 6

coolometer = 0

e_lvl_b = 1
e_lvl = e_lvl_b
e_spd = 5*(0.85*e_lvl)
e_max_hp = 25*e_lvl
e_hp = e_max_hp
e_dmg_min = 4*(1.5*e_lvl)
e_dmg_max = 8*(1.5*e_lvl)+2
e_crit_c = e_spd/100

xp_drop = math.ceil(e_lvl*1.125)

g_drop_min = (e_lvl*15)+10
g_drop_max = (e_lvl*30)+20



def cls():
    print('\n'*100)



def levelup(p_lvl):
    cls()
    print('''
       .-"```'.         Sweet! You Levelled up!
      /   \\    \\        
     /   / `\\__/        lvl ''',p_lvl,''' --> lvl ''',p_lvl+1,'''
     | .'  _  _|        
     \\(\\   6  6         + 3 Stat points
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          
_'     '-__ / `-_

''')
    
    return input('')


def run():
    print('''
they were strong, but you managed away to get away safely




''')
    return input()

def housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti):
    if p_statpt == 0:
        print('''
       .-"```'.         hp:''',p_hp,''' $''',money,''' ₭:''',kappas,'''
      /   \\    \\        view stats [1]
     /   / `\\__/        view inventory [2]
     | .'  _  _|        
     \\(\\   6  6 
      | \\   _\\ |        current weapon: ''',cur_wep,'''
      |\\ `~`= `/        current armour: ''',cur_arm,'''
      | '.___.'         current utility: ''',cur_uti,'''
  .'` \\     |_          leave home [4]
_'     '-__ / `-_

''')
    else:
        print('''
       .-"```'.         hp:''',p_hp,''' $''',money,''' ₭:''',kappas,'''
      /   \\    \\        view stats [1]
     /   / `\\__/        view inventory [2]
     | .'  _  _|        add stats [3] (''',p_statpt,''' skill pts)
     \\(\\   6  6 
      | \\   _\\ |        current weapon: ''',cur_wep,'''
      |\\ `~`= `/        current armour: ''',cur_arm,'''
      | '.___.'         current utility: ''',cur_uti,'''
  .'` \\     |_          leave home [4]
_'     '-__ / `-_

''')
    return input('')

def statups(p_str,p_stm,p_spd,p_max_hp,p_dmg_min,p_dmg_max,p_lvl,p_xp,p_max_hp_b):
    print('''            stat points : ''',p_statpt,'''
       .-"```'.         
      /   \\    \\        str : ''',p_str,''' [1 = +1]
     /   / `\\__/        stm : ''',p_stm,''' [2 = +1]
     | .'  _  _|        spd : ''',p_spd,''' [3 = +1]
     \\(\\   6  6         
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave stats [4]
_'     '-__ / `-_
''')
    return input()

def stat(p_str,p_stm,p_spd,p_max_hp,p_dmg_min,p_dmg_max,p_lvl,p_xp,p_crit_c):
    print('''
                        level ''',p_lvl,'''
                        exp : ''',p_xp,'''/''',p_xp_lvl,'''
       .-"```'.         max hp: ''',p_max_hp,'''
      /   \\    \\        str : ''',p_str,''' 
     /   / `\\__/        stm : ''',p_stm,'''
     | .'  _  _|        spd : ''',p_spd,'''
     \\(\\   6  6         crit : ''',p_crit_c,'''
      | \\   _\\ |        dmg : ''',p_dmg_min,''' - ''',p_dmg_max,'''
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave stats [1]
_'     '-__ / `-_
''')
    return input('')

def inventory(cur_wep,cur_arm,cur_uti):
    print('''
       .-"```'.         current weapon: ''',cur_wep,'''
      /   \\    \\        current armour: ''',cur_arm,'''
     /   / `\\__/        current utility: ''',cur_uti,'''
     | .'  _  _|        view items [1]
     \\(\\   6  6         view weapons [2]
      | \\   _\\ |        view armour [3]
      |\\ `~`= `/        view utility [4]
      | '.___.'         
  .'` \\     |_          leave inventory [5]
_'     '-__ / `-_
''')
    return input('')

def items(pot_n):
    if pot_n < 1:
        print('''
       .-"```'.         You have no items
      /   \\    \\        
     /   / `\\__/        
     | .'  _  _|        
     \\(\\   6  6         
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave items [1]
_'     '-__ / `-_
    ''')
    else:
                print('''
       .-"```'.         [1] potion x ''',pot_n,'''
      /   \\    \\        
     /   / `\\__/        
     | .'  _  _|        
     \\(\\   6  6         
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave items [2]
_'     '-__ / `-_
    ''')
    return input('')
    cls()

def weaps(Stick_t,Woodsword_t,Slingshot_t):
    print('''       .-"```'.         [1] Fist (+0 str)''')
    if Stick_t == True:
        print('''      /   \\    \\        [2] Stick (+1 str)''')
    else:
        print('''      /   \\    \\  ''')
    if Woodsword_t == True:
        print('''     /   / `\\__/        [3] Wood sword (+4 str)''')
    else:
        print('''     /   / `\\__/ ''')
    if Slingshot_t == True:
        print('''     | .'  _  _|        [4] Slingshot (+5 str +5 spd)''')
    else:
        print('''     | .'  _  _|        ''')
    print('''     \\(\\   6  6         
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave weapons [7]
_'     '-__ / `-_
''')
    return input()

def arms(Clothes_t,Leather_t,Chain_t):
    print('''
       .-"```'.         [1] Shirt (+0 str)''',end='')
    if Clothes_t == True:
        print('''
      /   \\    \\        [2] Clothes (+1 stm)''',end='')
    else:
        print('''
      /   \\    \\   ''',end='')
    if Leather_t == True:
        print('''
     /   / `\\__/        [3] Leather padding (+4 stm)''',end='')
    else:
        print('''
     /   / `\\__/  ''',end='')
    if Chain_t == True:
        print('''
     | .'  _  _|        [4] Chain mail (+10 stm)''',end = '')
    else:
        print('''
     | .'  _  _|''',end = '')
    print('''
     \\(\\   6  6         
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave armour [7]
_'     '-__ / `-_
''')
    return input()

def utility(Sandals_t,Shoes_t,Goggles_t):
    print('''
       .-"```'.         [1] Feet (+0 spd)''')
    if Sandals_t == True:
        print('''      /   \\    \\        [2] Sandals (+1 spd)''')
    else:
        print('''      /   \\    \\  ''')
    if Shoes_t == True:
        print('''     /   / `\\__/        [3] Shoes (+4 spd)''')
    else:
        print('''     /   / `\\__/ ''')
    if Goggles_t == True:
        print('''     | .'  _  _|        [4] Goggles (+5 str +5 spd)''')
    else:
        print('''     | .'  _  _|''')
    print('''     \\(\\   6  6         
      | \\   _\\ |        
      |\\ `~`= `/        
      | '.___.'         
  .'` \\     |_          leave utility [7]
_'     '-__ / `-_
''')
    return input()

def shopc(money,kappas,p_hp):
    print('''
|          |           $''',money,'''                hp:''',p_hp,'''
|          |           ₭: ''',kappas,'''           back [6]
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                               .---.                     |          |
|          |                     hey, i got               |     |                    |          |
|          |                     some cool           '-.__|_____|__.-'               |          |
|          |                     stuff for                |a  a |                    |          |
|          |                     pretty  cheap            |  L  |                    |          |
|          |                                              _\\ - /_                    |          |
|          |                                          _.-'\\_____/'-._                |          |
|          |                                         /  _         _  \\               |          |
|          |_______________                          | | |       | | |               |          |
|         /               /|                         | | |       | | |               |          |
|        /               / |                         | \\ |       | | |               |          |
|       /               /  |                          \\ \\|_______| | |               |          |
|      /               /   |                           \\_|__[x]__| |_|               |          |
|     /               /    |             ________________|_______|_|_|_______________|____      |
|    /               /     |____________/    __                                           \\     |
|   /               /      /           /     )(                                            \\    |
|  /               /      /           /     /  \\                                            \\   |
| /               /      /           /     (____)                                            \\  |
|/_______________/      /           /_________________________________________________________\\ |
||               |     /            |                                                          ||
||               |    /             |       [1]                                                ||
||               |   /              |       $15                                                ||
||               |  /               |       25%hp                                              ||
||               | /                |                                                          ||
||_______________|/_________________|__________________________________________________________||
''')
    return input('')

def nomoney():
    print('''
|          |           
|          |           
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                               .---.                     |          |
|          |                     YOU AINT                 |     |                    |          |
|          |                     GOT ENOUGH          '-.__|_____|__.-'               |          |
|          |                     MONEY FOR                |a  a |                    |          |
|          |                     THAT!                    |  L  |                    |          |
|          |                                              _\\ ^ /_                    |          |
|          |                                          _.-'\\_____/'-._                |          |
|          |                                         /  _         _  \\               |          |
|          |_______________                          | | |       | | |               |          |
|         /               /|                         | | |       | | |               |          |
|        /               / |                         | \\ |       | | |               |          |
|       /               /  |                          \\ \\|_______| | |               |          |
|      /               /   |                           \\_|__[x]__| |_|               |          |
|     /               /    |             ________________|_______|_|_|_______________|____      |
|    /               /     |____________/    __                                           \\     |
|   /               /      /           /     )(                                            \\    |
|  /               /      /           /     /  \\                                            \\   |
| /               /      /           /     (____)                                            \\  |
|/_______________/      /           /_________________________________________________________\\ |
||               |     /            |                                                          ||
||               |    /             |                                                          ||
||               |   /              |                                                          ||
||               |  /               |                                                          ||
||               | /                |                                                          ||
||_______________|/_________________|__________________________________________________________||
''')
    return input('')

def buyc(money,kappas,p_hp):
    print('''
|          |           $''',money,'''                hp:''',p_hp,'''
|          |           ₭: ''',kappas,'''           back [6]
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                                                         |          |
|          |                                               .---.                     |          |
|          |                     how many                 |     |                    |          |
|          |                     would you           '-.__|_____|__.-'               |          |
|          |                     like to buy?             |a  a |                    |          |
|          |                                              |  L  |                    |          |
|          |                                              _\\ - /_                    |          |
|          |                                          _.-'\\_____/'-._                |          |
|          |                                         /  _         _  \\               |          |
|          |_______________                          | | |       | | |               |          |
|         /               /|                         | | |       | | |               |          |
|        /               / |                         | \\ |       | | |               |          |
|       /               /  |                          \\ \\|_______| | |               |          |
|      /               /   |                           \\_|__[x]__| |_|               |          |
|     /               /    |             ________________|_______|_|_|_______________|____      |
|    /               /     |____________/    __                                           \\     |
|   /               /      /           /     )(                                            \\    |
|  /               /      /           /     /  \\                                            \\   |
| /               /      /           /     (____)                                            \\  |
|/_______________/      /           /_________________________________________________________\\ |
||               |     /            |                                                          ||
||               |    /             |       [1]                                                ||
||               |   /              |       $15                                                ||
||               |  /               |       25%hp                                              ||
||               | /                |                                                          ||
||_______________|/_________________|__________________________________________________________||
''')
    return input('')

def forgec(money,kappas,p_hp,Stick_t,Woodsword_t,Slingshot_t,Clothes_t,Leather_t,Chain_t,Sandals_t,Shoes_t,Goggles_t):
    print('''
                                                                                                 
                                                                                                 
  /        |          |         | |       ||_|_________|____    $''',money,'''  
 /         |          |         | |      /||_|_________|___ \    ''',kappas,'''
|          |          |         | |      \||_|_________|____/ hp:''',p_hp,'''
|          |          |         | |       || '         '                             |          |
|          |          |         | |                                   ______         |          |
|          |          |         | |                                .-' ____ '-.      |          |
|          |          |         | |                                \.-'    '-./      |          |
|          |          |         | |                 __|_________|___\        /       |          |
|          |          |         | |                |__|_________|___/        \       |          |
|          |          |         | |                   '         '  /'-.____.-'\      |          |
|          |    ______|         | |_______  "Hi! I'm a blacksmith."'-.______.-'      |          |
|          |   /      |_________|/       /\                                          |          |
|          |  /   o----                 / /                            ||            |          |
|          | /_________________________/ /                            /  \           |          |
|          |/__________________________\/                             \  /     ____  |          |
|          |                                                          .\/.    |____| |          |
|          |                                    _____                  /\      :||:  |          |
|          |              )                    / ~~~ \                /  \      ||   |          |
|          |             (                     \ `¿´ /               /    \     ||   |          |
|          |    _____)_________________      _.-\ - /-._            /      \         |          |
|          |   /  __(__________)____  /|  /¯¯¯¯/¯|¯|¯\¯¯¯¯\     _________________    |          |
|          |  /  :@@@@@@@@@@@@(@@@@: / | (  ´)|´  ¯  `|(´  )    \________________\   |          |
|          |  :. '-.@@@@@@@@@@@@.-' .: | |   ||       ||   |     \               /   |          |
|          |  : '.  '-.______.-'  .' : |  \   )|     |(   /       '-._________.-'    |          |
|          |__:   '-.__________.-'   : |___\==||_____||==/____|¯¯|_____||  |_________|          |
|         /   :     |----------|     : |---/  |+-----++:0+----|  |    .'|  |_         \         |
|        /    :     |----------|     :/'---UUUU+--+--+0000----|  |   |\.'__'.\         \        |
|       /     '-.   |----------|   .-'         |  |  |        |__|   \|______|          \       |
|      /         '-.|__________|.-'            |  |  |                                   \      |
|     /                                        |  |  |                                    \     |
''',end='')
    if Stick_t == False:
        print('''|    /        Buy stick [1] - $0               |__|__|                                     \    |
''',end='')
    elif Woodsword_t == False:
        print('''|    /        Buy Woodsword [1] - $200         |__|__|                                     \    |
''',end='')
    elif Slingshot_t == False:
        print('''|    /        Buy Slingshot [1] - $1000        |__|__|                                     \    |
''',end='')
    else:
        print('''|    /                                         |__|__|                                     \    |
''')
    if Clothes_t == False:
        print('''|   /         Buy clothing [2] - $0            (__|__)                                      \   |
''',end='')
    elif Leather_t == False:
        print('''|   /         Buy Leather padding [2] - $200   (__|__)                                      \   |
''',end='')
    elif Chain_t == False:
        print('''|   /         Buy Chain mail [2] - $1250       (__|__)                                      \   |
''',end='')
    else:
        print('''|   /                                          (__|__)                                      \   |
''',end='')
    if Sandals_t == False:
        print('''|  /          Buy Sandals [3] - $0                                                           \  |
''',end='')
    elif Shoes_t ==  False:
        print('''|  /          Buy Shoes [3] - $200                                                           \  |
''',end='')
    elif Goggles_t == False:
        print('''|  /          Buy Goggles [3] - $800                                                         \  |
''',end='')
    else:
        print('''|  /                                                                                         \  |
''',end='')
    print('''| /           Leave [4]                                                                       \ |
|/_____________________________________________________________________________________________\|
''',end='')
    return input()

def fnomoney():
    print('''
                                                                                                 
                                                                                                 
  /        |          |         | |       ||_|_________|____                         |        \  
 /         |          |         | |      /||_|_________|___ \                        |         \ 
|          |          |         | |      \||_|_________|____/                        |          |
|          |          |         | |       || '         '                             |          |
|          |          |         | |                                   ______         |          |
|          |          |         | |                                .-' ____ '-.      |          |
|          |          |         | |                                \.-'    '-./      |          |
|          |          |         | |                 __|_________|___\        /       |          |
|          |          |         | |                |__|_________|___/        \       |          |
|          |          |         | |                   '         '  /'-.____.-'\      |          |
|          |    ______|         | |_______"You can't afford that!" '-.______.-'      |          |
|          |   /      |_________|/       /\                                          |          |
|          |  /                         / /                            ||            |          |
|          | /_________________________/ /                            /  \           |          |
|          |/__________________________\/                             \  /     ____  |          |
|          |                                                          .\/.    |____| |          |
|          |                                    _____                  /\      :||:  |          |
|          |              )                    / ~~~ \                /  \      ||   |          |
|          |             (                     \ `¿´ /               /    \     ||   |          |
|          |    _____)_________________      _.-\ ^ /-._            /      \         |          |
|          |   /  __(__________)____  /|  /¯¯¯¯/¯|¯|¯\¯¯¯¯\     _________________    |          |
|          |  /  :@@@@@@@@@@@@(@@@@: / | (  ´)|´  ¯  `|(´  )    \________________\   |          |
|          |  :. '-.@@@@@@@@@@@@.-' .: | |   ||       ||   |     \               /   |          |
|          |  : '.  '-.______.-'  .' : |  \   )|     |(   /       '-._________.-'    |          |
|          |__:   '-.__________.-'   : |___\==||_____||==/____|¯¯|_____||  |_________|          |
|         /   :     |----------|     : |---/  |+-----++:0+----|  |    .'|  |_         \         |
|        /    :     |----------|     :/'---UUUU+--+--+0000----|  |   |\.'__'.\         \        |
|       /     '-.   |----------|   .-'         |  |  |        |__|   \|______|          \       |
|      /         '-.|__________|.-'            |  |  |                                   \      |
|     /                                        |  |  |                                    \     |
|    /                                         |__|__|                                     \    |
|   /                                          (__|__)                                      \   |
|  /                                                                                         \  |
| /                                                                                           \ |
|/_____________________________________________________________________________________________\|
''')
    noreply = input()

#######################################################################################################################################################################################################################
print('''

















                                                                                               ###########       ###########           #######
                                                                                               ##        ##      ##        ##        ##       ##
                                                                                               ##        ##      ##        ##      ##
                                                                                               ##        ##      ##        ##      ##
                                                                                               ##        ##      ##        ##      ##
                                                                                               ##        ##      ##        ##      ##    
                                                                                               ###########       ###########       ##     ####
                                                                                               ##    ##          ##                ##         ##
                                                                                               ##     ##         ##                ##         ##
                                                                                               ##      ##        ##                ##         ##
                                                                                               ##       ##       ##                ##         ##
                                                                                               ##        ##      ##                  ##       ##
                                                                                               ##        ##      ##                    #######

                                                                                -{================================@@@@=====================================}-
                                                                                                          [push enter to start]
                                                                                -{================================@@@@=====================================}-        
''')
noreplay = input()
cls()
print('''
 .~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 )                                                                                      )
 '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
  |  ^     ^                                                                            |
  |  +--+--+ any eons ago...  During the time while Dragons ruled this world, a certain |
  |  I  I  I young boy was sent to this realm for reasons unknown. Only an old Zeal     |
  |  I  I  I Druid was aware of this presence Descendance. Legend has it, that the boy  |
  |  I  I  I was delivered to the Druid by Demons. The Druid himself was old in age, but|
  |  strong in faith and wisdon, and therefore was not decieved by the Demons' presence,|
  |  instead, the druid welcomed the Demons as guests. This act of kindness heavily     |
  |  fractured the Demons and forced them to leave. Together, they have lived in        |
  |  Assonance for many years. The innocent boy, Xehspfe was left with the Druid, and he|
  |  then raised him like his own, Voluntarily.                                         |
  |                                                                                     |
  |                                                                                     |
  |                                                                                     |
  |                     %                   %                   %                       |  
  |                                                                                     |
  |                                                                                     |
  |  ---+--- o this day, no one knows what eventually happened to the Druid and the boy.|
  |     I    Many people believe that the Druid died of old age, but Incarnated himself |
  |     I    Into the grand forest Thenttkil, which could be a possible explanation for |
  |     I    the anomaly, 'living trees'. But no clues exist as to the missing case of  |                                    
  |  the boy. Some say the boy went into the Zealist ways, and also became a Druid,     |
  |  whilst others say he ran away and hides in the forest till today.                  |
  |                                                                                     |
  |  Fortunes, for you are playing as the one and only lost boy from the Zealot Druidism|
  |                                                                                     |
  |                                                                                     |
  |                                                                                     |
  |                                                                                     |                                                                                          
  |                     I PLEDGE TO FREE THE WORLD FROM DARKNESS                        |
  |                                                                                     |
  |                                                                                     |
 .vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv.
 )                                                                                      )
 '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ''')

noreply = input()
 
 
while True:
    cls()
    ui = maps.mapmain(money,p_hp)
    if ui == '1':
        cls()
        vi = maps.villagemap(money,p_hp)
        village = True
    elif ui == '2':
        Farm = True
    elif ui == '3':
        cls()
        di = maps.desertmap(money,p_hp)
        desert = True
    elif ui == 'admin58859****478':
        cls()
        money = 10000000000000
        kappas = 10000000000000
        p_str_b = 5000
        p_stm_b = 5000
        p_spd_b = 5000
        p_str = 5000
        p_stm = 5000
        p_spd = 5000
        p_max_hp_b = p_stm*5
        p_max_hp = p_max_hp_b
        p_hp = p_max_hp
        p_dmg_min = p_str+2
        p_dmg_max = math.ceil(p_str*1.3+5)
        p_crit_c = p_spd/100
        p_lvl = 'ADMIN'
        p_xp_lvl = 9999999999999999999999
        p_statpt = 99999
        cls()
        noreply = input('Welcome, Admin.')
    elif ui == 'David' and David == False:
        cls()
        p_str_b += 2
        p_stm_b += 2
        p_str += 2
        p_stm += 2
        p_max_hp_b = p_stm*5
        p_max_hp = p_max_hp_b
        p_hp = p_max_hp
        p_dmg_min = p_str+2
        p_dmg_max = math.ceil(p_str*1.3+5)
        David = True
        cls()
        noreply = input('Hello David.')
    elif ui == 'Xehspfe' or ui == 'Xehspfe' and Xehspfe == False:
        p_str_b += 5
        p_spd_b += 1
        p_str += 5
        p_spd += 1
        p_dmg_min = p_str+2
        p_dmg_max = math.ceil(p_str*1.3+5)
        p_crit_c = p_spd/100
        Xehspfe = True
        cls()
        noreply = input ('Xehspfe, is this really you?')
    elif ui == 'Thenttkil' or ui == 'Thenttkil' and Thenttkil == False:
        p_stm_b += 5
        p_stm += 5
        p_spd_b += 1
        p_spd += 1
        p_crit_c = p_spd/100
        p_max_hp_b = p_stm*5
        p_max_hp = p_max_hp_b
        p_hp = p_max_hp
        Thenttkil = True
        cls()
        noreply = input('Welcome to the grand frorest')
    elif ui == 'Spare me some cash pls':
        money += 1
        cls()
        noreply = input('Wow, you suck for using this code')
    elif ui == 'Grand knowledge' and GK == False:
        cls()
        GK= True
        cls()
        noreply = input("Thanks for reading the Grand knowledge, here's an exp tome")
        cls()
        levelup(p_lvl)
        p_lvl += 1
        p_statpt += 3
    else:
        noreply = input('something went wrong . IDK         :/')
        cls()
    while village == True:
        if vi == '1':
            cls()
            hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
            house = True
        elif vi == '2':
            cls()
            si = shopc(money,kappas,p_hp)
            shop = True
        elif vi == '4':
            cls()
            forge = True
        elif vi == '3':
            cls()
            inn = True
        elif vi == '7':
            village = False
            cls()
        else:
            noreply = input('something went wrong . IDK         :/')
            cls()
            vi = maps.villagemap(money,p_hp)
        while house == True:
            if hi == '1':
                stats = True
                cls()
                si = stat(p_str,p_stm,p_spd,p_max_hp,p_dmg_min,p_dmg_max,p_lvl,p_xp,p_crit_c)
                if si == '1':
                    stats = False
                    cls()
                    hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                else:
                    noreply = input('something went wrong . IDK         :/')
                    cls()
            elif hi == '2':
                inventoryc = True
                cls()
                ii = inventory(cur_wep,cur_arm,cur_uti)
                if ii == '1':
                    item = True
                    cls()
                    iii = items(pot_n)
                    if iii == '2':
                        item = False
                    elif iii == '1':
                        if p_hp+(math.ceil(p_max_hp*.25)) > p_max_hp:
                            p_hp = p_max_hp
                            pot_n -= 1
                        else:
                            p_hp+=(math.ceil(p_max_hp*.25))
                            pot_n -=1
                    else:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                        cls()
                        iii = items(pot_n)
                        if iii == '1':
                            t = True
                elif ii == '2':
                    weps = True
                    cls()
                    wi = weaps(Stick_t,Woodsword_t,Slingshot_t)
                    if wi == '1':
                        cls()
                        noreply = input('you equip... fist?')
                        cur_wep = 'Your Fist'
                        p_str = p_str_b
                        p_dmg_min = p_str+2
                        p_dmg_max = math.ceil(p_str*1.3+5)
                        if p_spd_b_w >0:
                            p_spd_b_w = -p_spd_b_w
                        p_spd+=p_spd_b_w
                        p_crit_c = p_spd/100
                        cls()
                    elif wi == '2':
                        if Stick_t == True:
                            cls()
                            noreply = input('you equip stick')
                            cur_wep = 'Stick'
                            p_str = p_str_b
                            p_str += Stick
                            p_dmg_min = p_str+2
                            p_dmg_max = math.ceil(p_str*1.3+5)
                            if p_spd_b_w >0:
                                p_spd_b_w = -p_spd_b_w
                            p_spd+=p_spd_b_w
                            p_crit_c = p_spd/100
                            cls()
                    elif wi == '3':
                        if Woodsword_t == True:
                            cls()
                            noreply = input('you equip Wooden Sword')
                            cur_wep = 'Wooden Sword'
                            p_str = p_str_b
                            p_str += Woodsword
                            p_dmg_min = p_str+2
                            p_dmg_max = math.ceil(p_str*1.3+5)
                            if p_spd_b_w >0:
                                p_spd_b_w = -p_spd_b_w
                            p_spd+=p_spd_b_w
                            p_crit_c = p_spd/100
                            cls()
                    elif wi == '4':
                        if Slingshot_t == True:
                            cls()
                            noreply = input('you equip Slingshot')
                            cur_wep = 'Slingshot'
                            p_str = p_str_b
                            p_str += Slingshot
                            p_dmg_min = p_str+2
                            p_crit_c = p_spd/100
                            if p_spd_b_w !=5:
                                p_spd_b_w = 5
                            p_spd+=p_spd_b_w
                            p_crit_c = p_spd/100
                            cls()
                    elif wi == '7':
                        print()
                elif ii == '3':
                    arm = True
                    cls()
                    ai = arms(Clothes_t,Leather_t,Chain_t)
                    if ai == '1':
                        cls()
                        noreply = input('you equip shirt.')
                        cur_arm = 'Your shirt'
                        p_max_hp = p_max_hp_b
                        p_stm = p_stm_b
                        if p_hp+Shirt*5 <= p_max_hp:
                            p_hp += Shirt*5
                        elif p_hp> p_max_hp:
                            p_hp = p_max_hp
                        cls()
                    elif ai == '2':
                        if Clothes_t == True:
                            cls()
                            noreply = input('you equip Clothes.')
                            cur_arm = 'Clothes'
                            p_stm = p_stm_b
                            p_stm += Clothes
                            p_max_hp = p_stm*5
                            if p_hp+Clothes*5 <= p_max_hp:
                                p_hp += Clothes*5
                            elif p_hp> p_max_hp:
                                p_hp = p_max_hp
                            cls()
                    elif ai == '3':
                        if Leather_t == True:
                            cls()
                            noreply = input('you equip Leather padding.')
                            cur_arm = 'Leather pads'
                            p_stm = p_stm_b
                            p_stm += Leather
                            p_max_hp = p_stm*5
                            if p_hp+Leather*5 <= p_max_hp:
                                p_hp += Leather*5
                            elif p_hp> p_max_hp:
                                p_hp = p_max_hp
                            cls()
                    elif ai == '4':
                        if Chain_t == True:
                            cls()
                            noreply = input('you equip Chain mail.')
                            cur_arm = 'Chain mail'
                            p_stm = p_stm_b
                            p_stm += Chain
                            p_max_hp = p_stm*5
                            if p_hp+Chain*5 <= p_max_hp:
                                p_hp += Chain*5
                            elif p_hp> p_max_hp:
                                p_hp = p_max_hp
                            cls()
                    elif ai == '7':
                        print('')
                elif ii == '4':
                    uti = True
                    cls()
                    ui = utility(Sandals_t,Shoes_t,Goggles_t)
                    if ui == '1':
                        cls()
                        noreply = input('you equip your Feet ??')
                        cur_uti = 'Your Feet'
                        if p_spd_b_u != 0:
                            p_spd_b_u = -p_spd_b_u
                        p_spd += p_spd_b_u
                        p_crit_c = p_spd/100
                    elif ui == '2':
                        if Sandals_t == True:
                            cls()
                            noreply = input('you equip Sandals.')
                            cur_uti = 'Your Sandals'
                            if p_spd_b_u != Sandals:
                                p_spd_b_u = -p_spd_b_u
                            p_spd += p_spd_b_u + Sandals
                            p_crit_c = p_spd/100
                    elif ui == '3':
                        if Shoes_t == True:
                            cls()
                            noreply = input('you equip Shoes.')
                            cur_uti = 'Your Shoes'
                            if p_spd_b_u != Shoes:
                                p_spd_b_u = -p_spd_b_u
                            p_spd += p_spd_b_u + Shoes
                            p_crit_c = p_spd/100
                    elif ui == '4':
                        if Goggles_t == True:
                            cls()
                            noreply = input('you equip Goggles. Smexy.')
                            cur_uti = 'Your Goggles'
                            if p_spd_b_u != Goggles:
                                p_spd_b_u = -p_spd_b_u + Goggles
                            p_spd += p_spd_b_u
                            p_crit_c = p_spd/100
                    else:
                        print('')
                elif ii == '5':
                    cls()
                    hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                else:
                    noreply = input('something went wrong . IDK         :/')
                    cls()
            elif hi == '3':
                if p_statpt > 0:
                    stats = True
                else:
                    cls()
                    noreply = input('you have no stat points... -__-')
                    cls()
                    hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                    cls()
                while stats == True:
                    cls()
                    statin = statups(p_str,p_stm,p_spd,p_max_hp,p_dmg_min,p_dmg_max,p_lvl,p_xp,p_max_hp_b)
                    cls()
                    if statin == '1':
                        p_str_b += 1
                        p_str += 1
                        p_dmg_min = p_str+2
                        p_dmg_max = math.ceil(p_str*1.3+5)
                        p_statpt -=1
                        if p_statpt == 0:
                            stats = False
                            hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                    elif statin == '2':
                        p_stm_b +=1
                        p_stm +=1
                        p_max_hp_b = p_stm*5
                        p_max_hp = p_max_hp_b
                        p_hp += 5
                        p_statpt -=1
                        if p_statpt == 0:
                            stats = False
                            hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                    elif statin == '3':
                        p_spd_b +=1
                        p_spd += 1
                        p_crit_c = p_spd/100
                        p_statpt -=1
                        if p_statpt == 0:
                            stats = False
                            hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                    elif statin == '4':
                        stats = False
                        cls()
                        hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
                        cls()
                    if p_statpt == 0:
                        stats = False
            elif hi == '4':
                cls()
                vi = maps.villagemap(money,p_hp)
                cls()
                house = False
            else:
                noreply = input('something went wrong . IDK         :/')
                cls()
                hi = housec(p_hp,money,kappas,cur_wep,cur_arm,p_statpt,cur_uti)
        while shop == True:
            if si == '1':
                cls()
                if money < 15:
                    nomoney()
                    shop = False
                else:
                    while True:
                        try:
                            no = buyc(money,kappas,p_hp)
                            if no.isalpha() or no < '0':
                                raise ValueError
                            break
                        except ValueError:
                            cls()
                            noreply = input('something went wrong . IDK         :/')
                    no = int(no)
                    if no*15 > money:
                        cls()
                        nomoney()
                        cls()
                        shop = False
                    else:
                        money -= no*15
                        pot_n += no
                        shop = False
            elif si == '6':
                cls()
                shop = False
                vi = maps.villagemap(money,p_hp)
                cls()
            else:
                cls()
                noreply = input('something went wrong . IDK         :/')
                cls()
                si = shopc(money,kappas,p_hp)
        while forge == True:
            cls()
            fi = forgec(money,kappas,p_hp,Stick_t,Woodsword_t,Slingshot_t,Clothes_t,Leather_t,Chain_t,Sandals_t,Shoes_t,Goggles_t)
            if fi == '1':
                if Stick_t == False:
                    Stick_t = True
                elif Woodsword_t == False:
                    if money <200:
                        cls()
                        fnomoney()
                    else:
                        money -=200
                        Woodsword_t = True
                elif Slingshot_t == False:
                    if money <1000:
                        cls()
                        fnomoney()
                    else:
                        money -=1000
                        Slingshot_t = True
            elif fi == '2':
                if Clothes_t == False:
                    Clothes_t = True
                elif Leather_t == False:
                    if money <200:
                        cls()
                        fnomoney()
                    else:
                        money -=200
                        Leather_t = True
                elif Chain_t == False:
                    if money <1250:
                        cls()
                        fnomoney()
                    else:
                        money -=1250
                        Chain_t = True 
            elif fi == '3':
                if Sandals_t == False:
                    Sandals_t = True
                elif Shoes_t == False:
                    if money <200:
                        cls()
                        fnomoney()
                    else:
                        money -=200
                        Shoes_t = True
                elif Goggles_t == False:
                    if money <800:
                        cls()
                        fnomoney()
                    else:
                        money -=800
                        Goggles_t = True
            elif fi == '4':
                cls()
                vi = maps.villagemap(money,p_hp)
                forge = False
            else:
                cls()
                noreply = input('something went wrong . IDK         :/')
                cls()
        while inn == True:
            cls()
            ic = maps.innc(money,kappas)
            cls()
            if ic == '1':
                cls()
                gi = maps.guyi(money,kappas,Task)
                cls()
                if gi == '1':
                    cls()
                    noreply = maps.guywho(money,kappas)
                    cls()
                elif gi == '2':
                    if Task == False:
                        tn = random.randint(1,5)
                        cls()
                        task = maps.guytask(money,kappas,tn)
                        cls()
                        if task == '1':
                            Task = True
                            if tn == 1:
                                TaskCact = True
                                ob = 0
                            elif tn == 2:
                                TaskCoyo = True
                                ob = 0
                            elif tn == 3:
                                TaskSpid = True
                                ob = 0
                            elif tn == 4:
                                TaskSnek = True
                                ob = 0
                            elif tn == 5:
                                TaskCam = True
                                ob = 0
                    else:
                        vti = maps.viewtask(money,kappas,ob,TaskCact,TaskCoyo,TaskSpid,TaskSnek,TaskCam)
                        if vti == '1' and TaskCact == True and ob == 10:
                            cls()
                            print('''
an extra $150 land in your pocket. :)



''')
                            noreply = input()
                            money += 150
                            Task = False
                            TaskCact = False
                        elif vti == '1' and TaskCoyo == True and ob == 8:
                            cls()
                            print('''
an extra $300 land in your pocket. :)



''')
                            noreply = input()
                            money += 300
                            Task = False
                            TaskCoyo = False
                        elif vti == '1' and TaskSpid == True and ob == 6:
                            cls()
                            print('''
an extra $450 land in your pocket. :)



''')
                            noreply = input()
                            money += 450
                            Task = False
                            TaskSpid = False
                        elif vti == '1' and TaskSnek == True and ob == 4:
                            cls()
                            print('''
an extra $650 land in your pocket. :)



''')
                            noreply = input()
                            money += 650
                            Task = False
                            TaskSnek = False
                        elif vti == '1' and TaskCam == True and ob == 2:
                            cls()
                            print('''
an extra $1000 land in your pocket. :)



''')
                            noreply = input()
                            money += 1000
                            Task = False
                            TaskCam = False
                        elif vti == '2':
                            inn = False
                            cls()
                elif gi == '3':
                    cls()
                    inn=False
                    cls()
                else:
                    cls()
                    noreply = input('something went wrong . IDK         :/')
                    cls()
            elif ic == '2':
                bi = maps.bartender()
                if bi == '1':
                    jokeno = random.randint(1,7)
                    coolometer+= 1
                    if jokeno == 1:
                        cls()
                        noreply = input('''Joke? okay! umm...

"Chuck Norris throws a grenade and it kills 20 people. Then it explodes."


''')
                    elif jokeno == 2:
                        cls()
                        noreply = input('''Joke? okay! umm...

Dave's PC is starting to get slow so he went to an electronic specialist and asks "How do you make your computer go faster?"

The Specialist replies "Draw racing strips on it and attatch a spoiler"


''')
                    elif jokeno == 3:
                        cls()
                        noreply = input('''Joke? okay! umm...

Timothy just came back home after a terrible ad at school, as he messed up on one of the question
on an exam. so he goes to his asian father and tells him.

The father answers "If at first you don't succseed, don't come back home"


''')
                    elif jokeno == 4:
                        cls()
                        noreply = input('''Joke? okay! umm...

Sarah: Dorothy, you're too old for this.
Dorothy: Bah! age is just a number...
Sarah : Age is just a number? False, age is a word"


''')
                    elif jokeno == 5:
                        cls()
                        noreply = input('''Joke? okay! umm...

Han as a youngster was always into cosplay but never got a chance to go to a real
convention before, now, an opportunity as opened up as LoL Con is starting soon near his town.
On the day, Han puts on his cosplay costume and goes to the convention. Inside, the Leader of the convention,
Jhon McDirivative, is in absolute shock at what he sees.
"Who in the world dragged this huge boulder into the building?! Remove it at once!" He screams.
Han turns around and says "What, why? But i'm cosplaying malphite!"


''')
                    elif jokeno == 6:
                        cls()
                        noreply = input('''Joke? okay! umm...

Clarence comes back home late, and his asian father is very disapointed.
Father: Why are you late?
Clarence: I forgot my homework
Father: You forget to study, I forget to feed you.


''')
                    elif jokeno == 7:
                        cls()
                        noreply = input('''Joke? okay! umm...

"


''')
                    if coolometer == 10:
                        cls()
                        maps.barthappy()
                        money += 500
                elif bi == '2':
                    inn = False
                else:
                    cls()
                    noreply = input('something went wrong . IDK         :/')
                    cls()
            elif ic == '3':
                inn=False
                vi = maps.villagemap(money,p_hp)
            else:
                cls()
                noreply = input('something went wrong . IDK         :/')
                cls()
    while Farm == True:
        cls()
        fi = maps.farmap(money,p_hp)
        cls()
        if fi == '1':
            cls()
            omi = maps.oldman(money,p_hp)
            cls()
            if omi == '1':
                while True:
                    try:
                        cls()
                        much = input('''

how much would you like to invest? (enter $$$ number)

You are investing :''')
                        if much.isalpha() :
                            raise ValueError
                        break
                    except ValueError:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                if much > money:
                    print('''

You aint got enough, son

''')
                else:
                    investmoney += much
                    time = 0
                    print('''

Thanks for investing, you will make some profit soon.

''')
    while desert == True:
        if di == '1':
            desert = False
            cls()
        elif di == '2':
            if Cactus == False:
                name_n = random.randint(1,5)
            cls()
            if name_n == 1:
                name = 'spiky cactus'
                if Cactus == False:
                    e_lvl = 1
                    e_spd = (0.85*e_lvl)
                    e_max_hp = 18*e_lvl
                    e_hp = e_max_hp
                    e_dmg_min = math.ceil(1*(1.5*e_lvl))
                    e_dmg_max = math.ceil(1.5*(1.5*e_lvl)+2)
                    e_crit_c = e_spd/100
                    xp_drop = math.ceil((e_lvl*2.25)+5)
                    g_drop_min = (e_lvl*15)+10
                    g_drop_max = (e_lvl*30)+20
                    Cactus = True
                while Cactus == True:
                    ci = cactusbattle.cactus(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max)
                    cls()
                    if ci == '1':
                        iscrit = random.randint(0,100)
                        if iscrit <= p_crit_c*100:
                            crit = True
                            damage = (random.randint(p_dmg_min,p_dmg_max))*1.5
                            cactusbattle.attack_cact_crit(damage)
                        else:
                            damage = random.randint(p_dmg_min,p_dmg_max)
                            cactusbattle.attack_cact(damage)
                        e_hp = e_hp - damage
                        cls()
                        edamage = random.randint(e_dmg_min,e_dmg_max)
                        p_hp -= edamage
                        cls()
                        cactusbattle.cactushit(edamage)
                        cls()
                        if e_hp <= 0:
                            if p_hp <= 0:
                                defea = True
                                while defea == True:
                                    cls()
                                    defe = maps.defeated(money,p_lvl)
                                    if defe == '2':
                                        quit()
                                        exit()
                                    elif defe == '1':
                                        if money < p_lvl*250:
                                            noreply = input('''
Your money cannot bring your life back...
        ''')
                                        else:
                                            money-=p_lvl*250
                                            p_hp = p_max_hp
                                            defea = False
                                            Cactus = False
                                            desert = False
                            g_drop = random.randint(g_drop_min,g_drop_max)
                            money += g_drop
                            p_xp += xp_drop
                            cls()
                            cactusbattle.cactus_dead(xp_drop,g_drop,ob,Cacti,TaskCact)
                            if TaskCact == True and ob < Cacti:
                                ob+=1
                            if p_xp >= p_xp_lvl:
                                p_xp = 0
                                p_xp_lvl = math.ceil(p_xp_lvl*1.25)
                                p_statpt += 3
                                levelup(p_lvl)
                                p_lvl += 1
                            Cactus = False
                            cls()
                            di = maps.desertmap(money,p_hp)
                            cls()
                        if p_hp <= 0:
                            defea = True
                            while defea == True:
                                cls()
                                if defe == '2':
                                    quit()
                                    exit()
                                elif defe == '1':
                                    if money < p_lvl*250:
                                        noreply = input('''
    Your money cannot bring your life back...
    ''')
                                    else:
                                        money-=p_lvl*250
                                        p_hp = p_max_hp
                                        defea = False
                                        Cactus = False
                                        desert = False
                    elif ci == '2':
                        cls()
                        item_input = items(pot_n)
                        cls()
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                    elif ci =='3':
                        run()
                        Cactus = False
                        cls()
                        di = maps.desertmap(money,p_hp)
                    else:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                        cls()
            elif name_n == 2:
                name = 'wild coyote'
                if Coyote == False:
                    e_lvl = 2
                    e_spd = (0.85*e_lvl)
                    e_max_hp = 18*e_lvl
                    e_hp = e_max_hp
                    e_dmg_min = math.ceil(1*(1.5*e_lvl))
                    e_dmg_max = math.ceil(1.5*(1.5*e_lvl)+2)
                    e_crit_c = e_spd/100
                    xp_drop = math.ceil((e_lvl*2.25)+5)
                    g_drop_min = (e_lvl*15)+10
                    g_drop_max = (e_lvl*30)+20
                    Coyote = True
                while Coyote == True:
                    cls()
                    ci = coyotebattle.coyote(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max)
                    Coyote = True
                    cls()
                    if ci == '1':
                        iscrit = random.randint(0,100)
                        if iscrit <= p_crit_c*100:
                            crit = True
                            damage = (random.randint(p_dmg_min,p_dmg_max))*1.5
                            coyotebattle.attack_coyote_crit(damage)
                        else:
                            damage = random.randint(p_dmg_min,p_dmg_max)
                            coyotebattle.attack_coyo(damage)
                        e_hp -= damage
                        cls()
                        edamage = random.randint(e_dmg_min,e_dmg_max)
                        p_hp -= edamage
                        cls()
                        coyotebattle.coyohit(edamage)
                        if e_hp <= 0:
                            if p_hp <= 0:
                                defea = True
                                while defea == True:
                                    cls()
                                    defe = maps.defeated(money,p_lvl)
                                    if defe == '2':
                                        quit()
                                        exit()
                                    elif defe == '1':
                                        if money < p_lvl*250:
                                            noreply = input('''
Your money cannot bring your life back...
        ''')
                                        else:
                                            money-=p_lvl*250
                                            p_hp = p_max_hp
                                            defea = False
                                            Coyote = False
                                            desert = False
                            g_drop = random.randint(g_drop_min,g_drop_max)
                            money += g_drop
                            p_xp += xp_drop
                            cls()
                            coyotebattle.coyote_dead(xp_drop,g_drop,TaskCoyo,ob,Coyo_Fur)
                            if TaskCoyo == True and ob < Coyo_fur:
                                ob+=1
                            if p_xp >= p_xp_lvl:
                                p_xp = 0
                                p_xp_lvl = math.ceil(p_xp_lvl*1.25)
                                p_statpt += 3
                                levelup(p_lvl)
                                p_lvl += 1
                            Coyote = False
                            cls()
                            di = maps.desertmap(money,p_hp)
                            cls()
                        if p_hp <= 0:
                            defea = True
                            while defea == True:
                                cls()
                                defe = maps.defeated(money,p_lvl)
                                if defe == '2':
                                    quit()
                                    exit()
                                elif defe == '1':
                                    if money < p_lvl*250:
                                        noreply = input('''
    Your money cannot bring your life back...
    ''')
                                    else:
                                        money-=p_lvl*250
                                        p_hp = p_max_hp
                                        defea = False
                                        Coyote = False
                                        desert = False
                    elif ci == '2':
                        cls()
                        item_input = items(pot_n)
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                    elif ci =='3':
                        run()
                        Coyote = False
                        cls()
                        di = maps.desertmap(money,p_hp)
                    else:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                        cls()
                cls()
            elif name_n == 3:
                name = 'venomous spider'
                e_lvl = 3
                e_spd = (0.85*e_lvl)
                e_max_hp = 18*e_lvl
                e_hp = e_max_hp
                e_dmg_min = math.ceil(1*(1.5*e_lvl))
                e_dmg_max = math.ceil(1.5*(1.5*e_lvl)+2)
                e_crit_c = e_spd/100
                xp_drop = math.ceil((e_lvl*2.25)+5)
                g_drop_min = (e_lvl*15)+10
                g_drop_max = (e_lvl*30)+20
                Spider = True
                while Spider == True:
                    cls()
                    si = spiderbattle.spider(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max)
                    Spider = True
                    cls()
                    if si == '1':
                        iscrit = random.randint(0,100)
                        if iscrit <= p_crit_c*100:
                            crit = True
                            damage = (random.randint(p_dmg_min,p_dmg_max))*1.5
                            spiderbattle.attack_spid_crit(damage)
                        else:
                            damage = random.randint(p_dmg_min,p_dmg_max)
                            spiderbattle.attack_spider(damage)
                        e_hp -= damage
                        cls()
                        edamage = random.randint(e_dmg_min,e_dmg_max)
                        p_hp -= edamage
                        cls()
                        spiderbattle.spiderhit(edamage)
                        if e_hp <= 0:
                            if p_hp <= 0:
                                defea = True
                                while defea == True:
                                    cls()
                                    defe = maps.defeated(money,p_lvl)
                                    if defe == '2':
                                        quit()
                                        exit()
                                    elif defe == '1':
                                        if money < p_lvl*250:
                                            noreply = input('''
Your money cannot bring your life back...
        ''')
                                        else:
                                            money-=p_lvl*250
                                            p_hp = p_max_hp
                                            defea = False
                                            Spider = False
                                            desert = False
                            g_drop = random.randint(g_drop_min,g_drop_max)
                            money += g_drop
                            p_xp += xp_drop
                            cls()
                            spiderbattle.spider_dead(xp_drop,g_drop,TaskSpid,ob,Spooder_Kills)
                            if TaskSpid == True and ob < Spooder_Kills:
                                ob+=1
                            if p_xp >= p_xp_lvl:
                                p_xp = 0
                                p_xp_lvl = math.ceil(p_xp_lvl*1.25)
                                p_statpt += 3
                                levelup(p_lvl)
                                p_lvl += 1
                            Spider = False
                            cls()
                            di = maps.desertmap(money,p_hp)
                            cls()
                        if p_hp <= 0:
                            defea = True
                            while defea == True:
                                cls()
                                defe = maps.defeated(money,p_lvl)
                                if defe == '2':
                                    quit()
                                    exit()
                                elif defe == '1':
                                    if money < p_lvl*250:
                                        noreply = input('''
    Your money cannot bring your life back...
    ''')
                                    else:
                                        money-=p_lvl*250
                                        p_hp = p_max_hp
                                        defea = False
                                        Spider = False
                                        desert = False
                    elif si == '2':
                        cls()
                        item_input = items(pot_n)
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                    elif si =='3':
                        run()
                        Spider = False
                        cls()
                        di = maps.desertmap(money,p_hp)
                    else:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                        cls()
                cls()
            elif name_n == 4:
                name = 'deadly snake'
                e_lvl = 4
                e_spd = (0.85*e_lvl)
                e_max_hp = 18*e_lvl
                e_hp = e_max_hp
                e_dmg_min = math.ceil(1*(1.5*e_lvl))
                e_dmg_max = math.ceil(1.5*(1.5*e_lvl)+2)
                e_crit_c = e_spd/100
                xp_drop = math.ceil((e_lvl*2.25)+5)
                g_drop_min = (e_lvl*15)+10
                g_drop_max = (e_lvl*30)+20
                Snake = True
                while Snake == True:
                    cls()
                    si = snakebattle.snake(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max)
                    Snake = True
                    cls()
                    if si == '1':
                        iscrit = random.randint(0,100)
                        if iscrit <= p_crit_c*100:
                            crit = True
                            damage = (random.randint(p_dmg_min,p_dmg_max))*1.5
                            snakebattle.attack_snake_crit(damage)
                        else:
                            damage = random.randint(p_dmg_min,p_dmg_max)
                            snakebattle.attack_snake(damage)
                        e_hp -= damage
                        cls()
                        edamage = random.randint(e_dmg_min,e_dmg_max)
                        p_hp -= edamage
                        cls()
                        snakebattle.snakehit(edamage)
                        if e_hp <= 0:
                            if p_hp <= 0:
                                defea = True
                                while defea == True:
                                    cls()
                                    defe = maps.defeated(money,p_lvl)
                                    if defe == '2':
                                        quit()
                                        exit()
                                    elif defe == '1':
                                        if money < p_lvl*250:
                                            noreply = input('''
Your money cannot bring your life back...
        ''')
                                        else:
                                            money-=p_lvl*250
                                            p_hp = p_max_hp
                                            defea = False
                                            Snake = False
                                            desert = False
                            g_drop = random.randint(g_drop_min,g_drop_max)
                            money += g_drop
                            p_xp += xp_drop
                            cls()
                            snakebattle.snake_dead(xp_drop,g_drop,TaskSnek,ob,Venom)
                            if TaskSnek == True and ob < Venom:
                                ob+=1
                            if p_xp >= p_xp_lvl:
                                p_xp = 0
                                p_xp_lvl = math.ceil(p_xp_lvl*1.25)
                                p_statpt += 3
                                levelup(p_lvl)
                                p_lvl += 1
                            Snake = False
                            cls()
                            di = maps.desertmap(money,p_hp)
                            cls()
                        if p_hp <= 0:
                            defea = True
                            while defea == True:
                                cls()
                                defe = maps.defeated(money,p_lvl)
                                if defe == '2':
                                    quit()
                                    exit()
                                elif defe == '1':
                                    if money < p_lvl*250:
                                        noreply = input('''
    Your money cannot bring your life back...
    ''')
                                    else:
                                        money-=p_lvl*250
                                        p_hp = p_max_hp
                                        defea = False
                                        Snake = False
                                        desert = False
                    elif si == '2':
                        cls()
                        item_input = items(pot_n)
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1': 
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                    elif si =='3':
                        run()
                        Snake = False
                        cls()
                        di = maps.desertmap(money,p_hp)
                    else:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                        cls()
                cls()
            elif name_n == 5:
                name = 'crazy camel'
                e_lvl = 5
                e_spd = (0.85*e_lvl)
                e_max_hp = 18*e_lvl
                e_hp = e_max_hp
                e_dmg_min = math.ceil(1*(1.5*e_lvl))
                e_dmg_max = math.ceil(1.5*(1.5*e_lvl)+2)
                e_crit_c = e_spd/100
                xp_drop = math.ceil((e_lvl*3.25)+5)
                g_drop_min = (e_lvl*15)+10
                g_drop_max = (e_lvl*30)+20
                Camel = True
                while Camel == True:
                    cls()
                    si = camelbattle.camel(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max)
                    Snake = True
                    cls()
                    if si == '1':
                        iscrit = random.randint(0,100)
                        if iscrit <= p_crit_c*100:
                            crit = True
                            damage = (random.randint(p_dmg_min,p_dmg_max))*1.5
                            camelbattle.attack_camel_crit(damage)
                        else:
                            damage = random.randint(p_dmg_min,p_dmg_max)
                            camelbattle.attack_camel(damage)
                        e_hp -= damage
                        cls()
                        edamage = random.randint(e_dmg_min,e_dmg_max)
                        p_hp -= edamage
                        p_hp -= edamage/2
                        cls()
                        camelbattle.camelhit(edamage)
                        if e_hp <= 0:
                            if p_hp <= 0:
                                defea = True
                                while defea == True:
                                    cls()
                                    defe = maps.defeated(money,p_lvl)
                                    if defe == '2':
                                        quit()
                                        exit()
                                    elif defe == '1':
                                        if money < p_lvl*250:
                                            noreply = input('''
Your money cannot bring your life back...
        ''')
                                        else:
                                            money-=p_lvl*250
                                            p_hp = p_max_hp
                                            defea = False
                                            Camel = False
                                            desert = False
                            g_drop = random.randint(g_drop_min,g_drop_max)
                            money += g_drop
                            p_xp += xp_drop
                            cls()
                            camelbattle.camel_dead(xp_drop,g_drop,TaskCam,ob,Camel_Souls)
                            if TaskCam == True and ob < Camel_Souls:
                                ob+=1
                            if p_xp >= p_xp_lvl:
                                p_xp = 0
                                p_xp_lvl = math.ceil(p_xp_lvl*1.25)
                                p_statpt += 3
                                levelup(p_lvl)
                                p_lvl += 1
                            Camel = False
                            cls()
                            di = maps.desertmap(money,p_hp)
                            cls()
                        if p_hp <= 0:
                            defea = True
                            while defea == True:
                                cls()
                                defe = maps.defeated(money,p_lvl)
                                if defe == '2':
                                    quit()
                                    exit()
                                elif defe == '1':
                                    if money < p_lvl*250:
                                        noreply = input('''
    Your money cannot bring your life back...
    ''')
                                    else:
                                        money-=p_lvl*250
                                        p_hp = p_max_hp
                                        defea = False
                                        Camel = False
                                        desert = False
                    elif si == '2':
                        cls()
                        item_input = items(pot_n)
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                        if pot_n > 0:
                            if item_input == '1':
                                if pot_n > 0:
                                    pot_n-=1
                                    if p_hp + (.15*p_max_hp) > p_max_hp:
                                        p_hp = p_max_hp
                                    else:
                                        p_hp += (p_max_hp*.15)
                                else:
                                    cls()
                                    noreply = input('something went wrong . IDK         :/')
                                    cls()
                            elif item_input == '2':
                                print()
                        elif pot_n < 0:
                            if item_input == '1':
                                print()
                            else:
                                cls()
                                noreply = input('something went wrong . IDK         :/')
                                cls()
                    elif si =='3':
                        run()
                        Camel = False
                        cls()
                        di = maps.desertmap(money,p_hp)
                    else:
                        cls()
                        noreply = input('something went wrong . IDK         :/')
                        cls()
                cls()
        else:
            cls()
            noreply = input('something went wrong . IDK         :/')
            cls()
            di = maps.desertmap(money,p_hp)
