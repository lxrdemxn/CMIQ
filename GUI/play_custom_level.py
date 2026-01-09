# Play custom level - Similar to main.py but for custom levels
import pygame
from settings import parametres
from player import *
from level import *
import os
from buttons import *
import sys

# Get the custom level map from command line argument or default
if len(sys.argv) > 1:
    import json
    custom_level_map = json.loads(sys.argv[1])
else:
    # Default empty level if no argument provided
    custom_level_map = []

# Check if map is valid
if not custom_level_map or len(custom_level_map) == 0:
    print("Error: No level map provided!")
    print("Usage: python play_custom_level.py '<map_json>'")
    sys.exit(1)

# Initialisation de Pygame
pygame.init()

file_path = "GUI/play_custom_level.py"

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((parametres.screen_width, parametres.screen_height))
pygame.display.set_caption("Custom Level - " + parametres.nom_jeu)
g = os.path.join("graphics","backgrounds", "background5.png")
bg = pygame.image.load(g).convert()

# Chargement des images des boutons
replay_button = button('graphics/end_screen/replay_button_normal.png','graphics/end_screen/replay_button_hover.png')
replay_button.resize(230,90)
replay_rect = replay_button.rect((parametres.screen_width//2,parametres.screen_height//1.5))

pause_screen = pygame.image.load('graphics/pause_screen/pause_icon.png').convert_alpha()
pause_screen_rect = pause_screen.get_rect(center=(parametres.screen_width // 2, parametres.screen_height // 2))

# Initialisation de l'horloge
clock = pygame.time.Clock()

# Initialisation du niveau avec la carte personnalisée
level = Level(custom_level_map, screen)
paused = False
run = True
level.wahd(bg)

# boucle d'éxecution
while run:
    for event in pygame.event.get():
        # fermeture de l'écran par le boutton X de la fenêtre
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            # fermeture de l'écran par le boutton "ECHAPE"
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                # Return to level editor
                import subprocess
                import os
                editor_path = os.path.join(os.path.dirname(file_path), 'level_editor_example.py')
                subprocess.run([sys.executable, editor_path])
                sys.exit()
                
        if event.type == pygame.KEYDOWN:
            # au cas d'un click sur le boutton "P"
            if event.key == pygame.K_p:
                if not paused and not level.isgameover:
                    level.pause = True
                    paused = True
                else:
                    level.pause = False
                    paused = False
                    
        if event.type == pygame.MOUSEBUTTONDOWN and (level.isgameover or level.win):
            # au cas d'un click sur le boutton "PLAY AGAIN"
            if replay_rect.collidepoint(event.pos):
                # Reinitialize the level without closing the window
                level = Level(custom_level_map, screen)
                paused = False
                level.wahd(bg)
    
    # Appel à la méthode pour dessiner le niveau
    level.draw_level(bg)
    
    if level.isgameover:
        # Gestion de l'état "game over"
        level.pause = True
        mouse_pos = pygame.mouse.get_pos()
        if replay_rect.collidepoint(mouse_pos):
            replay_button.is_hovered = False
        else:
            replay_button.is_hovered = True
            
        replay_button.draw(screen, replay_rect.topleft)
    
    if level.win:
        # Gestion de l'état "victoire"
        with open("GUI/youwon.py") as f:
            code = f.read()
            exec(code)
            
    # Affichage de l'écran de pause
    if paused:
        screen.blit(pause_screen, pause_screen_rect.topleft)
    
    pygame.display.update()

    # Limitation du taux de rafraîchissement de l'écran
    clock.tick(parametres.fps)

# Fermeture de Pygame
pygame.quit()
