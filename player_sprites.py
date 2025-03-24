import pygame
import os


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
        self.animation_index].convert_alpha()

    self.rect = pygame.Rect((30, 670) if self.player == 1 else (1200, 670),
                            (200, 300))

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

    self.blocking = False

    self.hit = False
    self.hit_time = 0

    self.hp = 100
    self.power = 5
    self.speed = 10
    self.hit_speed = self.speed / 2
    self.dash_speed = self.speed * 4

    self.ult_meter = 0
    self.ult_time = -10100
    self.ult_active = False
    self.last_clicked = ""

    self.combo = 0
    self.combo_time = 0

  def player_input(self):
    keys = pygame.key.get_pressed()
    if self.player == 1:
      if keys[pygame.K_w] and self.rect.bottom >= 670:
        self.gravity = -20

      if keys[pygame.K_LSHIFT] and self.dashing is False:
        self.dash_timer = self.current_time

      if keys[pygame.K_a]:
        self.rect.x -= self.speed
        if self.rect.x <= 0:
          self.rect.x = 0

      if keys[pygame.K_d]:
        self.rect.x += self.speed
        if self.rect.x >= 1080:
          self.rect.x = 1080

      if self.action != 2:
        if keys[pygame.K_a] or keys[pygame.K_d]:
          self.update_action(1)
        else:
          self.update_action(0)

      if keys[pygame.K_q]:
        self.attack_input()

      if keys[pygame.K_s]:
        self.blocking = True
      else:
        self.blocking = False

      if keys[pygame.K_z] and self.ult_meter == 100:
        self.ult_time = self.current_time
    else:

      if keys[pygame.K_UP] and self.rect.bottom >= 670:
        self.gravity = -20

      if keys[pygame.K_LEFT]:
        self.rect.x -= self.speed
        if self.rect.x <= 0:
          self.rect.x = 0

      if keys[pygame.K_RIGHT]:
        self.rect.x += self.speed
        if self.rect.x >= 1080:
          self.rect.x = 1080

      if keys[pygame.K_RSHIFT] and self.dashing is False:
        self.dash_timer = self.current_time

      if keys[pygame.K_m]:
        self.attack_input()
      if keys[pygame.K_l] and self.ult_meter == 100:
        self.ult_time = self.current_time

      if self.action != 2:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
          self.update_action(1)
        else:
          self.update_action(0)

  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.animation_index = 0
      self.update_time = pygame.time.get_ticks()


  def animation(self):
    if self.action == 2:
      self.animation_index += 1
      temp = 0
      #temp = 25 if self.combo == 0 else 0
      if self.animation_index >= len(
          self.animation_list[self.action]) - temp or self.hit:
        self.animation_index = 0
        self.update_action(0)
        self.attacking = False

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

  def attack_input(self):
    if not self.attacking:
      self.attack_time = pygame.time.get_ticks()
    if self.combo == 0:
      self.combo_time = pygame.time.get_ticks()
    if self.cooldown == 0:
      self.attacking = True
      self.update_action(2)

  def attack(self, target, screen):

    if self.attacking and (self.current_time - self.attack_time
                           > self.attack_delay):

      attack_rect = pygame.Rect((self.rect.centerx + 20 - (100 * self.flip)),
                                self.rect.y, 50, self.rect.height)
      self.cooldown += 1

      if self.current_time - self.combo_time < 1000:
        self.combo += 1
        if self.combo >= 2:
          self.combo = 0
      else:
        self.combo = 0

      if attack_rect.colliderect(target.rect):
        self.ult_meter += 10 if self.ult_active is False else 0
        self.attacking = False
        if self.ult_meter >= 100:
          self.ult_meter = 100
        if not target.blocking:
          target.hp -= self.power
          target.hit = True
          target.attacking = False
          target.hit_time = pygame.time.get_ticks()

  def block(self):
    if self.blocking:
      pass
  def ult(self):
    if (self.current_time - self.ult_time < 10000):
      self.ult_active = True
      self.speed, self.power = 20, 10
      self.ult_meter -= 0.33
    else:
      self.ult_active = False
      self.power = 5

  def dash_fun(self):
    if self.dash_cooldown == 0 and self.attacking is False:
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
    else:
      self.speed = 10

  def cool_down(self):
    if self.cooldown >= 20:
      self.cooldown = 0
    elif self.cooldown > 0:
      self.cooldown += 1

  def dash_cool_down(self):
    if self.dash_cooldown >= 20:
      self.dash_cooldown = 0
    elif self.dash_cooldown > 0:
      self.dash_cooldown += 1

  def hp_bar(self, screen):
    if self.player == 1:
      #HP bar
      pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((20, 15), (510, 60)))
      pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((25, 20), (500, 50)))
      pygame.draw.rect(screen, (255, 255, 255),
                       pygame.Rect((25, 20), (5 * self.hp, 50)))
      #ULTIMATE bar
      pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((20, 95), (510, 30)))
      pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((25, 100), (500, 20)))
      pygame.draw.rect(screen, (255, 255, 255),
                       pygame.Rect((25, 100), (5 * self.ult_meter, 20)))
    else:
      #HP bar
      pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((750, 15), (510, 60)))
      pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((755, 20), (500, 50)))
      pygame.draw.rect(
          screen, (255, 255, 255),
          pygame.Rect((755 - (5 * self.hp - 500), 20), (5 * self.hp, 50)))
      #ULTIMATE bar
      pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((750, 95), (510, 30)))
      pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((755, 100), (500, 20)))
      pygame.draw.rect(
          screen, (255, 255, 255),
          pygame.Rect((755 - (5 * self.ult_meter - 500), 100),
                      (5 * self.ult_meter, 20)))

    player_colour = pygame.draw.rect(screen,
                                     (0, 0, 255) if self.player == 1 else
                                     (255, 0, 0),
                                     (self.rect.x, self.rect.y + 200, 200, 10))
    player_colour.center = (self.rect.midbottom)

  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= 670:
      self.rect.bottom = 670

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
    self.player_input()
    self.apply_gravity()
    self.cool_down()
    self.dash_cool_down()
   # self.hp_bar(screen)
    self.flip_image(target)
    #self.dash(dt)
    self.animation()
    self.attack(target, screen)
    self.block()
    self.get_hit()
    self.ult()
    self.dash_fun()
    print(self.gravity)
  def draw(self, screen):
    image = pygame.transform.flip(self.image, self.flip, False)
    screen.blit(image, (self.rect))



'''
def double_click(self,event):
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


