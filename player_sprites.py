import pygame
import os
from controls import PLAYER_CONTROLS
from attacks import Attack, ATTACKS

def clear():
  os.system("clear")


class Player(pygame.sprite.Sprite):

  def __init__(self, player, animation_list):
    super().__init__()
    self.player = player
    self.action = 0
    self.animation_list = animation_list
    self.animation_index = 0
    self.update_time = pygame.time.get_ticks()

    self.image = self.animation_list[self.action][
        self.animation_index]

    self.rect = pygame.Rect((30, 670) if self.player == 1 else (1000, 670),
      (100, 180))
    
    self.flip = self.player != 1

    self.current_time = pygame.time.get_ticks()

    self.gravity = 0

    self.cooldown = 0

    self.dash_cooldown = 0
    self.dash_double = 0
    self.dashing = False
    self.dash_timer = 0

    self.attack_time = 0
    self.attack_delay = 500
    self.attacking = False
    self.is_attacking = False
    self.combo = False

    self.power = 5
    self.attack_type = "punch"
    self.hit_frame = ATTACKS[self.attack_type].hit_frame

    
    self.blocking = False
    self.block_hp = 100
    
    self.block_cooldown = 0
    self.block_cooldown_time = 1500 

    self.hit = False
    self.hit_time = 0
    self.block_break = False
    self.block_break_time = 0 
    self.block_time = 0 

    self.hp = 100
    self.speed = 10
    self.hit_speed = self.speed / 3
    self.dash_speed = self.speed * 4

    self.ult_meter = 0
    self.ult_time = -10100
    self.ult_active = False
    self.last_clicked = ""

    self.ai_state = ""
    
  def player_input(self):
    global keys
    global controls 
    #keys = pygame.key.get_pressed()
    #controls = PLAYER_CONTROLS[self.player]

    keys = self.keys = pygame.key.get_pressed()
    controls = self.controls = PLAYER_CONTROLS[self.player]
    
    
    if keys[controls["jump"]] and self.rect.bottom >= 560 and not self.blocking and not self.block_break:
        self.gravity = -28

    if keys[controls["dash"]] and not self.dashing:
        self.dash_timer = self.current_time

    if keys[controls["left"]]:
        self.rect.x -= self.speed
        if self.rect.x <= 0:
            self.rect.x = 0

    if keys[controls["right"]]:
        self.rect.x += self.speed
        if self.rect.x >= 1080:
            self.rect.x = 1080

    
    if keys[controls["ult"]] and self.ult_meter == 100:
      self.ult_time = self.current_time

    
        
    if not self.is_attacking: #If not attacking
      
        if (keys[controls["left"]] or keys[controls["right"]]) and not (self.block_break or self.blocking) :
            self.update_action(1) #Running
                  
        else:
            self.update_action(0) #Idle
        
        if keys[controls["down"]] and not self.block_break and self.block_cooldown == 0:
            if not self.blocking:
                self.blocking = True
        else:
            if self.blocking:
                self.block_cooldown = self.current_time
            self.blocking = False
        
        for attack in ATTACKS:
         try: 
            if keys[controls[attack]]:
              self.attack_type = attack
              self.update_action(ATTACKS[self.attack_type].animation)
         except KeyError:
            pass
            

  def ai_input(self):
    clear()
    print(self.ai_state)
    if not self.is_attacking:
      if self.ai_state in ("CHASE","RETREAT") and not (self.block_break or self.blocking):
        self.update_action(1)
      else:
        self.update_action(0)
    
      if self.ai_state == "BLOCK" and not self.block_break and self.block_cooldown == 0:
        if not self.blocking:
            self.blocking = True
      else:
        if self.blocking:
            self.block_cooldown = self.current_time
        self.blocking = False
        
      if self.ult_meter == 100:
        self.ult_time = self.current_time
        
      if self.ai_state == "ATTACK":
        self.update_action(ATTACKS[self.attack_type].animation)

    

  def update_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.animation_index = 0
      self.update_time = pygame.time.get_ticks()
    self.is_attacking = self.action >= 2

  def animation(self):
    
    if self.is_attacking:
      self.animation_index += ATTACKS[self.attack_type].animation_speed
      
      if self.animation_index >= len(self.animation_list[self.action]) or self.hit or self.blocking or self.block_break:
        self.update_action(0)
        self.rect.x += ATTACKS[self.attack_type].displacement if not self.flip else -ATTACKS[self.attack_type].displacement
        
      elif int(self.animation_index) == ATTACKS[self.attack_type].hit_frame:
        self.attacking = True

      if int(self.animation_index) in range(*ATTACKS[self.attack_type].combo_frames) and keys[controls[ATTACKS[self.attack_type].name]]: #If attack is pressed again during combo frames..
        self.combo = True

      try: 
        if self.combo and int(self.animation_index) == ATTACKS[self.attack_type].combo_frames[1]:
          self.attack_type = ATTACKS[ATTACKS[self.attack_type].combo_attack].name
          self.update_action(ATTACKS[self.attack_type].animation)
          self.combo = False
      except KeyError:
        pass

    else:
      self.animation_index += 0.6
      if self.animation_index >= len(self.animation_list[self.action]):
        self.animation_index = 0

    self.image = self.animation_list[self.action][int(self.animation_index)]

  def dash(self, dt):
    if self.dash_double != 0:
      self.dash_double += dt
      # Reset after 0.5 seconds.
      if self.dash_double >= 0.5:
        self.dash_double = 0


  def attack(self, target, screen):
    
    if self.attacking:
      attack_rect = pygame.Rect((self.rect.centerx + (ATTACKS[self.attack_type].displacement if not self.flip else -ATTACKS[self.attack_type].size[0] -ATTACKS[self.attack_type].displacement)), self.rect.y+20, *ATTACKS[self.attack_type].size)
    
      
      pygame.draw.rect(screen, "red", attack_rect)
      
      if attack_rect.colliderect(target.rect):
        self.ult_meter += 10 if self.ult_active is False else 0
        if self.ult_meter >= 100:
          self.ult_meter = 100
        if not target.blocking:
          target.hp -= ATTACKS[self.attack_type].damage if not self.ult_active else ATTACKS[self.attack_type].damage*2
          target.hit = True
          target.attacking = False
          target.hit_time = pygame.time.get_ticks()
        else:
          target.block_hp -= ATTACKS[self.attack_type].block_damage
          if target.block_hp <= 0:
            target.block_hp = 0 
            target.block_break = True
            target.block_break_time = pygame.time.get_ticks()
      
      self.attacking = False


  def block(self):
    if not self.blocking and self.block_hp < 100:
      self.block_hp += 0.08

  def ult(self):
    if (self.current_time - self.ult_time < 10000):
      self.ult_active = True
      if not self.block_break and not self.blocking: self.speed = 20 
      self.ult_meter -= 0.33
    else:
      self.ult_active = False

  def dash_fun(self):
    if self.dash_cooldown == 0 and self.attacking is False and not self.block_break:
      if self.current_time - self.dash_timer < 200:
        self.hit = False
        self.dashing = True
        self.speed = self.dash_speed
      else:
        self.dashing = False
        self.dash_cooldown += 1

  def get_hit(self):
    if self.hit:
      self.speed = self.hit_speed
      if self.current_time - self.hit_time > 500:
        self.hit = False
    elif self.blocking:
      self.speed = self.hit_speed

    elif self.block_break:
      self.speed = 0 
      if self.current_time - self.block_break_time > 2000:
        self.block_break = False
        self.block_hp = 100

    else:
      self.speed = 10

  def cool_down(self):
  
    if self.dash_cooldown >= 20:
      self.dash_cooldown = 0
    elif self.dash_cooldown > 0:
      self.dash_cooldown += 1

    if self.block_cooldown > 0 and self.current_time - self.block_cooldown >= self.block_cooldown_time:
      self.block_cooldown = 0

  def apply_gravity(self):
    self.gravity += 1.8
    self.rect.y += self.gravity
    if self.rect.bottom >= 560:
      self.rect.bottom = 560

  def flip_image(self, target):
    if self.player == 1:
      if self.rect.x > target.rect.x:
        self.flip = True
      else:
        self.flip = False
    self.flip is True if self.rect.x > target.rect.x else False
    if self.player == 2:
      if self.rect.x < target.rect.x:
        self.flip = False
      else:
        self.flip = True

  def update(self, dt, target, screen):
    self.current_time = pygame.time.get_ticks()
    self.player_input() if self.ai_state == "" else self.ai_input()
    self.apply_gravity()
    self.cool_down()
    self.flip_image(target)
    self.animation()
    self.block()
    self.get_hit()
    self.ult()
    self.dash_fun()
    self.attack(target, screen)
    #self.hp_bar(screen)
    #self.dash(dt)

  def draw(self, screen):
    image = pygame.transform.flip(self.image, self.flip, False)
    screen.blit(image, image.get_rect(center=self.rect.center))
    
  def draw_with_camera(self, screen, camera):
    image = pygame.transform.flip(self.image, self.flip, False)
    screen.blit(image, (self.rect.x - camera.x, self.rect.y))
    
    


  '''def double_click(self,event):
    if event.type == pygame.KEYDOWN and self.dash_cooldown == 0 and self.attacking == False:
      if self.player == 1:
        if event.key == pygame.K_a:
          if self.dash_double == 0:  # First mouse click.
              self.dash_double = 0.001  # Start the timer.
          # Click again before 0.5 seconds to double click.
          elif self.dash_double < 0.5 and event.key == pygame.K_a:
              self.rect.x -= 150
              self.dash_double = 0
              self.dash_cooldown += 0.01
  
        if event.key == pygame.K_d:
          if self.dash_double == 0:  # First mouse click.
              self.dash_double = 0.001  # Start the timer.
          # Click again before 0.5 seconds to double click.
          elif self.dash_double < 0.5:
              self.rect.x += 150
              self.dash_double = 0
              self.dash_cooldown += 0.01
  
      else:
        if event.key == pygame.K_LEFT:
          if self.dash_double == 0:  # First mouse click.
              self.dash_double = 0.001  # Start the timer.
          # Click again before 0.5 seconds to double click.
          elif self.dash_double < 0.5:
              self.rect.x -= 150
              self.dash_double = 0
              self.dash_cooldown += 0.01
  
  
        if event.key == pygame.K_RIGHT:
          if self.dash_double == 0:  # First mouse click.
              self.dash_double = 0.001  # Start the timer.
          # Click again before 0.5 seconds to double click.
          elif self.dash_double < 0.25:
              self.rect.x += 150
              self.dash_double = 0
              self.dash_cooldown += 0.01
  '''


