import pygame
from tiles import *
from inf_settings import parametres_inf
from player import *
from particles import ParticleEffect
from audio import *
import numpy as np

class Inf_Level:
    def __init__(self, screen):
        """
        Initialise un niveau avec une carte et un écran.

        Arguments :
        - map (list) : Une liste représentant la carte du niveau.
        - screen (pygame.Surface) : La surface d'affichage du jeu.

        Attributs :
        - window (pygame.Surface) : La surface d'affichage du jeu.
        - tiles (pygame.sprite.Group) : Groupe de sprites représentant les tuiles du niveau.
        - player (pygame.sprite.GroupSingle) : Groupe de sprite représentant le joueur.
        - deplacement (int) : Valeur de déplacement horizontale du niveau.
        - idle (bool) : Indicateur si le joueur est immobile ou non.
        """
        self.window = screen
        self.map_0 = []
        self.deplacement = 0
        self.idle = False
        self.isincollisionh = False
        self.isgameover =False
        self.pause = False
        self.win=False
        self.dust_sprite = pygame.sprite.Group()
        self.player_on_ground = False
        self.bgx = 0  # Position horizontale du background
        self.world_offset = 0  # Track how many columns have been removed from the map
        # player
        self.score = 0
        self.n=3
        self.n_lines = len(parametres_inf.blocks_bank[0])
        self.m = len(parametres_inf.blocks_bank[0][0])
        # coins
        self._7amra = 0
        self.dirham = 0
        self.deplacement_counter = 0

        self.obstacles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.bull = pygame.sprite.GroupSingle()
        self.ground=pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()  # Groupe pour les power-ups
        self.buses=pygame.sprite.Group()
        a= Bull(-50,100,150,450)
        self.bull.add(a)

        self.loading_level(parametres_inf.blocks_bank[1::])

    def cat_map(self, random_blocks:list[str]):
        """_summary_
            concatenates the actual map with a new map block chosen randomly
        Args:
            random_blocks (list[str]) : A list of random blocks
        """
        new_block = random_blocks[np.random.choice(range(1, len(random_blocks)))]
        n = len(new_block)
        m = len(new_block[0])

        new_map = [(self.map_0[x][m::] + new_block[x]) for x in range(n)]
        
        self.map_0 = new_map
        self.world_offset += m  # Track how many columns we've removed

    def draw_map(self,n, m, start_col=0):
        """_summary_

        Args:
            n (int): number of lines
            m (int): number of rows
            start_col (int): starting column index to begin drawing from
            map (list[str]): the defined map to draw
        """
        for i in range(n):
            for j in range(start_col, m):
                # Calculate world position: map index + world offset gives absolute world column
                # Then add bgx to match the current scroll state of existing tiles
                world_x = (j + self.world_offset) * parametres_inf.tile_size + self.bgx
                
                if self.map_0[i][j] == "X":
                    pos = (world_x, 100 + i * parametres_inf.tile_size)
                    tile = Obstacle(pos, parametres_inf.tile_size,"graphics/backgrounds/tuila.jpg")
                    self.obstacles.add(tile)
                elif self.map_0[i][j] == "P":
                    p = Player(world_x, 100+i * parametres_inf.tile_size,self.window)
                    self.player.add(p)
                elif self.map_0[i][j]=="G":
                    pos=(world_x, 100+i * parametres_inf.tile_size)
                    tile = Ground(pos, parametres_inf.tile_size)
                    self.ground.add(tile)
                elif self.map_0[i][j] == "S":  # Bouclier
                    pos = (world_x, 100 + i * parametres_inf.tile_size)
                    powerup = Coin(pos, parametres_inf.tile_size, 2, "graphics/coins/shield.png")  # Utiliser une image différente
                    self.powerups.add(powerup)
                elif self.map_0[i][j]=="0":
                    pos = (world_x, 100+i * parametres_inf.tile_size)
                    coin = Coin(pos, parametres_inf.tile_size, 0, "graphics/coins/1dh.png")
                    self.coins.add(coin)
                elif self.map_0[i][j]=="1":
                    pos = (world_x, 100+i * parametres_inf.tile_size)
                    coin = Coin(pos, parametres_inf.tile_size, 1, "graphics/coins/10dh.png")
                    self.coins.add(coin)
                elif self.map_0[i][j]=="B":
                    g = BUS((world_x,100+i*parametres_inf.tile_size),"graphics/backgrounds/bus.png")
                    self.obstacles.add(g)                
                elif self.map_0[i][j] == "A":  # Aimant
                    pos = (world_x, 100 + i * parametres_inf.tile_size)
                    powerup = Coin(pos, parametres_inf.tile_size, 3, "graphics/coins/magnet.png")  # Utiliser une image différente
                    self.powerups.add(powerup)
                elif self.map_0[i][j]=="M":    
                    pos = (world_x, 100+i * parametres_inf.tile_size)
                    mv_tile = Obstacle(pos, parametres_inf.tile_size,"graphics/backgrounds/tuila.jpg", is_moving = True)
                    self.obstacles.add(mv_tile)
                elif self.map_0[i][j]=="W":
                    g = BUS((world_x,100+i*parametres_inf.tile_size),"graphics/backgrounds/mur.png",size = (100,363))
                    self.obstacles.add(g)
    
    def loading_level(self, random_blocks):
        """
        Charge le niveau en fonction de la carte donnée.

        Arguments :
        - random_blocks (list) : Une liste représentant la carte du niveau.
        """
        
        n = len(random_blocks[0])
        m = len(random_blocks[0][0])

        init_blocks = [random_blocks[0]] + [random_blocks[np.random.choice(range(1,len(random_blocks)))] for _ in range(2)]

        self.map_0 = [(init_blocks[0][k]+init_blocks[1][k]+init_blocks[2][k]) for k in range(n)]

        self.draw_map(n, len(self.map_0[0]))
        
        # Ensure player exists - if not created from map, create manually at column 5 (6th column)
        if len(self.player.sprites()) == 0:
            player_x = 5 * parametres_inf.tile_size  # Column 5 (0-indexed = 6th column)
            player_y = 100 + (n - 2) * parametres_inf.tile_size
            p = Player(player_x, player_y, self.window)
            self.player.add(p)
             
                
    def bordure_x(self):
        """
        Gère les bordures horizontales du niveau pour le déplacement du joueur.
        """
        p = self.player.sprite
        if p is None:
            return
            
        if p.rect.centerx < parametres_inf.screen_width / 2 and p.direction.x < 0:
            self.deplacement = parametres_inf.vitesse_joueur
            p.v = 0
        elif p.rect.centerx >  parametres_inf.screen_width / 2 and p.direction.x > 0:
            self.deplacement = -parametres_inf.vitesse_joueur
            p.v = 0
        else:
            self.deplacement = 0
            p.v = parametres_inf.vitesse_joueur
            
    def update_bgx(self,deplacement):
        """
        Met à jour la position horizontale du background en fonction du déplacement donné.

        Arguments :
        - deplacement (int) : Valeur du déplacement horizontal.
        """
        self.bgx += deplacement
        self.deplacement_counter += abs(deplacement)  # Track actual distance, not frames

    def collision_hori(self):
        """
        Gère les collisions horizontales du joueur et du taureau avec les tuiles du niveau.
        Le bouclier permet de détruire le bloc en collision ainsi que tous les blocs au-dessus et au-dessous.
        """
        p = self.player.sprite
        b = self.bull.sprite
        p.rect.x += p.direction.x * p.v
        i = 0
        listes_obstaclesandbuses = list(self.obstacles.sprites()) +list(self.buses.sprites())
        for sprite in listes_obstaclesandbuses:
            # Collision joueur avec un obstacle
            if sprite.rect.colliderect(p.rect):
                if p.has_shield:  # Si le bouclier est actif
                    # Détruire l'obstacle principal
                    self.ajoute_particules(sprite.rect.center, "explosion")
                    sprite.kill()
                    music('./music/destroy.mp3', 0.5)

                    # DÉTRUIRE LES BLOCS AU-DESSUS ET EN-DESSOUS
                    obstacle_rect = sprite.rect  # Position de l'obstacle détruit
                    blocks_to_destroy = [
                        s for s in self.obstacles.sprites()
                        if s.rect.x == obstacle_rect.x and
                        (s.rect.y == obstacle_rect.y - parametres_inf.tile_size or  # Au-dessus
                        s.rect.y == obstacle_rect.y + parametres_inf.tile_size)   # En-dessous
                    ]
                    for block in blocks_to_destroy:
                        self.ajoute_particules(block.rect.center, "explosion")
                        block.kill()
                    music('./music/destroy.mp3', 1)
                    # Désactiver le bouclier après destruction
                    p.has_shield = False

                else:  # Collision sans bouclier
                    if p.direction.x < 0:
                        p.rect.left = sprite.rect.right
                        i += 1
                        self.isincollisionh = True
                    elif p.direction.x >= 0:
                        p.rect.right = sprite.rect.left
                        i += 1
                        self.isincollisionh = True

            # Collision taureau avec un obstacle
            if sprite.rect.colliderect(b.rect) or b.rect.right > sprite.rect.left:
                self.ajoute_particules(sprite.rect.center, "explosion")
                sprite.kill()
                music('./music/destroy.mp3', 0.2)

        if i == 0:
            self.isincollisionh = False
            
    def collision_torro(self):
        """
        Vérifie les collisions entre le joueur et le taureau.
        Met à jour l'état du jeu si une collision est détectée.
        """

        p = self.player.sprite
        p.rect.x += p.direction.x * p.v
        for sprite in self.bull.sprites():
            if sprite.rect.colliderect(p.rect):
                if p.rect.left <= sprite.rect.right:
                    music('./music/losing.wav', 0.5)
                    self.isgameover = True

    def collision_ver(self):
        """
        Gère les collisions verticales du joueur avec les tuiles du niveau.
        """
        p = self.player.sprite
        p.apply_gravity()
        frappe = [
            sprite for sprite in self.obstacles.sprites() if sprite.rect.colliderect(p.rect)
        ]
        frappe += [sprite for sprite in self.ground.sprites() if sprite.rect.colliderect(p.rect)]
        frappe += [sprite for sprite in self.buses.sprites() if sprite.rect.colliderect(p.rect)]

        if p.direction.y > 0:
            for i in frappe[::-1]:
                p.rect.bottom = i.rect.top
                p.direction.y = 0
                p.terre = True
                break
        elif p.direction.y < 0:
            for i in frappe:
                p.rect.top = i.rect.bottom
                p.direction.y = 0
                p.terre = False
                break
        if len(frappe) == 0:
            p.terre = False
            if p.direction.y > p.gravity:
                p.status = "fall"
    
    def get_player_on_ground(self):
        """
        Vérifie si le joueur est sur le sol.
        Met à jour l'état du joueur en fonction de sa position par rapport au sol.
        """
        if self.player.sprite.terre:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
                
    def draw_shield(self, surface):
        """
        Affiche une image de halo autour du joueur si le bouclier est actif.
        """
        p = self.player.sprite  # Référence au joueur
        if p.has_shield:
            # Charger l'image du halo
            halo_image = pygame.image.load('graphics/backgrounds/halo.png').convert_alpha()  # Assurez-vous que l'image existe et utilise convert_alpha() pour la transparence

            # Calculer la position et la taille du halo
            halo_center = p.rect.center  # Centre du halo sur le joueur
            halo_size = max(p.rect.width, p.rect.height) * 1.5  # Taille du halo, un peu plus grand que le joueur

            # Redimensionner l'image du halo pour qu'elle entoure bien le joueur
            halo_image = pygame.transform.scale(halo_image, (int(halo_size), int(halo_size)))
            halo_image.set_alpha(150)  # Réduire l'alpha pour rendre l'image plus transparente (0 = complètement transparent, 255 = opaque)

            # Dessiner l'image du halo sur l'écran
            halo_rect = halo_image.get_rect(center=halo_center)  # Positionner l'image du halo
            surface.blit(halo_image, halo_rect)  # Afficher le halo
            self.player.draw(surface)

    def ajoute_particules(self, pos,move):
        """
        Ajoute des particules d'effet de saut à la position donnée.
        Args:
        pos (tuple): Position où les particules d'effet de saut doivent être créées.
        """
        particule_sprite = ParticleEffect(pos, move)
        self.dust_sprite.add(particule_sprite)
        
    def handle_player_particles(self):
        """
        Gère la création et l'affichage des particules pour le joueur.
        Ajoute des particules pour les actions de saut et de course.
        """
        player=self.player.sprite
        if player is None:  # Safety check
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.ajoute_particules(player.rect.midbottom,"run")
        if keys[pygame.K_SPACE]:
            if player.terre:
                self.ajoute_particules(player.rect.midbottom,"jump")
        if not player.terre and player.direction.y > 0:  # En l'air et en train de descendre
            player.was_in_air = True  # Marque que le joueur était en l'air

        if player.terre and getattr(player, "was_in_air", False):  # Atterrissage détecté
            self.ajoute_particules(player.rect.midbottom, "land")
            player.was_in_air = False  # Réinitialise après l'atterrissage
           
    def hit_coin(self):
        """
        Gère la collecte des pièces par le joueur.
        Détecte les collisions entre le joueur et les pièces, et met à jour le score en fonction du type de pièce collectée.
        """
        p = self.player.sprite
        coins = self.coins.sprites()
        coins_collision = [c for c in coins if c.rect.colliderect(p.rect)]
        powerups_collision = [pu for pu in self.powerups.sprites() if pu.rect.colliderect(p.rect)]

        if coins_collision:
            for coin in coins_collision:
                if coin.val == 0:
                    self._7amra += 1
                    self.score += 20
                elif coin.val == 1:
                    self.dirham += 1
                    self.score += 200
                coin.kill() 
                music('./music/coin.wav', 0.3)        
        for powerup in powerups_collision:
            if powerup.val==2:
                self.player.sprite.has_shield = True  # Activer le bouclier
                music('./music/power_up.wav', 0.3)
                powerup.kill() 
                
                
            elif powerup.val ==3:
                self.player.sprite.activate_magnet()
                powerup.kill()

    # Fonction pour afficher le score
    def draw_score(self, surface):
        """
        Affiche le score actuel sur la surface donnée.

        Arguments :
        - surface (pygame.Surface) : La surface où le score sera affiché.
        """

        # Police pour le texte
        font = pygame.font.Font("pixel_font.ttf", 36)  
        # Créer un rectangle pour contenir le score
        rect_width, rect_height = 200, 50
        rect_x, rect_y = parametres_inf.screen_width - rect_width - 10, 10  # Position du rectangle
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        # Dessiner le rectangle
        pygame.draw.rect(surface,(0,0,0), rect, 2, border_radius=10)
        # Dessiner le texte du score
        score_text = font.render(f"Score: {self.score}", True, (0,0,0))
        text_rect = score_text.get_rect(center=rect.center)
        surface.blit(score_text,text_rect)
                
    def wahd(self,bg):
        """
        Affiche un compte à rebours de 3 secondes avant le début du niveau.

        Arguments :
        - bg (pygame.Surface) : Le fond d'écran actuel du niveau.
        """

        one = pygame.image.load('graphics/countdown/1.png').convert_alpha()
        two = pygame.image.load('graphics/countdown/2.png').convert_alpha()
        three = pygame.image.load('graphics/countdown/3.png').convert_alpha()

        # Définir les rectangles pour centrer les images
        one_rect = one.get_rect(center=(parametres_inf.screen_width // 2, parametres_inf.screen_height // 2))
        two_rect = two.get_rect(center=(parametres_inf.screen_width // 2, parametres_inf.screen_height // 2))
        three_rect = three.get_rect(center=(parametres_inf.screen_width // 2, parametres_inf.screen_height // 2))
        self.draw_level(bg)
        self.window.blit(one, one_rect.topleft)
        pygame.display.update()
        music('./music/beep1.wav', 1)
        pygame.time.delay(1000)
          

        self.draw_level(bg)
        self.window.blit(two, two_rect.topleft)
        pygame.display.update()
        music('./music/beep1.wav', 1)
        pygame.time.delay(1000)

        self.draw_level(bg)
        self.window.blit(three, three_rect.topleft)
        pygame.display.update()
        music('./music/beep2.wav', 1)
        pygame.time.delay(1000)
        
    def collect_nearby_coins(self):
        """
        Attire les pièces à proximité du joueur grâce à l'effet de l'aimant.
        Met à jour les positions des pièces et les collecte si elles atteignent le joueur.
        """
        p = self.player.sprite  # Référence au joueur
        for coin in self.coins.sprites():
            distance = pygame.math.Vector2(p.rect.centerx - coin.rect.centerx, p.rect.centery - coin.rect.centery)
            distance = distance.length()

            if distance < p.magnet_range:  # Si la pièce est dans la portée du magnet
                self.attract_coin(p, coin)

    def attract_coin(self, player, coin):
        """
        Attire une pièce vers le joueur.

        Arguments :
        - player (Player) : Le sprite représentant le joueur.
        - coin (Coin) : La pièce à attirer vers le joueur.
        """
        direction = pygame.math.Vector2(player.rect.centerx - coin.rect.centerx, player.rect.centery - coin.rect.centery)
        direction = direction.normalize()  # Normaliser la direction pour déplacer la pièce

        # Déplacer la pièce vers le joueur
        coin.rect.x += direction.x * 10  # Vitesse d'attraction
        coin.rect.y += direction.y * 10  # Vitesse d'attraction

        # Si la pièce atteint le joueur, on la collecte
        if coin.rect.colliderect(player.rect):
            if coin.val == 0:
                self._7amra += 1
                self.score += 20

            elif coin.val == 1:
                self.dirham += 1
                self.score += 200
            coin.kill()  # Supprime la pièce du jeu
            music('./music/coin.wav', 0.3) 
 
    def draw_magnet(self):
        """
        Affiche l'icône de l'aimant et gère la collecte automatique des pièces
        lorsque l'aimant est activé.
        """

        if self.player.sprite.is_magnet_active and not self.isgameover:
            self.collect_nearby_coins()
            icon_position = (10, 10)  # Position de l'icône
            icon_size = (50, 50)  # Taille de l'icône

            # Affichage de l'icône du magnet
            self.window.blit(pygame.transform.scale(pygame.image.load('graphics/coins/magnet.png').convert_alpha(), icon_size), icon_position)

            # Calculer la progression de la barre
            elapsed_time = pygame.time.get_ticks() - self.player.sprite.magnet_timer
            progress = elapsed_time / self.player.sprite.magnet_duration  # Progression (0 à 1)

            # Positionner la barre à côté de l'icône
            bar_x = icon_position[0] + icon_size[0] + 10  # À droite de l'icône avec un décalage de 10 px
            bar_y = icon_position[1] + icon_size[1] // 4  # Aligné verticalement au centre de l'icône

            # Dimensions de la barre
            bar_width = 200
            bar_height = 10

            # Dessiner la barre de progression
            pygame.draw.rect(self.window, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Fond de la barre
            pygame.draw.rect(self.window, (0, 255, 0), (bar_x, bar_y, bar_width * progress, bar_height))  # Barre remplie
     
    def draw_level(self,bg):
        """
        Dessine le niveau en mettant à jour les éléments et en gérant les collisions.
        """
        if self.pause == False:
            self.player.update()
            self.handle_player_particles()
            self.update_bgx(self.deplacement)
            self.bull.update(self)
            self.coins.update(self.deplacement)
            self.obstacles.update(self.deplacement)
            self.ground.update(self.deplacement)
            self.powerups.update(self.deplacement)
            self.buses.update(self.deplacement)
            self.collision_torro()
            self.dust_sprite.update(self.deplacement)


        
        if self.isgameover and self.n>0:
            self.player.sprite.status ="fall"
            self.player.sprite.animation_speed=0.6
            self.player.sprite.animate()
            self.n-=1
            

        
        # Draw infinite scrolling background
        bg_width = bg.get_width()
        # Calculate wrapped background position
        bg_x_wrapped = self.bgx % bg_width
        
        # Draw two copies to ensure continuous background
        self.window.blit(bg, (bg_x_wrapped, 0))
        self.window.blit(bg, (bg_x_wrapped - bg_width, 0))
        
        self.bull.draw(self.window)
        self.obstacles.draw(self.window)
        self.ground.draw(self.window)
        self.powerups.draw(self.window)
        self.buses.draw(self.window)

        if self.deplacement_counter > parametres_inf.tile_size*self.m:
            self.cat_map(parametres_inf.blocks_bank[1::])
            new_length = len(self.map_0[0])
            start_col = new_length - self.m
            # Draw only the newly added block (last m columns of the new map)
            self.draw_map(self.n_lines, new_length, start_col=start_col)
            self.deplacement_counter = 0
        
        self.bordure_x()
        self.collision_ver()
        self.collision_hori()
        self.get_player_on_ground()
        
        
        self.player.draw(self.window)
        self.draw_shield(self.window)
        self.dust_sprite.draw(self.window)


        self.coins.draw(self.window)
        self.hit_coin()
        self.coins.draw(self.window)
        self.draw_magnet()
        self.draw_score(self.window)

