import pygame
import os 


player_run = []
for i in range(20):
  player_run.append(pygame.image.load(f"Running/running_{i}.png"))
  player_run[i] = pygame.transform.scale(player_run[i], (200, 200))
  
player_idle = []
for i in range(19):
  player_idle.append(pygame.image.load(f"Idle/idle_{i:04}.png"))
for i in range(len(player_idle)):
  player_idle[i] = pygame.transform.scale(player_idle[i], (200, 200))


player_punching = []
for i in range(39):
  player_punching.append(pygame.image.load(f"Punching/punching_{i:04}.png"))
for i in range(len(player_punching)):
  player_punching[i] = pygame.transform.scale(player_punching[i], (200, 200))


  

animation_list = [player_idle,player_run,player_punching]
