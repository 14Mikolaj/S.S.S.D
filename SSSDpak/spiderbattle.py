def spider(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max):
    print('''
You found a spooder. You are not a big fan of spooders.


     ____
    (0  0)              Spooder, lvl 3
//// -vv- \\\\\\\\     
                        [1] hit (''',p_dmg_min,'''-''',p_dmg_max,''')
                        [2] check pots
                        [3] run for your life before the great one

                        Spooder hp: ''',e_hp,'''
                        your hp: ''',p_hp,''' 
''')
    return input()

def spiderhit(edamage):
    print('''



     ____
    (0  0)              Spooder crawls over you
//// -vv- \\\\\\\\      
                        You somehow took ''',edamage,''' damage???
                        
                      

                        
                       
''')
    return input()

def attack_spider(damage):
    print('''


 
     ____ oh...
    (0  0)             You attack the spooder for ''',damage,''' damage.
//// -vv- \\\\\\\\     
                    
                        
                      

                        
                       
''')
    return input()

def spider_dead(xp_drop,g_drop,TaskSpid,ob,Spooder_Kills):
    print('''


  
     ____               The spooder imploded. Not a nice sight
    (x  x)             
//// -vv- \\\\\\\\        
                        You earnt ''',xp_drop,''' xp
                        And earnt $ ''',g_drop)
    if TaskSpid == True and ob < Spooder_Kills:
        print('''                        Spooder Death Documented. (''',ob+1,'''/6)''')
    print('''
                        
                       
''')
    return input()

def attack_spid_crit(damage):
    print('''



     ____
    (0  0)             you CRIT! dealing ''',damage,''' damage to the spooder.
//// -vv- \\\\\\\\     
                        
                        
                      

                        
                       
''')
    return input()
