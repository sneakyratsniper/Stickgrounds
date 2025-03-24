import pygame
from player_sprites import Player
from animations import animation_list


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_active = False
game_start = False
running = True
pygame.display.set_caption('Fighter')
dt = 0
#fonts
font = pygame.font.SysFont(None, 200)
font_2 = pygame.font.SysFont(None, 100)
font_3 = pygame.font.SysFont(None, 200)

font_4 = pygame.font.SysFont(None, 110)

#texts
winner_text = "e"
winner_colour = (0,0,255)
start_surf = font.render('STICKGROUNDS', True, (69,68,77))
start_rect = start_surf.get_rect(center = (640,240))
W_surf = font_2.render('W', True, (69,68,77))
W_rect = W_surf.get_rect(center = (375,400))

UP_surf = font_2.render('UP', True, (69,68,77))
UP_rect = W_surf.get_rect(center = (520,400))

start_2_surf = font_2.render('W + UP TO START', True, (69,68,77))
start_2_rect = start_2_surf.get_rect(center = (640,400))

#surfaces
background_surface = pygame.image.load('pngbackground.png').convert()
background_2_surface = pygame.image.load('pngstartscreen.jpg').convert()

#player = pygame.sprite.GroupSingle()
#player.add(Player())

player_1 = Player(1,animation_list)
player_2 = Player(2,animation_list)


def hp_bar():
    #HP bar
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((20, 15), (510, 60)))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((25, 20), (500, 50)))
    pygame.draw.rect(screen, (255, 255, 255),
                     pygame.Rect((25, 20), (5 * player_1.hp, 50)))
    #ULTIMATE bar
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((20, 95), (510, 30)))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((25, 100), (500, 20)))
    pygame.draw.rect(screen, (255, 255, 255),
                     pygame.Rect((25, 100), (5 * player_1.ult_meter, 20)))
    #HP bar
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((750, 15), (510, 60)))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((755, 20), (500, 50)))
    pygame.draw.rect(
        screen, (255, 255, 255),
        pygame.Rect((755 - (5 * player_2.hp - 500), 20), (5 * player_2.hp, 50)))
    #ULTIMATE bar
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((750, 95), (510, 30)))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((755, 100), (500, 20)))
    pygame.draw.rect(
        screen, (255, 255, 255),
        pygame.Rect((755 - (5 * player_2.ult_meter - 500), 100),
                    (5 * player_2.ult_meter, 20)))


def blurSurf(surface, amt):
  """
  Blur the given surface by the given 'amount'.  Only values 1 and greater
  are valid.  Value 1 = no blur.
  """
  if amt < 1.0:
      raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
  scale = 1.0/float(amt)
  surf_size = surface.get_size()
  scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
  surf = pygame.transform.smoothscale(surface, scale_size)
  surf = pygame.transform.smoothscale(surf, surf_size)
  return surf
def check_death():
  global winner_text,winner_colour
  if player_1.hp < player_2.hp:
    winner_text = "PLAYER 2 WINS"
    winner_colour = (255,0,0)
  if player_2.hp <= player_1.hp:
    winner_text = "PLAYER 1 WINS"
    winner_colour = (0,0,255)
  if player_1.hp <= 0 or player_2.hp <= 0:
    player_1.hp = 100
    player_2.hp = 100

    player_1.rect.x = 30
    player_2.rect.x = 1200
    return False
  else: return True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
          #player_1.double_click(event)
          #player_2.double_click(event)
          pass
        else:
          if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(f'Mouse clicked at {x}, {y}')
          keys = pygame.key.get_pressed()
          if keys[pygame.K_w]:
            W_surf = font_2.render('W', True, (0,0,255))
          elif keys[pygame.K_UP]:
            UP_surf = UP_surf = font_2.render('UP', True, (255,0,0))
          else:
            W_surf = font_2.render('W', True, (69,68,77))
            UP_surf = font_2.render('UP', True, (69,68,77))

          if keys[pygame.K_UP] and keys[pygame.K_w]:
              game_active = True
              game_start = True


    # fill the screen with a color to wipe away anything from last frame
    if game_active:


      #game
      current_time = pygame.time.get_ticks()
      screen.fill("purple")
      screen.blit(background_surface,(0,0))
      player_1.draw(screen)
      player_2.draw(screen)
      player_1.update(dt,player_2,screen)
      player_2.update(dt,player_1,screen)
      hp_bar()
      game_active = check_death()

    else:

      #start screen
      if game_start:
        screen.blit(blurSurf(background_2_surface,10),(0,0))
        win_surf = font_3.render(winner_text,True, winner_colour)
        win_rect = win_surf.get_rect(center = (640,200))
        screen.blit(win_surf,win_rect)
        screen.blit(start_2_surf,start_2_rect)
        screen.blit(W_surf,W_rect)
        screen.blit(UP_surf,UP_rect)

      #end screen
      else:


        screen.blit(blurSurf(background_2_surface,10),(0,0))
        screen.blit(start_surf,start_rect)
        screen.blit(start_2_surf,start_2_rect)
        screen.blit(W_surf,W_rect)
        screen.blit(UP_surf,UP_rect)






    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)


    dt = clock.tick(60) /1000# limits FPS to 60

pygame.quit()

