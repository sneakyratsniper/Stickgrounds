import pygame

root_path = "/mnt/chromeos/GoogleDrive/SharedWithMe/1956/Pygame-Fighter/"

player_run = []
for i in range(20):
        player_run.append(pygame.image.load(root_path + f"Running/running_{i}.png"))
        player_run[i] = pygame.transform.scale(player_run[i], (200, 200))
    
player_idle = []
for i in range(18):
        player_idle.append(pygame.image.load(root_path + f"Idle/idle_{i:04}.png"))
        player_idle[i] = pygame.transform.scale(player_idle[i], (200, 200))


player_punching_1 = []
for i in range(19):
        player_punching_1.append(pygame.image.load(root_path + f"Punching/Punching1/punching_1_{i:04}.png"))
        player_punching_1[i] = pygame.transform.scale(player_punching_1[i], (200, 200))
    
player_punching_2 = []
for i in range(27):
        player_punching_2.append(pygame.image.load(root_path + f"Punching/Punching2/punching_2_{i:04}.png"))
        player_punching_2[i] = pygame.transform.scale(player_punching_2[i], (200, 200))


player_kicking = []
for i in range(34):
        player_kicking.append(pygame.image.load(root_path + f"Kicking/kicking_{i:04}.png"))
        player_kicking[i] = pygame.transform.scale(player_kicking[i], (200,200))

animation_list = [player_idle,player_run,player_punching_1,player_punching_2,player_kicking]
