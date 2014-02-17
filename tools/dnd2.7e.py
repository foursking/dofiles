#qpy:console
#coding: utf-8
import random
import math
import time
from sys import exit

def welcome():
    global dex_a,dex_b,value_a,value_b,hp_a,hp_b,str_a,str_b,atk_a,atk_b,name_a,name_b,base_a,base_b,x,dex_a_h, dex_b_h, str_a_h, str_b_h, luck_a_h, luck_b_h, ultimate_skill_a, ultimate_skill_b,honor_point_a,honor_point_b,critical_strike_a,critical_strike_b,smart_dodge_a,smart_dodge_b,crazy_bash_a,crazy_bash_b,damage_reflection_a,damage_reflection_b,win_number_a,win_number_b,total_number
    print "Welcome to Mario's Arena, Let's fight!\n"
    name_a = raw_input('Please enter in the name for PlayerA:')
    name_b = raw_input('Please enter in the name for PlayerB:')
    x = random.randrange(0,20)
    try:
        value_a = input('Please enter in lucky number for PlayerA:')
        value_b = input('Please enter in lucky number for PlayerB:')
        str_a = abs( (value_a - x+2342352528545) % 7)+ random.randrange(0,16) + 1
        str_b = abs( (value_b - x+8683587681239) % 7)+ random.randrange(0,16) + 1
        dex_a = (x + 242343565423448 + value_a)%7 + 100*(1.0/str_a)
        dex_b = (x + 325893945824574 + value_b)%7 + 100*(1.0/str_b)
    except NameError:
        print "Please type pure number for your lucky number"
        return welcome()
    except SyntaxError:
        print "Please type pure number for your lucky number"
        return welcome()
    except TypeError:
        print "Please type pure number for your lucky number"
        return welcome()
    else:
        pass
    base_a = dex_a
    base_b = dex_b
    hp_a = str_a * 10 * 8
    hp_b = str_b * 10 * 8
    atk_a = ((dex_a*2 + str_a)/2+1) * 10
    atk_b = ((dex_b*2 + str_b)/2+1) * 10
    honor_point_a = 0
    honor_point_b = 0
    dex_a_h = 0
    dex_b_h = 0
    str_a_h = 0
    str_b_h = 0
    luck_a_h = 0
    luck_b_h = 0
    critical_strike_a=None
    critical_strike_b=None
    smart_dodge_a=None
    smart_dodge_b=None
    crazy_bash_a=None
    crazy_bash_b=None
    damage_reflection_a=None
    damage_reflection_b=None
    ultimate_skill_a=None
    ultimate_skill_b=None
    win_number_a=0
    win_number_b=0
    total_number=0
    print"%s has %d hp and %d basic damage, %s has %d hp and %d basic damage. The attack speed,float damage and special skills are hidden\n" % (name_a,hp_a,atk_a,name_b,hp_b,atk_b)
    time.sleep(3)


class Revenge_Cauculator(object):
    def hp_compute(self):
        global dex_a,dex_b,hp_a,hp_b,str_a,str_b,atk_a,atk_b,name_a,name_b,dice,honor_point_a,honor_point_b,luck_a_h,luck_b_h,dex_a_h,dex_b_h,str_a_h,str_b_h,critical_strike_a,critical_strike_b,smart_dodge_a,smart_dodge_b,crazy_bash_a,crazy_bash_b,damage_reflection_a,damage_reflection_b,win_number_a,win_number_b,total_number
        if (hp_a <= 0 or hp_b <= 0) and (ultimate_skill_a == True or ultimate_skill_b == True):
            return finish()
        if hp_a <= 0 and hp_b <=0:
	    print "%s and %s die together！" % (name_a,name_b)
            total_number += 1
	    return refresh()
        if hp_a <= 0:
	    honor_point_b = honor_point_b + 1
	    honor_point_a =0
            total_number += 1
            win_number_b += 1
	    print "%s was killed, %s wins! %s got %d points now" % (name_a,name_b,name_b,honor_point_b)
	    return refresh_a()
        if hp_b <= 0:
	    honor_point_a = honor_point_a + 1
	    honor_point_b = 0
            total_number +=1
            win_number_a +=1
	    print "%s was killed, %s wins! %s got %d points now" % (name_b,name_a,name_a,honor_point_a)
	    return refresh_b()
    def skill_compute(self):
        global dex_a,dex_b,hp_a,hp_b,str_a,str_b,atk_a,atk_b,name_a,name_b,dice,honor_point_a,honor_point_b,luck_a_h,luck_b_h,dex_a_h,dex_b_h,str_a_h,str_b_h,critical_strike_a,critical_strike_b,smart_dodge_a,smart_dodge_b,crazy_bash_a,crazy_bash_b,damage_reflection_a,damage_reflection_b
        if hp_a < hp_b and random.randrange(0,150)- base_a - luck_a_h < 0 and dex_a > dex_b and critical_strike_a == True :
            hp_b = hp_b - real_atk_a * 2
            print "!!!Critical Strike!!! %s deals %d damage to %s, %s has %d hp left.\n" %(name_a, real_atk_a*2,name_b, name_b, hp_b)
            time.sleep(3)
        self.hp_compute
        if hp_b < hp_a and random.randrange(0,150)- base_b - luck_b_h < 0 and dex_b > dex_a and critical_strike_b == True :
            hp_a = hp_a - real_atk_b * 2
            print "!!!Critical Strike!!! %s deals %d damage to %s, %s has %d hp left. \n" %(name_b, real_atk_b*2, name_a, name_a, hp_a)
            time.sleep(3)
        self.hp_compute
        if random.randrange(0,150)- base_a - luck_a_h < 0 and dex_b > dex_a and smart_dodge_a == True :
            dex_a = base_a +dex_a
            print "~~~Miss~~~%s try to attack %s, but was dodged by %s. \n" %(name_b,  name_a, name_a)
            time.sleep(3)
        if random.randrange(0,150)- base_b - luck_b_h < 0 and dex_a > dex_b and smart_dodge_b == True:
            dex_b = base_b +dex_b
            print  "~~~Miss~~~%s try to attack %s, but was dodged by %s.  \n" %(name_a,  name_b, name_b)
            time.sleep(3)
        if random.randrange(0,45)- str_b - luck_b_h < 0 and  dex_a > dex_b and damage_reflection_b == True:
            hp_b=hp_b - real_atk_a
            hp_a=hp_a - 20 - str_b*3
            rl_dam=20+str_b*3
            dex_a=base_a + dex_a
            print"!!!Damage Reflection!!!%s deals %d damage to %s, %s reflects %d damage back. %s\'s hp:%d, %s\'s hp:%d\n" %(name_a,real_atk_a,name_b,name_b,rl_dam,name_a,hp_a,name_b,hp_b)
            time.sleep(3)
        if random.randrange(0,45)- str_a - luck_a_h < 0  and dex_b > dex_a and damage_reflection_a == True:
            hp_a=hp_a - real_atk_b
            hp_b=hp_b - 20 - str_a*3
            rl_dam=20 + str_a*3
            dex_b=base_b + dex_b
            print"!!!Damage Reflection!!!%s deals %d damage to %s, %s reflects %d damage back. %s\'s hp:%d, %s\'s hp:%d\n" %(name_b,real_atk_b,name_a,name_a,rl_dam,name_b,hp_b,name_a,hp_a)
            time.sleep(3)
        self.hp_compute()
        if hp_b > hp_a and random.randrange(0,45)- str_b - luck_b_h < 0 and str_b > str_a and crazy_bash_b == True :
            hp_a = hp_a - real_atk_b - 2*str_b
            dex_b = base_b + dex_b*2
            dex_a = base_a + dex_a
            print"!!!Bash!!!%s attacks %s, deals %d damage and stun him. %s now has %d hp left. \n" %(name_b,  name_a,real_atk_b+2*str_b, name_a, hp_a)
            time.sleep(3)
        if hp_a > hp_b and random.randrange(0,45)- str_a - luck_a_h < 0 and str_a > str_b and crazy_bash_a == True :
            hp_b = hp_b - real_atk_a - 2*str_a
            dex_a = base_a + dex_a*2
            dex_b = base_b + dex_b
            print "!!!Bash!!!%s attacks %s, deals %d damage and stun him. %s now has %d hp left.  \n" %(name_a,  name_b,real_atk_a+2*str_a, name_b, hp_b)
            time.sleep(3)
        self.hp_compute()


def refresh():
    global dex_a,dex_b,value_a,value_b,hp_a,hp_b,str_a,str_b,atk_a,atk_b,name_a,name_b,base_a,base_b,x,dex_a_h, dex_b_h, str_a_h, str_b_h, luck_a_h, luck_b_h, ultimate_skill_a, ultimate_skill_b
    try:
        command = raw_input('type in anything to continue, type in exit to exit the game:')
        if command == 'exit':
            exit(0)
        else:
            pass
    except SyntaxError:
        pass
    except NameError:
        pass
    name_a = raw_input('Please enter in the name for PlayerA:')
    name_b = raw_input('Please enter in the name for PlayerB:')
    x = random.randrange(0,20)
    try:
        value_a = input('Please enter in lucky number for PlayerA:')
        value_b = input('Please enter in lucky number for PlayerB:')
        str_a = abs( (value_a - x+2342352528545) % 7)+ random.randrange(0,16) + 1
        str_b = abs( (value_b - x+8683587681239) % 7)+ random.randrange(0,16) + 1
        dex_a = (x + 242343565423448 + value_a)%7 + 100*(1.0/str_a)
        dex_b = (x + 325893945824574 + value_b)%7 + 100*(1.0/str_b)
    except NameError:
        print "Please type pure number for your lucky number"
        return refresh()
    except SyntaxError:
        print "Please type pure number for your lucky number"
        return refresh()
    except TypeError:
        print "Please type pure number for your lucky number"
        return refresh()
    else:
        pass
    base_a = dex_a
    base_b = dex_b
    hp_a = str_a * 10 * 8
    hp_b = str_b * 10 * 8
    atk_a = ((dex_a*2 + str_a)/2+1) * 10
    atk_b = ((dex_b*2 + str_b)/2+1) * 10
    return shop()
    time.sleep(2)

def refresh_a():
    global dex_a,value_a,hp_a,str_a,atk_a,name_a,base_a,x,dex_a_h,str_a_h,luck_a_h,ultimate_skill_a,honor_point_a,name_b,hp_b,atk_b,dex_b,base_b,str_b
    try:
        command = raw_input('type in anything to continue, type in exit to exit to exit the game:')
        if command == 'exit':
            exit(0)
        else:
            pass
    except SyntaxError:
        pass
    except NameError:
        pass
    name_a=raw_input('Please enter in the name for PlayerA:')
    x=random.randrange(0,20)
    try:
        value_a = input('Please enter in lucky number for PlayerA:')
        str_a = abs( (value_a - x+2342352528545) % 7)+ random.randrange(0,16) + 1
        dex_a = (x + 242343565423448 + value_a)%7 + 100*(1.0/str_a)
    except NameError:
        print "Please type pure number for your lucky number"
        return refresh_a()
    except SyntaxError:
        print "Please type pure number for your lucky number"
        return refresh_a()
    except TypeError:
        print "Please type pure number for your lucky number"
        return refresh_a()
    else:
        pass
    base_a=dex_a
    dex_b=base_b
    hp_a=str_a * 10 * 8
    hp_b=str_b * 10 * 8 + str_b_h*80
    atk_a = ((dex_a*2 + str_a)/2+1) * 10
    honor_point_a=0
    str_a_h=0
    dex_a_h=0
    luck_a_h=0
    return shop()
    time.sleep(2)

def refresh_b():
    global dex_b,value_b,hp_b,str_b,atk_b,name_b,base_b,x,dex_b_h, str_b_h, luck_b_h, ultimate_skill_b,honor_point_b,name_a,hp_a,atk_a,dex_a,base_a,str_a,str_a_h
    try:
        command = raw_input('type in anything to continue, type in exit to exit the game:')
        if command == 'exit':
            exit(0)
        else:
            pass
    except SyntaxError:
        pass
    except NameError:
        pass
    name_b=raw_input('Please enter in the name for PlayerB:')
    x=random.randrange(0,20)
    try:
        value_b = input('Please enter in lucky number for PlayerB:')
        str_b = abs( (value_b - x+8683587681239) % 7)+ random.randrange(0,16) + 1
        dex_b = (x + 325893945824574 + value_b)%7 + 100*(1.0/str_b)
    except NameError:
        print "Please type pure number for your lucky number"
        return refresh_b()
    except SyntaxError:
        print "Please type pure number for your lucky number"
        return refresh_b()
    except TypeError:
        print "Please type pure number for your lucky number"
        return refresh_b()
    else:
        pass
    dex_a = base_a
    base_b=dex_b
    base_a=dex_a
    hp_b=str_b * 10 * 8
    hp_a=str_a * 10 * 8 + str_a_h*80
    atk_b = ((dex_b*2 + str_b)/2+1) * 10
    honor_point_b=0
    str_b_h=0
    dex_b_h=0
    luck_b_h=0
    return shop()
    time.sleep(2)

def shop():
    global name_a,name_b,honor_point_a, honor_point_b, dex_a_h, dex_b_h, str_a_h, str_b_h, luck_a_h, luck_b_h, ultimate_skill_a,hp_a,str_a, ultimate_skill_b,hp_b,str_b,critical_strike_a,critical_strike_b,smart_dodge_a,smart_dodge_b,crazy_bash_a,crazy_bash_b,damage_reflection_a,damage_reflection_b,win_number_a,win_number_b,total_number
    print "\n------------Introduction of monster system----------\n"
    print "\nYou have played %d games now,%s won %d games, %s won %d games" % (total_number,name_a,win_number_a,name_b,win_number_b)
    print "\n\nThe one who has won more than 20 games can go to the misterious cave to fight the monsters."
    print "\nAfter you kill the monsters, you may get valuable treasures so you can chanllenge more powerful monsters or smash your opponent."
    print "\nBut if the monster kills you, you die, not a joke!"
    print "\nBy the way, the monster system is still in developing, please be patient."
    print "\nOr you can donate to my ZhiFuBao account 'bb2qqq@gmail.com' to stimulate me, lol"
    print "\n------------Introduction of shop system-----------\n"
    print "\nWhen you won a battle, you'll get 1 point"
    print "Points can be used to buy things in the shop."
    print "When you die, all your points will lost."
    print "\n\n %s\'s point:\"\"%d\"\", %s\'s point:\"\"%d\"\".\n" % (name_a,honor_point_a,name_b,honor_point_b)
    print "\nEach time you can only buy 1 thing."
    print "\nShopList:"
    print "\n\'Strength+1\' costs: 1point, effect: hp+,damdage+ shopcode:\"\"S\"\""
    print "\n\'Dexterity+1\' costs: 1 point, effect: attack speed+,damage+. shopcode:\"\"D\"\""
    print "\n\'Luck+1\' costs: 1 point, effect: skill chance+,damadge+. shopcode:\"\"L\"\""
    print "\n\'Critical Strike\' cost: 3 point. effect: have chance to deal double damage when your hp is lower than your rival. shopcode:\"\"CS\"\""
    print "\n\'Smart Dodge\' cost: 3 point. effect:have chance to dodge enemy's attack. shopcode:\"\"SD\"\""
    print "\n\'Crazy Bash\' cost: 3 point. effect: have chance to stun your enemy. shopcode:\"\"CB\"\""
    print "\n\'Dmage Reflection\' cost: 3 point. effect: have chance to reflect damage when your rival attacks you. shopcode:\"\"DR\"\""
    print "\n\'Ultimate Skill\' cost: 10 point. effect: get ultimate skill. shopcode:\"\"US\"\""
    print "\nType A/B + shopcode to buy items. If PlayerA wants to buy Strength+1, type AS, then press Enter, If PLayerB wants to buy Luck+1, type BL, then press Enter, etc."
    shop_behaviour=raw_input('\nType in command and press Enter to buy items, Type in leave and press Enter to leave the shop:')
    if shop_behaviour == 'AS' and  honor_point_a > 0:
        honor_point_a -= 1
        str_a_h += 1
        print " %s has increased his strength successfully !" % name_a
        return prepare()
    elif shop_behaviour == 'AD' and  honor_point_a > 0:
        honor_point_a -= 1
        dex_a_h += 1
        print " %s has increased his dexterity successfully !" % name_a
        return prepare()
    elif shop_behaviour == 'AL' and  honor_point_a > 0:
        honor_point_a -= 1
        luck_a_h += 1
        print " %s has increased his luck successfully !" % name_a
        return prepare()
    elif shop_behaviour == 'ACS' and  honor_point_a >= 3:
        honor_point_a -= 3
        critical_strike_a=True
        print " %s has get Critical Strike ability!" % name_a
        return prepare()
    elif shop_behaviour == 'ASD' and  honor_point_a >= 3:
        honor_point_a -= 3
        smart_dodge_a=True
        print " %s has get Smart Dodge ability!" % name_a
        return prepare()
    elif shop_behaviour == 'ACB' and  honor_point_a >= 3:
        honor_point_a -= 3
        crazy_bash_a=True
        print " %s has get Crazy Bash ability!" % name_a
        return prepare()
    elif shop_behaviour == 'ADR' and  honor_point_a >= 3:
        honor_point_a -= 3
        damage_reflection_a=True
        print " %s has get Damage Reflection ability!" % name_a
        return prepare()
    elif shop_behaviour == 'AUS' and  honor_point_a >= 10:
        honor_point_a -= 10
        ultimate_skill_a=True
        print " %s has get his ultimate skill!"	% name_a
        return ultimate()
    elif shop_behaviour == 'BS' and  honor_point_b > 0:
        honor_point_b -= 1
        str_b_h += 1
        print " %s has increased his strength successfully !" % name_b
        return prepare()
    elif shop_behaviour == 'BD' and  honor_point_b > 0:
        honor_point_b -= 1
        dex_b_h += 1
        print " %s has increased his dexterity successfully !" % name_b
        return prepare()
    elif shop_behaviour == 'BL' and  honor_point_b > 0:
        honor_point_b -= 1
        luck_b_h += 1
        print " %s has increased his luck successfully !" % name_b
        return prepare()
    elif shop_behaviour == 'BUS' and  honor_point_b >= 10:
        honor_point_b -= 10
        ultimate_skill_b=True
        print " %s has get his ultimate skill!" % name_b
        return ultimate()
    elif shop_behaviour == 'BCS' and  honor_point_b >= 3:
        honor_point_b -= 3
        critical_strike_b=True
        print " %s has get Critical Strike ability!" % name_b
        return prepare()
    elif shop_behaviour == 'BSD' and  honor_point_b >= 3:
        honor_point_b -= 3
        smart_dodge_b=True
        print " %s has get Smart Dodge ability!" % name_b
        return prepare()
    elif shop_behaviour == 'BCB' and  honor_point_b >= 3:
        honor_point_b -= 3
        crazy_bash_b=True
        print " %s has get Crazy Bash ability!" % name_b
        return prepare()
    elif shop_behaviour == 'BDR' and  honor_point_b >= 3:
        honor_point_b -= 3
        damage_reflection_b=True
        print " %s has get Damage Reflection ability!" % name_b
        return prepare()
    elif shop_behaviour == 'leave':
        print "You walk out of the shop to embrace the next fight!"
        return prepare()
    else:
        return shop()


def ultimate():
    global hp_a,str_a,dex_a,atk_a,str_a_h,dex_a_h,luck_a_h,hp_b,str_b,dex_b,atk_b,str_b_h,dex_b_h,luck_b_h
    print " What???!!! You got 10 points now???!!! Your opponent must be screwed like a shit. It boring, isn't it? Cheer up, we've cloned you now. Please	enjoy your last fight with your oppent."
    if ultimate_skill_a == True:
        hp_b=hp_a
        str_b=str_a
        dex_b=dex_a
        atk_b=atk_a
        str_b_h=str_a_h
        dex_b_h=dex_a_h
        luck_b_h=luck_a_h
        time.sleep(10)
        return start()
    elif ultimate_skill_b == True:
        hp_a=hp_b
        str_a=str_b
        dex_a=dex_b
        atk_a=atk_b
        str_a_h=str_b_h
        dex_a_h=dex_b_h
        luck_a_h=luck_b_h
        time.sleep(10)
        return start()


def prepare():
    global name_a,name_b,hp_a,hp_b,atk_a,atk_b,dex_a,str_a,dex_b,str_b,dex_a_h,dex_b_h,str_a_h,str_b_h
    hp_a=str_a * 10 * 12 + str_a_h*120
    hp_b=str_b * 10 * 12 + str_b_h*120
    atk_a = (((dex_a+dex_a_h)*2 + str_a+str_a_h)/2+1) * 10
    atk_b = (((dex_b+dex_b_h)*2 + str_b+str_b_h)/2+1) * 10
    print"%s has %d hp and %d basic damage, %s has %d hp and %d basic damage. The attack speed, float damage and special skills are hidden\n" % (name_a,hp_a,atk_a,name_b,hp_b,atk_b)
    return start()


def start():
    global dex_a,dex_b,hp_a,hp_b,str_a,str_b,atk_a,atk_b,name_a,name_b,dice,honor_point_a,honor_point_b,luck_a_h,luck_b_h,dex_a_h,dex_b_h,str_a_h,str_b_h
    real_atk_a = atk_a + random.randrange(-10,10) + random.randrange(-1,luck_a_h*10)
    real_atk_b = atk_b + random.randrange(-10,10) + random.randrange(-1,luck_b_h*10)
    if dex_a > dex_b:
        hp_b = hp_b - real_atk_a
        dex_b = base_b + dex_b
        print "%s attacks %s, deals %d damage, %s has %d hp left. \n" % (name_a,name_b,real_atk_a,name_b,hp_b)
        time.sleep(2.5)
    elif dex_b > dex_a:
        hp_a = hp_a - real_atk_b
        dex_a = base_a + dex_a
        print "%s attacks %s, deals %d damage, %s has %d hp left. \n" % (name_b,name_a,real_atk_b,name_a,hp_a)
        time.sleep(2.5)
    elif dex_a == dex_b:
        hp_b = hp_b - real_atk_a
        hp_a = hp_a - real_atk_b
        dex_a = base_a + dex_a
        dex_b = base_b + dex_b
        print" %s and %s attacks each other at the same time, %s deals %d damage to %s, %s deals %d damage to %s, %s has %d hp left，%s has %d hp left。\n" % (name_a,name_b,name_a,real_atk_a,name_b,name_b,real_atk_b,name_a,name_a,hp_a,name_b,hp_b)
        time.sleep(2.5)
    i1.hp_compute()
    i1.skill_compute()
    if str_a_h > 99 or dex_a_h > 99 or luck_a_h or str_b_h > 99 or dex_b_h > 99 or luck_b_h > 99 or honor_point_a > 99 or honor_point_b > 99:
        return envy()


def finish():
    if hp_a <= 0 and hp_b <= 0:
        print "---------Both players die. Game Creater is the final winner, CONGRATULATIONS!!!!!---------"
    elif hp_a <= 0:
        print "---------%s is the final winner, CONGRATULATIONS!!!!!!---------" % (name_b)
    elif hp_b <= 0:
	    print "---------%s is the final winner, CONGRATULATIONS!!!!!!---------" % (name_a)

def envy():
    print "---------You are too strong now, the Game Creator envys you, a thunder splashed on you, you are dead now------------"
    print "Game Over"


i1=Revenge_Cauculator()
welcome()
while True:
    start()
