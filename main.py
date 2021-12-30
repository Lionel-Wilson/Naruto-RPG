# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 17:51:00 2021

@author: Lione
"""
#importing modules to be used
import random
import pygame
import os
pygame.init() #initialise pygame#
pygame.font.init()

class Screen:
    def __init__(self, path, caption):
        # set the name of the screen
        pygame.display.set_caption(caption)
        self.pic = pygame.image.load(path)
        #get_rect returns the a rectangle surface the same size of the surface. in this case the image.
        #Rect(left, top, width, height). The 2nd index and the 3rd index of a rect are the width and height, so we are get those attributes with the get_rect function.And setting them as the screens width and height.
        self.screen_width = self.pic.get_rect()[2]
        self.screen_height = self.pic.get_rect()[3]

    def make_screen(self):
        return pygame.display.set_mode((self.screen_width, self.screen_height))

    def choose_Background(self):
        return self.pic



#Game setup
init_screen = Screen('Title Screen complete.png', 'Naruto RPG by East meets West')
# set the screen width and height
screen_width, screen_height = init_screen.screen_width, init_screen.screen_height # Screen width and height changes depending on the image on the screen
screen = init_screen.make_screen()
Background_picture = init_screen.choose_Background()
fg_color = pygame.Color("gray")
clock = pygame.time.Clock() #allows to change the frame rate. 
FPS = 60
running_game = True
text_font = pygame.font.SysFont("monospace",25)
battle_text_font = pygame.font.SysFont("monospace",15)
battle_update_text1 = "Waiting for Player 1 to attack"
battle_update_text2 = "Waiting for Player 2 to attack"



#class for Loading maps into memory
class maps: 
    def __init__(self,filename,starting_x_pos = 100 ,starting_y_pos = 310 ,exit_x_pos = None,exit_y_pos = None):
        self.filename = filename
        self.img = pygame.image.load(self.filename).convert()
        
        #where character will start when they enter the map
        self.starting_x_pos = starting_x_pos
        self.starting_y_pos = starting_y_pos
        
        #preseting the location the platformer has to cross to move to the next map.
        self.exit_x_pos = exit_x_pos
        self.exit_y_pos = exit_y_pos
        
    
            

#CREATING MAP OBJECTS
Title = maps('Title Screen complete.png',None,None,None,None)
battle_screen_stage = maps('stages/battle screen.png',None,None,None,None)
stage_1_tutorial = maps('stages/Stage 1 - Tutorial.png',100,300,800,300)
Stage_2_minigame = maps('stages/Stage 2 - 1st minigame.png',100,310,800,310)
stage_5_sasuke_platform_p1 = maps('stages/Stage 5 - Sasuke Base platformer 2 part 1.png',None,250,800,310)
stage_5_sasuke_platform_p2 = maps('stages/Stage 5 - Sasuke Base platformer 2 part 2.png',None,191,800,310)
stage_5_sasuke_platform_p3 = maps('stages/Stage 5 - Sasuke Base platformer 2 part 3.png',None,135,800,310)
stage_5_sasuke_platform_p4 = maps('stages/Stage 5 - Sasuke Base platformer 2 part 4.png',None,20,800,310)
Stage_6_final = maps('stages/Stage 6 - Sasuke vs naruto final.png',None,224,800,310)




'''PLAYER CLASSES SECTION'''

#objects of this class will be drawn when not in battle.Aka platformer.
class Player_Platform_Mode:
    def __init__(self, name = 'Naruto',hp = 3,max_hp = 3,x_pos=100,y_pos = 310,width = 47,height = 63,speed=10,runcount = 0,left = False ,right =False ,jumping =False,jumpcount= 10): 
       #CHARACTER PLATFORM STATS 
       self.name,self.hp,self.max_hp = name,hp,max_hp #If we included projectiles when naruto is hit 3 times he dies in the platform mode and you start the game again
       self.alive = True   
       
       #CHARACTER MOVEMENT - width and height. NOTE - the coordinate of the any objects created on the screen is in the top left of it.
       self.x_pos = x_pos 
       self.y_pos = y_pos
       self.width = width
       self.height = height
       self.speed = speed
       self.runcount = runcount
       self.left = left
       self.right = right
       self.jumping = jumping
       self.jumpcount = jumpcount
       
       #CHARACTER MOVEMENT ANIMATIONS
       self.jumping_right_animation = [pygame.image.load('characters/Naruto/naruto jump 1.png'),pygame.image.load('characters/Naruto/naruto jump 2.png'),pygame.image.load('characters/Naruto/naruto jump 3.png'),
                                       pygame.image.load('characters/Naruto/naruto jump 4.png'),pygame.image.load('characters/Naruto/naruto jump 5.png')]
       self.jumping_left_animation = [pygame.transform.flip(self.jumping_right_animation[0], True, False),pygame.transform.flip(self.jumping_right_animation[1], True, False),pygame.transform.flip(self.jumping_right_animation[2], True, False),
                                       pygame.transform.flip(self.jumping_right_animation[3], True, False),pygame.transform.flip(self.jumping_right_animation[4], True, False)]
       self.right_running_animation = [pygame.image.load('characters/Naruto/naruto run right 1.png'),pygame.image.load('characters/Naruto/naruto run right 2.png'),pygame.image.load('characters/Naruto/naruto run right 3.png'),
                                        pygame.image.load('characters/Naruto/naruto run right 4.png'),pygame.image.load('characters/Naruto/naruto run right 5.png'),pygame.image.load('characters/Naruto/naruto run right 6.png'),]
       self.left_running_animation = [pygame.transform.flip(self.right_running_animation[0], True, False),pygame.transform.flip(self.right_running_animation[1], True, False),pygame.transform.flip(self.right_running_animation[2], True, False),
                                       pygame.transform.flip(self.right_running_animation[3], True, False),pygame.transform.flip(self.right_running_animation[4], True, False),pygame.transform.flip(self.right_running_animation[5], True, False)]
       self.portrait = pygame.image.load('characters/Naruto/portrait.png')
       self.stance =  pygame.image.load('characters/Naruto/Naruto stance.png')
    



    def images_list(self, path):
        images = os.listdir(path)
        image_list = []
        for i in images:
            image_list += [path+i]
        return image_list
    
    def load_images(self):
        self.jumping_right_animation = self.images_list(self.jumping_right_animation)
        self.jumping_left_animation = self.images_list(self.jumping_left_animation)
        self.right_running_animation = self.images_list(self.right_running_animation)
        self.left_running_animation = self.images_list(self.left_running_animation)
        self.portrait = self.images_list(self.portrait)
        self.stance = self.images_list(self.stance)
        
    
    def state_switcher(self): #Edit this to be able to change position depending on the maps starting point
        self.x_pos = 100
        return   

    #DRAWS ALL ACTIONS OF CHARACTER E.G. RUNNING,STANDING AND JUMPING 
    def draw(self):
         global runcount,jumpcount,x_pos,y_pos #drawing running animation took inspiration from 'Pygame Tutorial #3 - Character Animation & Sprites' Youtube Video by 'Tech with Tim'
         
         
         if self.runcount + 1>= 18:
            self.runcount = 0
            
            
         if self.left: #if left is =True then the below code will be run.
             if self.jumping: #checks if character is jumping
                 #cycles through the different jump animations
                 if self.jumpcount >= 2:
                     screen.blit(self.jumping_left_animation[0],(self.x_pos,self.y_pos)) 
                 elif self.jumpcount <2 and  self.jumpcount>=-2:
                     screen.blit(self.jumping_left_animation[1],(self.x_pos,self.y_pos))
                 elif self.jumpcount <-2 and self.jumpcount>=-4:
                     screen.blit(self.jumping_left_animation[2],(self.x_pos,self.y_pos))
                 elif self.jumpcount <=-4 and  self.jumpcount>-8:
                     screen.blit(self.jumping_left_animation[3],(self.x_pos,self.y_pos))
                 else: #otherwise draw final jump animation
                     screen.blit(self.jumping_left_animation[4],(self.x_pos,self.y_pos)) 
                     
             #RUNNING LEFT ANIMATION        
             else: 
                 screen.blit(self.left_running_animation[self.runcount//3],(self.x_pos,self.y_pos+6))
                 self.runcount += 1
                 
         elif self.right:#if right is =True then the below code will be run
             if self.jumping: #checks if character is jumping
                 #cycles through the different jump animations
                 if self.jumpcount >= 2:
                     screen.blit(self.jumping_right_animation[0],(self.x_pos,self.y_pos)) 
                 elif self.jumpcount <2 and  self.jumpcount>=-2:
                     screen.blit(self.jumping_right_animation[1],(self.x_pos,self.y_pos))
                 elif self.jumpcount <-2 and self.jumpcount>=-4:
                     screen.blit(self.jumping_right_animation[2],(self.x_pos,self.y_pos))
                 elif self.jumpcount <=-4 and  self.jumpcount>-8:
                     screen.blit(self.jumping_right_animation[3],(self.x_pos,self.y_pos))
                 else: #otherwise draw final jump animation
                     screen.blit(self.jumping_right_animation[4],(self.x_pos,self.y_pos)) 
                     
             #RUNNING RIGHT ANIMATION  
             else: 
                 screen.blit(self.right_running_animation[self.runcount//3],(self.x_pos,self.y_pos+6))
                 self.runcount += 1
                 
         elif self.jumping: #checks if character is jumping
             #cycles through the different jump animations
             if self.jumpcount >= 2:
                 screen.blit(self.jumping_right_animation[0],(self.x_pos,self.y_pos)) 
             elif self.jumpcount <2 and  self.jumpcount>=-2:
                screen.blit(self.jumping_right_animation[1],(self.x_pos,self.y_pos))
             elif self.jumpcount <-2 and self.jumpcount>=-4:
                screen.blit(self.jumping_right_animation[2],(self.x_pos,self.y_pos))
             elif self.jumpcount <=-4 and  self.jumpcount>-8:
                screen.blit(self.jumping_right_animation[3],(self.x_pos,self.y_pos))
             else: #otherwise draw final jump animation
                screen.blit(self.jumping_right_animation[4],(self.x_pos,self.y_pos)) 
              
         else: #if both left,right and jumping are false then character must be standing and  below code is run
             screen.blit(self.stance,(self.x_pos,self.y_pos))
     
    
        
        
    def jump(self):#Jump feature below took inspiration from 'Pygame Tutorial #2 - Jumping and Boundaries' Youtube Video by 'Tech with Tim'
        if self.jumpcount >= -10: #each iteration the character Y position is decrease(Made to go up) until it reaches a negative jumpcount. in that case neg becomes negative and then starts increasing the characters y positon(made to go down). Until jump count is =-10. then the else clause is run.
                neg = 1
                if self.jumpcount <0:
                    neg = -1
                self.y_pos = self.y_pos - (self.jumpcount**2)/2 *neg #a quadratic formula that emulates the shape of a parabola.
                self.jumpcount -=1
                return
        else: #this runs when our jump is finished. i.e. lands back on the grouund
            self.jumping = False
            self.jumpcount= 10
            return
                
    #KEEPS TRACK OF USER INPUTS AND CARRIES OUT FUNCTIONS
    def key_inputs(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.x_pos>self.speed:
            self.x_pos -= self.speed #this moves the character by minusing the speed variable '5' from the characters x position.
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x_pos<(screen_width-self.width-self.speed): #this ensures the character doesnt go off screen
            self.x_pos += self.speed
            self.left = False
            self.right = True
        else:
            self.right = False
            self.left = False
            self.runcount = 0
        
        if not (self.jumping):#If you're not jumping then you're able to crawl(!add feature later!) and jump
            if keys[pygame.K_DOWN] and self.y_pos>(screen_width-self.height-self.speed):
                self.y_pos -= self.speed #change this to crawl feature
            if keys[pygame.K_UP]:
                self.right = False
                self.left = False
                self.jumping = True
                self.runcount = 0
        else:
            self.jump()

   
    
#pf = platform
Naruto_pf = Player_Platform_Mode() #Object with all the attributes above^

class Player_Battle_Mode(Player_Platform_Mode):
    def __init__(self,norm_attack= 'Naruto Combo',spec_attack1 = 'Naruto Rendan',ep_restore_move = 'Charge Chakra'): 
        #CHARACTER BATTLE STATS - hp = health points, ep = Energy points,norm = normal, spec = special,dmg = Damage, na=normal attack, sa = special attack, cost means energy/chakra point cost
        Player_Platform_Mode.__init__(self,name = 'Naruto',hp = 100,max_hp=100)
        self.x_pos=337
        self.y_pos=295
        self.ep,self.max_ep, = 100,100
        self.norm_attack,self.spec_attack1,self.ep_restore_move = norm_attack,spec_attack1,ep_restore_move
        self.na_dmg, self.sa1_dmg,self.ep_restore,self.critical_dmg = 8,12,18,15 
        self.na_cost, self.sa1_cost = 2,8
        self.alive = True
        self.attacking = False 
        self.turn = True     
        
        #CHARACTER ATTACK ANIMATIONS
        self.framecount = 0
        self.na_animation = [pygame.image.load('characters/Naruto/naruto combo A 1.png'),pygame.image.load('characters/Naruto/naruto combo A 2.png'),pygame.image.load('characters/Naruto/naruto combo A 3.png'),pygame.image.load('characters/Naruto/naruto combo A 4.png'),pygame.image.load('characters/Naruto/naruto combo A 5.png'),pygame.image.load('characters/Naruto/naruto combo A 6.png'),pygame.image.load('characters/Naruto/naruto combo A 7.png'),
                             pygame.image.load('characters/Naruto/naruto combo A 8.png'),pygame.image.load('characters/Naruto/naruto combo A 9.png'),pygame.image.load('characters/Naruto/naruto combo A 10.png'),pygame.image.load('characters/Naruto/naruto combo A 11.png')]
        self.na_attacking = False
        self.sa1_animation = [pygame.image.load('characters/Naruto/naruto rendan 1.png'), pygame.image.load('characters/Naruto/naruto rendan 2.png'), pygame.image.load('characters/Naruto/naruto rendan 3.png'), pygame.image.load('characters/Naruto/naruto rendan 4.png'), pygame.image.load('characters/Naruto/naruto rendan 5.png'), pygame.image.load('characters/Naruto/naruto rendan 6.png'), pygame.image.load('characters/Naruto/naruto rendan 7.png'), pygame.image.load('characters/Naruto/naruto rendan 8.png'), pygame.image.load('characters/Naruto/naruto rendan 9.png'), pygame.image.load('characters/Naruto/naruto rendan 10.png'), 
                              pygame.image.load('characters/Naruto/naruto rendan 11.png'), pygame.image.load('characters/Naruto/naruto rendan 12.png'), pygame.image.load('characters/Naruto/naruto rendan 13.png'), pygame.image.load('characters/Naruto/naruto rendan 14.png'), pygame.image.load('characters/Naruto/naruto rendan 15.png'), pygame.image.load('characters/Naruto/naruto rendan 16.png'), pygame.image.load('characters/Naruto/naruto rendan 17.png'), pygame.image.load('characters/Naruto/naruto rendan 18.png'), pygame.image.load('characters/Naruto/naruto rendan 19.png'), pygame.image.load('characters/Naruto/naruto rendan 20.png'), 
                              pygame.image.load('characters/Naruto/naruto rendan 21.png'), pygame.image.load('characters/Naruto/naruto rendan 22.png'), pygame.image.load('characters/Naruto/naruto rendan 23.png')]
        self.sa1_attacking = False
        self.chakra_charge_animation = [pygame.image.load('characters/Naruto/Naruto energy restore 1.png'),pygame.image.load('characters/Naruto/Naruto energy restore 2.png')]
        self.chakra_charging = False
        self.missing = False
        self.name_tag = pygame.image.load('characters/Name tags/naruto health bar.png')
        self.hp_bars = [pygame.image.load('characters/Name tags/yellow health.png'),pygame.image.load('characters/Name tags/red health.png')]
        self.hp_bar_x =17
        self.hp_bar_y =23
    
    
        
     #KEEPS TRACK OF USER INPUTS AND CARRIES OUT FUNCTIONS
    def key_inputs_battle(self,target):
        keys = pygame.key.get_pressed()
        #BEFORE I CAN PRESS ANYTHING IT CHECKS IF ITS MY TURN AND THE ENEMIES TURN IS FINISHED
        if self.turn == True and target.turn == False:
            #THEN CHECKS IF I'M NOT IN ATTACKING OR IN AN ATTACKING ANIMATION
            if not(self.attacking) and not (self.chakra_charging): 
                #CHECKS WHAT KEY AND ATTACK I CHOSE AND RUNS THAT ATTACK
                if keys[pygame.K_1]:
                    self.normal_attack(target)
                    
                if keys[pygame.K_2]:
                    self.special_attack1(target)

                    
                if keys[pygame.K_3]:
                    self.energy_restoration()  
        
 
    def normal_attack(self,target):
        global battle_update_text1
        self.attacking = True
        self.na_attacking = True
        
        na_no_energy_msg = f"\n{self.name} tried to use '{self.norm_attack}' but didn't have enough energy. {self.name}'s guard is now OPEN!"
        miss_chance = random.randint(0,100) #generates chance of missing
        critical_chance = random.randint(0,100) #genereates chance of hitting critical attack
        if miss_chance<=80: #below is what happens when i dont miss
            if critical_chance<=10: #checks if i land critical. 1/10 chance
                if self.ep>=self.na_cost: #checks if I have enough energy to even use the normal attack and land the critical
                    self.ep = self.ep-self.na_cost
                    total_dmg = self.na_dmg+self.critical_dmg
                    battle_update_text1 = f"{self.name} attacked {target.name} with {self.norm_attack} & landed a CRITICAL HIT! Total damage = {total_dmg} !"
                    target.hp = target.hp-total_dmg
                    if target.hp <=0: #checks if target is dead after that attack
                        target.alive = False
                        battle_update_text1 = f"Well done! you defeated {target.name}"
                        return 
                else:#what happens if i dont have enough energy
                    self.attacking = False
                    self.na_attacking = False
                    battle_update_text1 = f"{na_no_energy_msg}" #ADD NO ENRGY BOOLEAN IF POSSIBLE
                    return
            else: #what happens if its not a critical hit
                if self.ep>=self.na_cost:
                    self.ep = self.ep-self.na_cost
                    battle_update_text1 = f"{self.name} attacked {target.name} with '{self.norm_attack}' and dealt {self.na_dmg} damage"
                    target.hp = target.hp-self.na_dmg
                    if target.hp <=0:
                        target.alive = False
                        battle_update_text1 = f"Well done! You defeated {target.name}"
                        return 
                    return
                else: # what happens if i dont have enough energy 
                    self.attacking = False
                    self.na_attacking = False
                    battle_update_text1 = f"{na_no_energy_msg}"
                    return
        #what happens if you miss        
        else:
            self.missing =True
            if self.ep>=self.na_cost:#check if you have enough energy
                self.ep = self.ep-self.na_cost
                battle_update_text1 = f"{self.name} tried to use '{self.norm_attack}' on {target.name} but MISSED! {self.name}'s guard is now OPEN!"
                return 
            else:
                self.attacking = False
                self.na_attacking = False
                self.missing =False
                battle_update_text1 = f"{na_no_energy_msg}"
                return     
            
            
    def special_attack1(self,target):
        global battle_update_text1
        self.attacking = True
        self.sa1_attacking = True
        
        na_no_energy_msg = f"\n{self.name} tried to use '{self.spec_attack1}' but didn't have enough energy. {self.name}'s guard is now OPEN!"
        miss_chance = random.randint(0,100) #generates chance of missing
        critical_chance = random.randint(0,100) #genereates chance of hitting critical attack
        if miss_chance<=80: #below is what happens when i dont miss
            if critical_chance<=10: #checks if i land critical. 1/10 chance
                if self.ep>=self.sa1_cost: #checks if I have enough energy to even use the normal attack and land the critical
                    self.ep = self.ep-self.sa1_cost
                    total_dmg = self.sa1_dmg+self.critical_dmg
                    battle_update_text1 = f"{self.name} attacked {target.name} with {self.spec_attack1} and landed a CRITICAL HIT! Total Damage = {total_dmg}!"
                    target.hp = target.hp-total_dmg
                    if target.hp <=0: #checks if target is dead after that attack
                        target.alive = False
                        battle_update_text1 = f"Well done! you defeated {target.name}"
                        return 
                else:#what happens if i dont have enough energy
                    self.attacking = False
                    self.sa1_attacking = False
                    battle_update_text1 = f"{na_no_energy_msg}" #ADD NO ENRGY BOOLEAN IF POSSIBLE
                    return
            else: #what happens if its not a critical hit
                if self.ep>=self.sa1_cost:
                    self.ep = self.ep-self.sa1_cost
                    battle_update_text1 = f"{self.name} attacked {target.name} with '{self.spec_attack1}' and dealt {self.sa1_dmg} damage"
                    target.hp = target.hp-self.sa1_dmg
                    if target.hp <=0:
                        target.alive = False
                        battle_update_text1 = f"Well done! You defeated {target.name}"
                        return 
                    return
                else: # what happens if i dont have enough energy 
                    self.attacking = False
                    self.sa1_attacking = False
                    print(f"{na_no_energy_msg}")
                    return
        #what happens if you miss        
        else:
            self.missing =True
            if self.ep>=self.sa1_cost:#check if you have enough energy
                self.ep = self.ep-self.sa1_cost
                battle_update_text1 = f"{self.name} tried to use '{self.spec_attack1}' on {target.name} but MISSED! {self.name}'s guard is now OPEN!"
                return 
            else:
                self.attacking = False
                self.sa1_attacking = False
                self.missing =False
                battle_update_text1 = f"{na_no_energy_msg}"
                return
        
        
    def energy_restoration(self):
        global battle_update_text1
        self.chakra_charging = True
        if self.ep+self.ep_restore<=self.max_ep:
            self.ep=self.ep+self.ep_restore
            battle_update_text1 = f"{self.name} restored {self.ep_restore} EP with '{self.ep_restore_move}'"
            return
        else:
            self.energy = self.max_ep
            battle_update_text1 = f"{self.name} used '{self.ep_restore_move}' and maxed out their HP"
            return
    
        
    #DRAWS CHARACTERS ATTACKS AND MOVEMENTS IN BATTLE
    def draw_battle(self,enemy):
        if self.chakra_charging:
            if self.framecount + 1 >= ((len(self.chakra_charge_animation))*4):
                self.framecount = 0
                self.chakra_charging = False
                self.turn = False
                enemy.turn = True
                return
            screen.blit(self.chakra_charge_animation[self.framecount//4],(self.x_pos,self.y_pos))
            self.framecount+=1
                
        #Checks if 'self'(Player) is attacking.
        elif self.attacking:
            if self.missing:
                if self.na_attacking:
                    if self.framecount + 1 >= ((len(self.na_animation))*3):
                        #if we have reached the final frame,reset framecount to 0 and return
                        self.framecount = 0
                        self.attacking = False
                        self.missing = False
                        self.na_attacking = False
                        self.turn = False
                        enemy.turn = True
                        return
                    screen.blit(self.na_animation[self.framecount//3],(enemy.x_pos-self.width,self.y_pos))
                    self.framecount+=1
                    return
                if self.sa1_attacking:
                    #This runs the attack animation
                    if self.framecount + 1 >= ((len(self.sa1_animation))*3):
                        #if we have reached the final frame,reset framecount to 0 and return
                        self.framecount = 0
                        self.attacking = False
                        self.sa1_attacking = False
                        self.missing = False
                        self.turn = False
                        enemy.turn = True
                        return
                    screen.blit(self.sa1_animation[self.framecount//3],(enemy.x_pos-self.width,self.y_pos))
                    self.framecount+=1
                    return
                
            #IF NOT MISSING, THEN CHECK WHAT ATTACK PLAYER IS ATTACKING WITH
            elif self.na_attacking:
                    if self.framecount + 1 >= ((len(self.na_animation))*3):
                        #if we have reached the final frame,reset framecount to 0 and return
                        self.framecount = 0
                        self.attacking = False
                        self.missing = False
                        self.na_attacking = False
                        self.turn = False
                        enemy.turn = True
                        return
                    screen.blit(self.na_animation[self.framecount//3],(enemy.x_pos-self.width,self.y_pos))
                    self.framecount+=1
                    return
            #This section checks what attack 'self' is attacking with(Attack checker and drawer can be put here maybe.
            elif self.sa1_attacking:
                #This runs the attack animation
                if self.framecount + 1 >= ((len(self.sa1_animation))*3):
                    #if we have reached the final frame,reset framecount to 0 and return
                    self.framecount = 0
                    self.attacking = False
                    self.sa1_attacking = False
                    self.turn = False
                    enemy.turn = True
                    return
                screen.blit(self.sa1_animation[self.framecount//3],((enemy.x_pos-enemy.width),enemy.y_pos))
                self.framecount+=1
                return
        else:
            screen.blit(self.stance,(self.x_pos,self.y_pos))
            return
                   
    def draw_health_bar(self,enemy):
        #resize bars
        nametg_resize_x = 231
        nametg_resize_y = 130
        nametag_resized = pygame.transform.scale(self.name_tag,(nametg_resize_x,nametg_resize_y))
        screen.blit(nametag_resized,(10,10)) 
        enemy_nametg_resize_x = 231
        enemy_nametg_resize_y = 130
        enemy_nametag_resized = pygame.transform.scale(enemy.name_tag,(enemy_nametg_resize_x,enemy_nametg_resize_y))
        screen.blit(enemy_nametag_resized,(669,10))  
        hp_bar_resize_x = 155
        hp_bar_resize_y = 19
        yellow_bar_resized = pygame.transform.scale(self.hp_bars[0],(hp_bar_resize_x,hp_bar_resize_y))
        redbar_resized = pygame.transform.scale(self.hp_bars[1],(hp_bar_resize_x,hp_bar_resize_y))
        #Dynamically change hp colour
        if self.hp>=40 and self.hp<80:
            screen.blit(yellow_bar_resized,(10+(self.hp_bar_x*3.5),10+(self.hp_bar_y*3.5)))
        if self.hp<40:
            screen.blit(redbar_resized,(10+(self.hp_bar_x*3.5),10+(self.hp_bar_y*3.5)))
        
        if enemy.hp>=40 and enemy.hp<80:
            screen.blit(yellow_bar_resized,(669+(self.hp_bar_x*3.5),10+(self.hp_bar_y*3.5)))
        if enemy.hp<40:
            screen.blit(redbar_resized,(669+(self.hp_bar_x*3.5),10+(self.hp_bar_y*3.5)))
            
                    
    def Battle_Results_checker(self,target,target_pf ):
        #Were both alive
        if self.alive and target.alive:
            return
        #I'm alive and target is dead
        elif self.alive:
            target_pf.mission_completion = True
            game_state.state = 'stage_1_tutorial'
        #I'm dead    
        else:
            pygame.quit()
        
    
            
                
                
Naruto_battle = Player_Battle_Mode()


'''COMPUTER CLASSES SECTION'''


class Platform_NPC(): #Any characters that are not the main characters will be made from this class when in platform mode.
    def __init__(self,name = 'Kakashi',x_pos = 300,y_pos = 300,width = 26,height = 38,speed = 5 ):
       self.name=  name
       self.x_pos = x_pos 
       self.y_pos = y_pos
       self.width = width
       self.height = height
       self.speed = speed
       self.stance = pygame.image.load('characters/Kakashi/stance.png')
       self.mission_completion = False
    
    
    def draw(self): 
        screen.blit(self.stance,(self.x_pos,self.y_pos))

    
#For the below Characters, give them their x and y positions and width etc as arguments in their brackets. these positions is where they will be on the screen.
Kakashi_pf = Platform_NPC()

Sasuke_pf = Platform_NPC('Sasuke',)
Sasuke_pf.stance = pygame.image.load('characters/Sasuke/Sasuke npc stand.png')
Sasuke_pf.x_pos = 700
Sasuke_pf.y_pos = 224



class Battle_NPC(Platform_NPC):
    def __init__(self,norm_attack= 'Kakashi Combo A',spec_attack1 = 'Kakashi Combo B',na_dmg=8, sa1_dmg=12,critical_dmg=15):
        #ENEMY BATTLE STATS
        Platform_NPC.__init__(self,name ='Kakashi',x_pos = 563,y_pos = 290)
        self.hp,self.max_hp = 100,100
        self.na_dmg, self.sa1_dmg,self.critical_dmg = na_dmg, sa1_dmg,critical_dmg
        self.alive = True
        self.attacking = False
        self.turn = False
        
        self.norm_attack = norm_attack
        self.spec_attack1 = spec_attack1
        
       #ENEMY ATTACK ANIMATION
        self.framecount = 0
        self.na_animation= [pygame.image.load('characters/Kakashi/Combo A 1.png'),pygame.image.load('characters/Kakashi/Combo A 2.png'),pygame.image.load('characters/Kakashi/Combo A 3.png'),pygame.image.load('characters/Kakashi/Combo A 4.png'),
                            pygame.image.load('characters/Kakashi/Combo A 5.png'),pygame.image.load('characters/Kakashi/Combo A 6.png'),pygame.image.load('characters/Kakashi/Combo A 7.png'),pygame.image.load('characters/Kakashi/Combo A 8.png'),
                            pygame.image.load('characters/Kakashi/Combo A 9.png'),pygame.image.load('characters/Kakashi/Combo A 10.png'),pygame.image.load('characters/Kakashi/Combo A 11.png'),pygame.image.load('characters/Kakashi/Combo A 12.png'),
                            pygame.image.load('characters/Kakashi/Combo A 13.png')]
        self.na_attacking = False
        self.sa1_animation= [pygame.image.load('characters/Kakashi/Combo B 1.png'),pygame.image.load('characters/Kakashi/Combo B 2.png'),pygame.image.load('characters/Kakashi/Combo B 3.png'),pygame.image.load('characters/Kakashi/Combo B 4.png'),
                            pygame.image.load('characters/Kakashi/Combo B 5.png')]
        self.sa1_attacking = False
        self.portrait = pygame.image.load('characters/Kakashi/portrait.png')
        self.missing = False
        self.name_tag = pygame.image.load('characters/Name tags/Kakashi health bar.png')
        self.hp_bars = [pygame.image.load('characters/Name tags/yellow health.png'),pygame.image.load('characters/Name tags/red health.png')]
        self.hp_bar_x =18
        self.hp_bar_y =23
       
       
    def draw_NPC_battle(self,enemy ):
        #CHECKS IF PLAYER IS ATTACKING OR RESTORING ENERGY
        if enemy.attacking or enemy.chakra_charging:
            self.attacking = False
            screen.blit(self.stance,(self.x_pos,self.y_pos))
            return
        #CHECKS IF NPC IS CURRENTLY ATTACKING
        elif self.attacking:
            #CHECKS IF NPC MISSED THEIR ATTACK
            if self.missing:
                if self.na_attacking:
                    if self.framecount + 1 >= ((len(self.na_animation))*3):
                        #if we have reached the final frame,reset framecount to 0 and return
                        self.framecount = 0
                        self.attacking = False
                        self.na_attacking = False
                        self.missing = False
                        self.turn = False
                        enemy.turn = True
                        return
                    screen.blit(self.na_animation[self.framecount//3],(enemy.x_pos+enemy.width,self.y_pos))
                    self.framecount+=1
                    return
                if self.sa1_attacking:
                    if self.framecount + 1 >= ((len(self.sa1_animation))*3):
                        #if we have reached the final frame,reset framecount to 0 and return
                        self.framecount = 0
                        self.attacking = False
                        self.missing = False
                        self.sa1_attacking = False
                        self.turn = False
                        enemy.turn = True
                        return
                    screen.blit(self.sa1_animation[self.framecount//3],(enemy.x_pos+enemy.width,self.y_pos))
                    self.framecount+=1
                    return
                
            #CHECKS WHAT ATTACK WAS CHOSEN BY NPC
            elif self.na_attacking:
                    #This runs the attack animation
                    if self.framecount + 1 >= ((len(self.na_animation))*3):
                        #if we have reached the final frame,reset framecount to 0 and return
                        self.framecount = 0
                        self.attacking = False
                        self.na_attacking = False
                        self.missing = False
                        self.turn = False
                        enemy.turn = True
                        return
                    screen.blit(self.na_animation[self.framecount//3],(enemy.x_pos+enemy.width,self.y_pos))
                    self.framecount+=1
                    return
            elif self.sa1_attacking:
                #This runs the attack animation
                if self.framecount + 1 >= ((len(self.sa1_animation))*3):
                    #if we have reached the final frame,reset framecount to 0 and return
                    self.framecount = 0
                    self.attacking = False
                    self.sa1_attacking = False
                    self.turn = False
                    enemy.turn = True
                    return
                screen.blit(self.sa1_animation[self.framecount//3],((enemy.x_pos+enemy.width),enemy.y_pos))
                self.framecount+=1
                return

            
        
        
    def draw_NPC(self):
        screen.blit(self.stance,(self.x_pos,self.y_pos))
        return
    
    def NPC_normal_attack(self,target = Naruto_battle):
        global battle_update_text2
        #CHECKS IF ITS THE NPC'S TURN
        if self.turn == True:
            self.attacking = True
            self.na_attacking = True
            miss_chance = random.randint(0,100) #generates chance of missing
            critical_chance = random.randint(0,100) #genereates chance of hitting critical attack
            if miss_chance<=80: #below is what happens when i dont miss
                if critical_chance<=12: #checks if i land critical. 1/10 chance
                    total_dmg = self.na_dmg+self.critical_dmg
                    battle_update_text2 = f"{self.name} attacked {target.name} with {self.spec_attack1} and landed a CRITICAL HIT! Total damage = {total_dmg}!"
                    target.hp = target.hp-total_dmg
                    if target.hp <=0: #checks if target is dead after that attack
                        target.alive = False
                        battle_update_text2 = f"Well done! you defeated {target.name}"
                        return 
                else: #what happens if its not a critical hit
                    battle_update_text2 = f"{self.name} attacked {target.name} with '{self.spec_attack1}' and dealt {self.na_dmg} damage"
                    target.hp = target.hp-self.na_dmg
                    if target.hp <=0:
                        target.alive = False
                        battle_update_text2 = f"Well done! You defeated {target.name}"
                        return 
                    return
                    
            #what happens if you miss        
            else:
                self.missing =True
                battle_update_text2 = f"{self.name} tried to use '{self.spec_attack1}' on {target.name} but MISSED! {self.name}'s guard is now OPEN!"
        
    def NPC_special_attack1(self,target = Naruto_battle):
        global battle_update_text2
        #CHECKS IF ITS THE NPC'S TURN
        if self.turn == True:
            self.attacking = True
            self.sa1_attacking = True
            miss_chance = random.randint(0,100) #generates chance of missing
            critical_chance = random.randint(0,100) #genereates chance of hitting critical attack
            if miss_chance<=80: #below is what happens when i dont miss
                if critical_chance<=12: #checks if i land critical. 1/10 chance
                    total_dmg = self.sa1_dmg+self.critical_dmg
                    battle_update_text2 = f"{self.name} attacked {target.name} with {self.spec_attack1} and landed a CRITICAL HIT! Total damage = {total_dmg}!"
                    target.hp = target.hp-total_dmg
                    if target.hp <=0: #checks if target is dead after that attack
                        target.alive = False
                        battle_update_text2 = f"Well done! you defeated {target.name}"
                        return 
                else: #what happens if its not a critical hit
                    battle_update_text2 = f"{self.name} attacked {target.name} with '{self.spec_attack1}' and dealt {self.sa1_dmg} damage"
                    target.hp = target.hp-self.sa1_dmg
                    if target.hp <=0:
                        target.alive = False
                        battle_update_text2 = f"Well done! You defeated {target.name}"
                        return 
                    return
                    
            #what happens if you miss        
            else:
                self.missing =True
                battle_update_text2 = f"{self.name} tried to use '{self.spec_attack1}' on {target.name} but MISSED! {self.name}'s guard is now OPEN!"

        
    def NPC_attack_chooser(self,target = Naruto_battle):
        attack_chooser =   random.randint(0, 10)  
        if attack_chooser>4:
            self.NPC_normal_attack(target)
        else:
            self.NPC_special_attack1(target)
        

Kakashi_battle = Battle_NPC() 

Sasuke_battle = Battle_NPC('Uchiha Combo','Cursed Combo',10,13,16)
Sasuke_battle.name = 'Sasuke'
Sasuke_battle.stance = pygame.image.load('characters/Sasuke/Sasuke npc stance.png')
Sasuke_battle.damage_animation = pygame.image.load('characters/Sasuke/sasuke damage.png')
Sasuke_battle.na_animation = [pygame.image.load('characters/Sasuke/sasuke combo A 1.png'),pygame.image.load('characters/Sasuke/sasuke combo A 2.png'),pygame.image.load('characters/Sasuke/sasuke combo A 3.png'),pygame.image.load('characters/Sasuke/sasuke combo A 4.png'),pygame.image.load('characters/Sasuke/sasuke combo A 5.png'),pygame.image.load('characters/Sasuke/sasuke combo A 6.png'),
                              pygame.image.load('characters/Sasuke/sasuke combo A 7.png'),pygame.image.load('characters/Sasuke/sasuke combo A 8.png'),pygame.image.load('characters/Sasuke/sasuke combo A 9.png'),pygame.image.load('characters/Sasuke/sasuke combo A 10.png'),pygame.image.load('characters/Sasuke/sasuke combo A 11.png'),
                              pygame.image.load('characters/Sasuke/sasuke combo A 12.png'),pygame.image.load('characters/Sasuke/sasuke combo A 13.png'),pygame.image.load('characters/Sasuke/sasuke combo A 14.png'),pygame.image.load('characters/Sasuke/sasuke combo A 15.png')]
Sasuke_battle.sa1_animation = [pygame.image.load('characters/Sasuke/sasuke combo B 1.png'),pygame.image.load('characters/Sasuke/sasuke combo B 2.png'),pygame.image.load('characters/Sasuke/sasuke combo B 3.png'),pygame.image.load('characters/Sasuke/sasuke combo B 4.png'),pygame.image.load('characters/Sasuke/sasuke combo B 5.png'),
                               pygame.image.load('characters/Sasuke/sasuke combo B 6.png'),pygame.image.load('characters/Sasuke/sasuke combo B 7.png'),pygame.image.load('characters/Sasuke/sasuke combo B 8.png'),pygame.image.load('characters/Sasuke/sasuke combo B 9.png'),pygame.image.load('characters/Sasuke/sasuke combo B 10.png'),
                               pygame.image.load('characters/Sasuke/sasuke combo B 11.png'),pygame.image.load('characters/Sasuke/sasuke combo B 12.png'),pygame.image.load('characters/Sasuke/sasuke combo B 13.png'),pygame.image.load('characters/Sasuke/sasuke combo B 14.png'),
                               pygame.image.load('characters/Sasuke/sasuke combo B 15.png')]
Sasuke_battle.name_tag = pygame.image.load('characters/Name tags/sasuke health bar.png')
Sasuke_battle.hp_bar_y = 23
Sasuke_battle.hp_bar_x =17

    


'''GAME STATE SECTION'''

class Game_state: 
    def __init__(self):
        #When the game is first loaded up, stage_1_tutorial is loaded up via the 'state manager method'
        self.state = 'Title'
        self.battle ='Naruto vs Kakashi' 

    
    #checks keyboard inputs and what state you're in. whether its platform or RPG and changes key inputs accordingly
    def event_checker(self):
        keys = pygame.key.get_pressed() 
        #EXIT GAME CONTROLS
        for event in pygame.event.get():
            if event.type ==pygame.QUIT or keys[pygame.K_ESCAPE]: #if an event  'user presses the x button on the window' enters the queue it will lead below.
                pygame.quit() # quits the game
        
        #TITLE SCREEN CONTROLS
        if self.state == 'Title':
            if keys[pygame.K_RETURN]:
                self.state = 'stage_1_tutorial'
                
       
    def State_updater(self,Platform_player,Battle_player,Platform_NPC,fight_npc,map_name,previous_state, next_state = 'stage_1_tutorial', battle = None):
        global battle_update_text1, battle_update_text2
        if self.state == 'Title':
            screen.fill(fg_color)
            screen.blit(map_name.img,(0,0))
            return
        elif self.state ==  'battle_screen_stage':
            naruto_name_txt = text_font.render(f"{Battle_player.name}",1,(0,0,0))
            naruto_hp_text = text_font.render(f"HP: {Battle_player.hp}",1,(0,0,0))
            naruto_ep_text = text_font.render(f"EP: {Battle_player.ep}",1,(0,0,0))
            enemy_name_txt = text_font.render(f"{fight_npc.name}",1,(0,0,0))
            enemy_hp_text = text_font.render(f"HP: {fight_npc.hp}",1,(0,0,0))
            render_battletxt1 = battle_text_font.render(battle_update_text1,1,(0,0,0))
            render_battletxt2 = battle_text_font.render(battle_update_text2,1,(0,0,0))
            #DRAW BATTLE STAGE BACKGROUND IMAGE, PORTRAITS AND HEALTH BARS
            screen.blit(map_name.img,(0,0))
            Battle_player.draw_health_bar(fight_npc)
            #DRAW NPC STANDING
            fight_npc.draw_NPC()
            #CHECK FOR USER INPUTS
            Battle_player.key_inputs_battle(fight_npc)
            screen.blit(render_battletxt1,(10,550))
            screen.blit(render_battletxt2,(10,583))
            #DRAW THE RESULT OF THE USER INPUT.E.G. ATTACK ANIMATIONS
            Battle_player.draw_battle(fight_npc)
            #CHECKS IF FIGHTERS ARE STILL ALIVE AND IF THE FIGHT SHOULD CONTINUE
            Battle_player.Battle_Results_checker(fight_npc,Platform_NPC)
            #CHECKS IF IF ENEMY IS NOT ATTACK AND ITS HIS TURN. 
            if not (fight_npc.attacking) and fight_npc.turn ==True:
                #NPC/ENEMY ATTACK CALCULATIONS
                fight_npc.NPC_attack_chooser(Battle_player)
                screen.blit(render_battletxt2,(10,583))
            #DRAW ENEMY ATTACK. AND CONTINUES TO DRAW ATTACK AS LONG AS HE'S ATTACKING AND ITS HIS TURN
            fight_npc.draw_NPC_battle(Battle_player)
            #CHECKS IF FIGHTERS ARE STILL ALIVE AND IF THE FIGHT SHOULD CONTINUE
            Battle_player.Battle_Results_checker(fight_npc,Platform_NPC)
            screen.blit(naruto_name_txt,(10,400))
            screen.blit(naruto_hp_text,(10,450))
            screen.blit(naruto_ep_text,(10,500))
            screen.blit(enemy_name_txt,(650,400))
            screen.blit(enemy_hp_text,(650,450))
            return
        else: #DRAWS PLATFORM MAP IF NOT IN A TITLE SCREEN OR BATTLE SCREEN
            screen.blit(map_name.img,(0,0))
            screen.blit(Platform_player.portrait,(50,20))
            Platform_player.key_inputs()
            Platform_player.draw()
            if Platform_NPC != None:
                Platform_NPC.draw()
                if Platform_player.x_pos > (Platform_NPC.x_pos-Platform_NPC.width) and Platform_player.x_pos<(Platform_NPC.x_pos) and Platform_player.y_pos>(Platform_NPC.y_pos-Platform_NPC.height) and Platform_NPC.mission_completion == False :
                    self.state = 'battle_screen_stage' 
                    self.battle = battle
            #checks naruto's position on screen and changes gamestate/aka runs 'battle_scree_stage' method
            if Platform_player.x_pos >= map_name.exit_x_pos:
                Platform_player.state_switcher()
                self.state = next_state
            
            
    
    def state_manager(self): #Change 'game state' to self as you're refering to the object and not the general class!
        #changes the 'game_state' or what method is being run.
        if self.state == 'Title':
            self.State_updater(Naruto_pf,Naruto_battle,Kakashi_pf,Kakashi_battle,Title,None,'stage_1_tutorial')
            
        elif self.state == 'stage_1_tutorial':
             self.State_updater(Naruto_pf,Naruto_battle,Kakashi_pf,Kakashi_battle,stage_1_tutorial,'Title','Stage_2_minigame','Naruto vs Kakashi')
             
        elif self.state == 'Stage_2_minigame':
             self.State_updater(Naruto_pf,Naruto_battle,None,Kakashi_battle,Stage_2_minigame,'stage_1_tutorial','stage_5_sasuke_platform_p1')
            
        elif self.state == 'battle_screen_stage':
            if self.battle == 'Naruto vs Kakashi':
                self.State_updater(Naruto_pf,Naruto_battle,Kakashi_pf,Kakashi_battle,battle_screen_stage,'stage_1_tutorial',None,None)
            if self.battle == 'Naruto vs Sasuke':
                self.State_updater(Naruto_pf,Naruto_battle,Sasuke_pf,Sasuke_battle,Stage_6_final,'Stage_6_final',None,None)
            
        elif self.state == 'stage_5_sasuke_platform_p1':
            self.State_updater(Naruto_pf,Naruto_battle,None,Kakashi_battle,stage_5_sasuke_platform_p1,'Stage_2_minigame','stage_5_sasuke_platform_p2')
            
        elif self.state == 'stage_5_sasuke_platform_p2':
            self.State_updater(Naruto_pf,Naruto_battle,None,Kakashi_battle,stage_5_sasuke_platform_p2,'stage_5_sasuke_platform_p1','stage_5_sasuke_platform_p3')
            
        elif self.state == 'stage_5_sasuke_platform_p3':
            self.State_updater(Naruto_pf,Naruto_battle,None,Kakashi_battle,stage_5_sasuke_platform_p3,'stage_5_sasuke_platform_p2','stage_5_sasuke_platform_p4')
            
        elif self.state == 'stage_5_sasuke_platform_p4':
            self.State_updater(Naruto_pf,Naruto_battle,None,Kakashi_battle,stage_5_sasuke_platform_p4,'stage_5_sasuke_platform_p3','Stage_6_final')
            
        elif self.state == 'Stage_6_final':
            self.State_updater(Naruto_pf,Naruto_battle,Sasuke_pf,Sasuke_battle,Stage_6_final,'stage_5_sasuke_platform_p4','stage_1_tutorial','Naruto vs Sasuke')
            
        
    

        
    
    
    
    
        
game_state = Game_state()

#Main Game Loop
while running_game:
    #sets Frames per second. Currently 60 frames per second
    clock.tick(FPS)
                
    screen.fill(fg_color)
    #checks the current game state and carries out any changes.
    game_state.event_checker()
    game_state.state_manager()
    
    pygame.display.flip()




