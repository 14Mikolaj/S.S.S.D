def camel(p_hp,p_max_hp,p_str,p_spd,p_crit_c,p_dmg_min,p_dmg_max,e_hp,e_max_hp,e_spd,e_dmg_min,e_dmg_max):
    print('''
The camel looks in the eye. you welcome it with a bow.
Bewildered, you rush to prepare for battle with this beast.
However, it seems it does not want to fight with you... leave in peace?

          __             --.__       Crazy camel, lvl 5
        .'  '.        ..' '   .
      .'      '._____/    .---'      [1] hit (''',p_dmg_min,'''-''',p_dmg_max,''')
   .-/                   |           [2] check pots
 .'                    ./            [3] run for your life before the great one
 |   |\\        .  .---'
 |   |.'------| .'                   Crazy camel hp: ''',e_hp,'''
 #\\  |        | |.                   your hp: ''',p_hp,'''
## \\ .        | |.
   ||'       .| |.
  . |.        | |.
  \\ \\ #       | |.
   \\_\\ #      |__..

''')
    return input()

def camelhit(edamage):
    print('''

          __             --.__       Crazy camel furiously wrecks you with its iron hooves, engulfed with it's rage, it considers also inhumanely eat you alive.
        .'  '.        ..' '   .
      .'      '._____/    .---'      You wonder what hit you... you do not realise the blood heaping from your lower abdominal area from where the camel has layed its jaws on.
   .-/                   |           You feel as though your soul is fading... you realise you are closer to dying as your life points drop by ''',edamage,''' points.
 .'                    ./            The camel is still in the distance, awaiting your next move. You now know that you need to be a lot more careful when dealing with this one.
 |   |\\        .  .---'              But the pain... it doesn't want to go away.. what are you experiencing? you may ask...
 |   |.'------| .'                   Well this camel is no ordinairy camel, for this is a god in disguise full of fury and anger, within the body of the camel.
 #\\  |        | |.                   This camel is, well what it seems to me is, 'crazy'.
## \\ .        | |.                   The Bleeding can't seem to get off your mind, it only appears to be worsening. You don't know how to go about this
   ||'       .| |.                   and therefore the itensive bleed forces your life points to drop by another ''',edamage/2,''' . You feel as though your soul
  . |.        | |.                   is being torn apart, slowly, and painfully. You suffer and you want it to stop, but you can sense the pain overcome your senses.
  \\ \\ #       | |.                   
   \\_\\ #      |__..                  Dear camel save me once and i'll come back stronger. I promise...

                                     Your promise is made and your wish is granted.
''')
    return input()

def attack_camel(damage):
    print('''
          __             --.__       Something is not right... you know you have launched your attack. And that it has landed on your opponent.
        .'  '.        ..' '   .      But this is strange - you are standing right where you were before, and the camel, lifelessly glaring into the 
      .'      '._____/    .---'      empty scenery far ad beyond. Without emothion, looking to be as though it is frozen in time.
   .-/                   |           "Time" You think to yourself, and an idea comes to your head that maybe something has reversed time, and you are actually standing here
 .'                    ./            because you havn't declared an attack yet . But something STILL seems off... 
 |   |\\        .  .---'              A thought comes to your mind. You don't know why, but you don't seem to question it. 
 |   |.'------| .'                   "yauhhaaatthhee  diieessruuuttt peeeessss" Where did this come from?
 #\\  |        | |.                   It's a strange voice speaking to you in your head: It's the camel using its wise intellect to telepathically
## \\ .        | |.                   communicate with you. Your heart begins racing as the camel slowly begins to make a move towards you.
   ||'       .| |.                   "impossible!" you say, knowing that no one else will hear you yell to a camel. You are absolutely certain that you hit the camel.
  . |.        | |.                   You stop believing in this fantasty, and through your eyes, the world around you begins to go dark. You experience an unusual tingling 
  \\ \\ #       | |.                   sensation chasing around your body, and you witness the time around you reverse.
   \\_\\ #      |__..                  You have entered the parallel universe in which you most certainly HAVE attacked the camel. This is easily proven by that scratch on 
                                     the camel. Dissapointment. Eternal wrath. What does this mean? I don't know either, i'm only the narrator, but it may be linked.

                                     The Crazy camel looses ''',damage,''' life points.               
''')
    return input()

def camel_dead(xp_drop,g_drop,TaskCam,ob,Camel_Souls):
    print('''
          __             --.__       The air around you is relieved of tension and you feel relief. 
        .'  '.        ..' X   .      You know exactly that peace has been disrupted, but for now the area seems peacful enough for another battle. 
      .'      '._____/    .---'      You watch carefully as the camel lifelessly topples to its side as though you have done nothing to it.
   .-/                   |           Your mind fills up with guilt, plenty of guilt. The guilt is insisting for you to believe that you have
 .'                    ./            committed a creat crime ... - murder. camel murder. crazy camel god murder...
 |   |\\        .  .---'              You stare at the soulless body of a camel lying on the sand in front of you, as a faint spirit leaves the camel's body.
 |   |.'------| .'                   And then you hear it : a quick clink in your pocket. You enter the pocket with your hand, and to your suprise, 
 #\\  |        | |.                   your pockets are full of gold! You know something doesn't feel right, being rewarded from no where for the murder of the great
## \\ .        | |.                   camel. But that doesn't stop you from going further... you feel stronger as your mind is imbued with extra experience points.
   ||'       .| |.                   You will remember this for all time and for the future you will know more about crazy god camels.
  . |.        | |.                   You turn back to the camel, but strangely, the flesh and blood is missing and all residue left behind is pure camel bone.
  \\ \\ #       | |.                   You glance back at your hands, to your sanity, they are coverd and dripping in blood!
   \\_\\ #      |__..                  
                                     You find ''',g_drop,''' extra gold in your pocket.
                                     And Gain an extra ''',xp_drop,''' experience points for defeating the first titan.''')
    if TaskCam == True and ob < Camel_Souls:
        print('''
                                     A white whisp leaves the camel's corpse, you stare in amazemement as you realize that this is your goal, the reason
                                     you are here and sloughtered this beast. The Soul of the Camel God. You rush with an ancient clay Amphoric Vial in your
                                     hands towards the great beast and capture the soul. A soul of a God.         You now have ''',ob+1,''' of the two souls needed for the ritual.''')
    else:
        print()
    print('''



                                                             
''')
    return input()

def attack_camel_crit(damage):
    print('''
          __             --.__       Your blood-boiled mind becomes enraged with fury. your weapon is demanding blood for sacrifice.
        .'  '.        ..'.O   .      A great Slash of your weapon cuts cleanly through the opponent. A flesh wound for them and
      .'      '._____/    .---'      bloody havoc is done. You are amazed at how severely wounded the camel looks, it almost makes you feel sorrow.
   .-/                   |           But the camel says otherwise, still not moving. staring into the scenery, almost as if it let you do this
 .'                    ./            to itself. Crazy yes, but metally challenging for you as your sanity drops below 0, mad man.
 |   |\\        .  .---'              
 |   |.'------| .'                  
 #\\  |        | |.                   
## \\ .        | |.                   
   ||'       .| |.                   Your Critical strike sliced the camel for ''',damage,''' life points.
  . |.        | |.                   Clean Cut!
  \\ \\ #       | |.                   
   \\_\\ #      |__..                  Your sanity drops below 0?!

                  
''')
    return input()
