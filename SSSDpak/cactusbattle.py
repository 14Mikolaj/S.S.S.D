
def cactus(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max):
    print('''
Here lies a cactus... its quite spiky

             ^^            spiky cactus, lvl 1
            <  >
    ^^      <  >      ^^
   <  >     <  >     <  >  [1] hit (''',p_dmg_min,'''-''',p_dmg_max,''')
   <  >     <  >     <  >  [2] check pots
   <  ^^^^^^    ^^^^^^  >  [3] run for your life before the great one
    ^^^^^^^^^  ^^^^^^^^^
            <  >
            <  >           cactus hp: ''',e_hp,'''
            <  >           your hp: ''',p_hp,'''
            <  >
            <  >
            <  >
            <  >
            <  >
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
''')
    return input()

def attack_cact (damage):

    print('''


             ^^            
            <  >
    ^^      <  >      ^^     you dealt ''',damage,''' damage to the cactus
   <  >     <  >     <  >  
   <  >     <  >     <  >  
   <  ^^^^^^    ^^^^^^  >  
    ^^^^^^^^^  ^^^^^^^^^
            <  >
            <  >           
            <  >           
            <  >
            <  >
            <  >
            <  >
            <  >
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
''')
    noreply = input()

def attack_cact_crit(damage):

    print('''


             ^^            
            <  >
    ^^      <  >      ^^     you CRIT! dealing ''',damage,''' damage to the cactus
   <  >     <  >     <  >  
   <  >     <  >     <  >  
   <  ^^^^^^    ^^^^^^  >  
    ^^^^^^^^^  ^^^^^^^^^
            <  >
            <  >           
            <  >           
            <  >
            <  >
            <  >
            <  >
            <  >
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
''')
    noreply = input()

def cactushit(edamage):

    print('''


             ^^            
            <  >
    ^^      <  >      ^^    you hurt yourself for ''',edamage,''' damage.
   <  >     <  >     <  >  
   <  >     <  >     <  >  
   <  ^^^^^^    ^^^^^^  >  
    ^^^^^^^^^  ^^^^^^^^^
            <  >
            <  >           
            <  >           
            <  >
            <  >
            <  >
            <  >
            <  >
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
''')
    noreply = input()
    
def cactus_dead(xp_drop,g_drop,ob,Cacti,TaskCact):

    print('''


             ^^            
            <  >
    ^^      <  >      ^^     You Relentlesly murdered the cactus.
   <  >     <  >     <  >   
   <  >     <  >     <  >  
   <  ^^^^^^    ^^^^^^  >    You earnt ''',xp_drop,''' xp
    ^^^^^^^^^  ^^^^^^^^^     And earnt $ ''',g_drop)
    if TaskCact == True and ob < Cacti:
          print('''            <  >             You Also Collected 1 Cactus!  (''',ob+1,'''/10)''')
    else:
        print('''            <  >     ''')
    print('''            <  >           
            <  >           
            <  >
            <  >
            <  >
            <  >
            <  >
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
''')
    noreply = input()
