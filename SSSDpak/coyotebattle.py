def coyote(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max):
    print('''
You Found a coyote. seems friendly.
                 .     .
                 \ \__/ '     wild coyote, lvl 2
   ______________/ -  - /     
  /'             \_ @  /      [1] hit (''',p_dmg_min,'''-''',p_dmg_max,''')
  | \   \       | /---'       [2] check pots
  | /./\ |----- |/|           [3] run for your life before the great one
 /.//  | /      |||
//||  / /       |||           coyote hp: ''',e_hp,'''
' |_\ \_\       |_\\          your hp: ''',p_hp,''' 
''')
    return input()

def coyohit(edamage):
    print('''
You Found a coyote. seems friendly.
                 .     .
                 \ \__/ '     
   ______________/ -  - /     
  /'             \_ @  /      Coyote Growls at you.
  | \   \       | /---'       
  | /./\ |----- |/|           You take ''',edamage,''' damage.
 /.//  | /      |||
//||  / /       |||           
' |_\ \_\       |_\\          
''')
    return input()

def attack_coyo(damage):
    print('''
You Found a coyote. seems friendly.
                 .     .
                 \ \__/ '     
   ______________/ -  - /     
  /'             \_ @  /      You attack the coyote for ''',damage,''' damage.
  | \   \       | /---'       
  | /./\ |----- |/|           
 /.//  | /      |||
//||  / /       |||           
' |_\ \_\       |_\\          
''')
    return input()

def coyote_dead(xp_drop,g_drop,TaskCoyo,ob,Coyo_Fur):
    print('''
                 .     .
                 \ \__/ '     
   ______________/ X  X /     You Eviscerated the coyote from existance
  /'             \_ @  /      
  | \   \       | /---'       You earnt ''',xp_drop,''' xp
  | /./\ |----- |/|           And earnt $ ''',g_drop,)
    if TaskCoyo == True and ob < Coyo_fur:
        print(''' /.//  | /      |||           You also collect 1 Coyote Fur! (''',ob+1,'''/8)''')
    else:
        print(''' /.//  | /      |||        ''')
    print('''//||  / /       |||           
' |_\ \_\       |_\\          
''')
    return input()

def attack_coyote_crit(damage):
    print('''
                 .     .
                 \ \__/ '     
   ______________/ -  - /     you CRIT! dealing ''',damage,''' damage to the coyote
  /'             \_ @  /      
  | \   \       | /---'      
  | /./\ |----- |/|           
 /.//  | /      |||
//||  / /       |||           
' |_\ \_\       |_\\          
''')
    return input()
