def snake(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max):
    print('''
Behold the great snek.
AM MUCH VENOM
                 __
        hiss    /..\\          Snek, lvl 4
                \\" /
      ____      / |'          [1] hit (''',p_dmg_min,'''-''',p_dmg_max,''')
 _,--'____'----' ,'           [2] check pots
<_.--'    '-----'             [3] run for your life before the great one

                              Snek hp: ''',e_hp,'''
                              your hp: ''',p_hp,''' 




''')
    return input()

def snakehit(edamage):
    print('''

                 __
        hiss    /..\\         Snek uses weak venom stab.
                \\" /         It's super effective!
      ____      / |'
 _,--'____'----' ,'          You take ''',edamage,''' damage.
<_.--'    '-----'






''')
    return input()


def attack_snake(damage):
    print('''


                 __
        why?    /..\\         You attack Snek for ''',damage,''' damage.
                \\" /
      ____      / |'
 _,--'____'----' ,'
<_.--'    '-----'






''')
    return input()


def snake_dead(xp_drop,g_drop,TaskSnek,ob,Venom):
    print('''


                 __
                /xx\\          You Disssintegrated the Snek.
                \\" /
      ____      / |'          You earnt ''',xp_drop,''' xp
 _,--'____'----' ,'           And earnt $ ''',g_drop)
    if TaskSnek == True and ob < Venom:
        print('''<_.--'    '-----'             You also Collect 1 Snek Venom! (''',ob+1,'''/4)''')
    else:
        print('''<_.--'    '-----''')
    print('''





''')
    return input()

def attack_snake_crit(damage):
    print('''


                 __
        hiss    /..\\           you CRIT! dealing ''',damage,''' damage to the Snek.
                \\" /
      ____      / |'
 _,--'____'----' ,'
<_.--'    '-----'






''')
    return input()

