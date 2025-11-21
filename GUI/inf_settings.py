class settings_infinite():
    def __init__(self):
        self.GRAVITY=1
        self.vitesse_joueur = 6
        self.nom_jeu = "CATCH ME ILA QEDDITI"
        self.jump_speed = -20
        self.fps = 60
        self.tile_size = 50
        self.coin_size = 40
        self.screen_height=500
        self.screen_width = 800
        self.blocks_bank = [
                # Block 0 - Player spawn with shield
                ["                                   S",
                "                           111111   ",
                "                           XXXXXX   ",
                "            A        XX    XXXXXX   ",
                "           XXX       XX 0           ",
                "        XX   XXX     XXXX           ",
                "     P  XX    XX     XXXX    1   0  ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 1 - Staircase with coins
                ["                                     ",
                "                               0   S ",
                "                            1  XX    ",
                "                      0   XXX        ",
                "                 1  XXX              ",
                "            0  XXX                   ",
                "       1  XXX                        ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 2 - Moving platforms challenge
                ["                    A                ",
                "                                   0 ",
                "             0                       ",
                "                                     ",
                "                                     ",
                "    1                          1     ",
                "  XXX   M         M         MXXX     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 3 - Tunnel with power-ups
                ["XXXXXXXXXXXXX                        ",
                "                          S          ",
                "                 0   0   XXX         ",
                "               XXXX XXXX             ",
                "                                     ",
                "                 A      1      1     ",
                "           XXXXXXXXXXXXXXX   XXX     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 4 - High jumps with magnet
                ["                                     ",
                "                                   A ",
                "                              XXXX   ",
                "              1                      ",
                "           XXXX                      ",
                "      0                        0     ",
                "    XXX              M       XXX     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 5 - Mixed obstacles
                ["               0     S               ",
                "            XXXX   XXX     11        ",
                "                            XX       ",
                "                                     ",
                "                    B                ",
                "   0       1                  0      ",
                " XXX    MXXX                XXX      ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 6 - Vertical challenge
                ["                                     ",
                "                              1    S ",
                "                           XXXX      ",
                "                 0                   ",
                "              XXXX                   ",
                "         A                           ",
                "      XXXX                     M     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 7 - Gap jumps with rewards
                ["          S                          ",
                "       XXXX                    1     ",
                "                                XX   ",
                "   0                                 ",
                "  XX          0         A            ",
                "           XXXX      XXXX            ",
                "                                     ",
                "GGGGGGG         GGGGGG        GGGGGGG"],
                
                # Block 8 - Coin collection maze
                ["                                     ",
                "          0   0   0   0   0          ",
                "                              XXXXX  ",
                "          1   S   1   A   1   X      ",
                "  XXXXX                       X      ",
                "      XXXXXXXXXXXXXXXXXXXXXXXXXM     ",
                "                                     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 9 - Double moving platforms
                ["                                     ",
                "                              S      ",
                "        M                            ",
                "                   M                 ",
                "   0                           0     ",
                "                                     ",
                "      1                    1         ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 10 - Zigzag pattern
                ["                                 1 S ",
                "                              XXX    ",
                "                   0   0             ",
                "                XXXX                 ",
                "         A                           ",
                "      XXXX                           ",
                " 0                                   ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 11 - Bus obstacle course
                ["                                     ",
                "         1         1        1        ",
                "      XXXX      XXXX     XXXX        ",
                "                                     ",
                "              B           S          ",
                "   0                           A     ",
                "  XX                         XXX     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 12 - Low ceiling challenge
                ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
                "X                                  X ",
                "X  0    1    0    S    0    1    0 X ",
                "XXXX                             XXX ",
                "       M          M          M       ",
                "                                     ",
                "                                     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 13 - Ascending platforms
                ["                                     ",
                "                                    A",
                "                          1     XXXX ",
                "                       XXXX          ",
                "                0                    ",
                "             XXXX                    ",
                "       S                             ",
                "GGGGGXXXXGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 14 - Multi-level maze
                ["                     S               ",
                "                    XXX              ",
                "   0   X                             ",
                "  XX   XXXXXXXXX  0  XXXXXX          ",
                "                 XX        X   A     ",
                " M                         X  XXX    ",
                "                           X         ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGXGGGGGGGGG"],
                
                # Block 15 - Speed run section
                ["                                     ",
                "  0   0   0   0   0   0   0   0   S  ",
                "                                     ",
                "                                     ",
                "                                     ",
                "    M         M         M            ",
                "                                     ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"],
                
                # Block 16 - Wall climb with rewards
                ["                                     ",
                "                              1    1 ",
                "              S         X     XX  XXX",
                "           XXXX         X            ",
                "      A                 X   0        ",
                "   XXXX                 XXXXX        ",
                "                              M      ",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"]]
        
parametres_inf = settings_infinite()

