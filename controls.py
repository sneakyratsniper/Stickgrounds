import pygame
PLAYER_CONTROLS = {
        1: {
                "jump": pygame.K_w,
                "left": pygame.K_a,
                "down": pygame.K_s,
                "right": pygame.K_d,
                "dash": pygame.K_LSHIFT,
                "punch": pygame.K_z,
                "kick":pygame.K_x,
                "ult": pygame.K_q,
                "punch_2":0
        },
        2: {
                "jump": pygame.K_UP,
                "left": pygame.K_LEFT,
                "down": pygame.K_DOWN,
                "right": pygame.K_RIGHT,
                "dash": pygame.K_RSHIFT,
                "punch": pygame.K_n,
                "kick":pygame.K_m,
                "ult": pygame.K_l,
                "punch_2":0

        }
}
