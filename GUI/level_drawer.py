import pygame as pg
from settings import parametres
import os

class Draw_Level():
    def __init__(self, n_tiles = 6, map_size = 100):
        """initialisation

        Args:
            n_tiles (int, optional): number of blocks simulatnously shown in the screen. Defaults to 6.
            map_size (_type_, optional): number of columns in the map, should be a multiple of 32. Defaults to 32*3.
        """
        self.n_tiles = n_tiles
        self.map_size = map_size
        self.n = len(parametres.level_map[0])       # number of lines
        self.map = [[" " for _ in range(self.map_size)] for i in range(self.n)]
        # Add default ground layer on the last line
        for col in range(self.map_size):
            self.map[self.n - 1][col] = "G"
        # Add default goal (Y) blocks centered in the win_background area (middle of last third)
        goal_column = int(self.map_size - 14)
        for row in range(self.n):
            self.map[row][goal_column] = "Y"
        # Add default player spawn at the same position as in settings.py (row n-2, col 5)
        if self.n >= 2:
            self.map[self.n - 2][5] = "P"
        self.blocks_bank = ["0", "1", "X", "A", "S", "Y"]
        
        # Visual settings
        self.tile_size = 50
        self.grid_offset_x = 100  # Space for block bank on left
        self.grid_offset_y = 50   # Space at top
        
        # Scrolling
        self.scroll_offset = 0  # Starting column index
        
        # Dragging state
        self.dragged_block = None
        self.dragging = False
        self.drag_pos = (0, 0)
        
        # Colors
        self.grid_color = (200, 200, 200, 100)  # Semi-transparent grid lines
        self.bg_color = (50, 50, 50)
        self.block_colors = {
            "0": (255, 215, 0, 80),      # Gold for coin
            "1": (139, 69, 19, 80),      # Brown for platform
            "G": (34, 139, 34, 80),      # Green for ground
            "X": (105, 105, 105, 80),    # Gray for obstacle
            "A": (200, 100, 200, 80),    # Magnet (transparent)
            "S": (100, 150, 255, 80),    # Shield (transparent)
            "P": (0, 150, 255, 80),      # Player spawn (blue)
            "Y": (255, 255, 0, 80),      # Goal (yellow)
            " ": None                     # Empty - no background
        }
        
        # Load block icons and background
        self.block_images = {}
        self.background = None
        self._load_images()

    def _load_images(self):
        """Load all block images and background from the graphics directory"""
        graphics_path = os.path.join(os.path.dirname(__file__), '..', 'graphics')
        
        # Load background image
        bg_path = os.path.join(graphics_path, 'backgrounds', 'background5.png')
        if os.path.exists(bg_path):
            try:
                bg_image = pg.image.load(bg_path).convert()
                # Scale background to fit the grid height exactly
                grid_height = self.n * self.tile_size
                aspect_ratio = bg_image.get_width() / bg_image.get_height()
                new_width = int(grid_height * aspect_ratio)
                scaled_bg = pg.transform.scale(bg_image, (new_width, grid_height))
                
                # Load win background
                win_bg_path = os.path.join(graphics_path, 'game_won_icons', 'win_background.png')
                win_bg = pg.image.load(win_bg_path).convert()
                win_bg = pg.transform.scale(win_bg, (new_width, grid_height))
                win_bg_width = win_bg.get_width()
                
                # Calculate total map width
                map_width = self.map_size * self.tile_size
                
                # Calculate how much space to fill with regular background before win background
                # Reserve the last portion for win background
                regular_bg_width = map_width - win_bg_width
                num_tiles = (regular_bg_width // new_width) + 1
                
                # Create tiled background with win background reserved at the end
                self.background = pg.Surface((map_width, grid_height))
                
                # Fill with regular background tiles
                for i in range(num_tiles):
                    self.background.blit(scaled_bg, (i * new_width, 0))
                
                # Place win background at the end (last portion of map)
                self.background.blit(win_bg, (map_width - win_bg_width, 0))
            except Exception as e:
                print(f"Error loading background: {e}")
                self.background = None
        
        # Define image paths for each block type
        image_paths = {
            "0": os.path.join(graphics_path, 'coins', '1dh.png'),
            "1": os.path.join(graphics_path, 'coins', '10dh.png'),
            "X": os.path.join(graphics_path, 'Obstacles', 'img3.png'),
            "G": None,  # Ground will use a solid color
            "A": os.path.join(graphics_path, 'coins', 'magnet.png'),
            "S": os.path.join(graphics_path, 'coins', 'shield.png'),
            "P": None,  # Player spawn will show as "P" text
            "Y": None   # Goal will show as "Y" text
        }
        
        # Load and scale images
        for block_type, path in image_paths.items():
            if path and os.path.exists(path):
                try:
                    image = pg.image.load(path).convert_alpha()
                    # Scale to fit tile size with some padding
                    scaled_image = pg.transform.scale(image, (self.tile_size - 4, self.tile_size - 4))
                    self.block_images[block_type] = scaled_image
                except:
                    # If image fails to load, we'll fall back to text
                    self.block_images[block_type] = None
            else:
                self.block_images[block_type] = None

    def draw_grid(self, screen):
        """draws the shown part of the grid on the screen given the window of the previewed map (n_tiles) and map_size
        
        Args:
            screen: pygame surface to draw on
        """
        # Draw scrolling background behind the grid
        if self.background:
            # Calculate background offset based on scroll position
            bg_scroll_offset = self.scroll_offset * self.tile_size
            
            # Draw background tiles to cover the grid width
            grid_width = self.n_tiles * self.tile_size
            grid_height = self.n * self.tile_size
            
            # Create a surface for the background that matches grid dimensions
            bg_surface = pg.Surface((grid_width, grid_height))
            
            # Blit the appropriate portion of the tiled background
            bg_surface.blit(self.background, (-bg_scroll_offset, 0))
            
            # Blit the background surface clipped to grid area
            screen.blit(bg_surface, (self.grid_offset_x, self.grid_offset_y))
        
        # Draw grid cells
        for row in range(self.n):
            for col in range(self.n_tiles):
                actual_col = self.scroll_offset + col
                if actual_col >= self.map_size:
                    continue
                    
                x = self.grid_offset_x + col * self.tile_size
                y = self.grid_offset_y + row * self.tile_size
                
                # Draw semi-transparent cell background only for non-empty cells
                block_type = self.map[row][actual_col]
                if block_type != " ":
                    color = self.block_colors.get(block_type)
                    if color:
                        # Create a transparent surface
                        surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
                        surf.fill(color)
                        screen.blit(surf, (x, y))
                
                # Draw grid lines
                pg.draw.rect(screen, self.grid_color, (x, y, self.tile_size, self.tile_size), 1)
                
                # Draw block icon or letter
                if block_type != " ":
                    if block_type in self.block_images and self.block_images[block_type]:
                        # Draw image centered in the cell
                        img_rect = self.block_images[block_type].get_rect(
                            center=(x + self.tile_size // 2, y + self.tile_size // 2)
                        )
                        screen.blit(self.block_images[block_type], img_rect)
                    else:
                        # Fallback to text if image not available
                        font = pg.font.Font(None, 36)
                        text = font.render(block_type, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                        screen.blit(text, text_rect)
        
        # Draw block bank on the left
        for i, block in enumerate(self.blocks_bank):
            x = 10
            y = self.grid_offset_y + i * (self.tile_size + 10)
            
            color = self.block_colors.get(block, (100, 100, 100, 150))
            if color:
                surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
                surf.fill(color)
                screen.blit(surf, (x, y))
            
            pg.draw.rect(screen, (255, 255, 255), (x, y, self.tile_size, self.tile_size), 2)
            
            # Draw block icon or letter
            if block in self.block_images and self.block_images[block]:
                img_rect = self.block_images[block].get_rect(
                    center=(x + self.tile_size // 2, y + self.tile_size // 2)
                )
                screen.blit(self.block_images[block], img_rect)
            else:
                font = pg.font.Font(None, 36)
                text = font.render(block, True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                screen.blit(text, text_rect)
        
        # Draw dragged block if dragging
        if self.dragging and self.dragged_block:
            color = self.block_colors.get(self.dragged_block, (100, 100, 100, 150))
            if color:
                surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
                surf.fill(color)
                screen.blit(surf, (self.drag_pos[0] - self.tile_size // 2, 
                                  self.drag_pos[1] - self.tile_size // 2))
            
            pg.draw.rect(screen, (255, 255, 255), (self.drag_pos[0] - self.tile_size // 2, 
                                                    self.drag_pos[1] - self.tile_size // 2, 
                                                    self.tile_size, self.tile_size), 2)
            
            # Draw block icon or letter
            if self.dragged_block in self.block_images and self.block_images[self.dragged_block]:
                img_rect = self.block_images[self.dragged_block].get_rect(center=self.drag_pos)
                screen.blit(self.block_images[self.dragged_block], img_rect)
            else:
                font = pg.font.Font(None, 36)
                text = font.render(self.dragged_block, True, (255, 255, 255))
                text_rect = text.get_rect(center=self.drag_pos)
                screen.blit(text, text_rect)
        
        # Draw scroll info
        font = pg.font.Font(None, 24)
        scroll_text = f"Columns {self.scroll_offset} - {min(self.scroll_offset + self.n_tiles - 1, self.map_size - 1)}"
        text = font.render(scroll_text, True, (255, 255, 255))
        screen.blit(text, (self.grid_offset_x, 10))

    def select_block(self, mouse_pos):
        """selects a block by clicking on it using the mouse and sets it to be dragged to the map by the mouse
            and once dragged it's locked to the mouse pointer and only dropped if clicked on on top of the choosen grid block
            
        Args:
            mouse_pos: tuple (x, y) of mouse position
            
        Returns:
            bool: True if a block was selected, False otherwise
        """
        x, y = mouse_pos
        
        # Check if clicking on block bank
        for i, block in enumerate(self.blocks_bank):
            block_x = 10
            block_y = self.grid_offset_y + i * (self.tile_size + 10)
            
            if (block_x <= x <= block_x + self.tile_size and 
                block_y <= y <= block_y + self.tile_size):
                self.dragged_block = block
                self.dragging = True
                self.drag_pos = mouse_pos
                return True
        
        return False

    def detect_block(self, mouse_pos):
        """detects if the dragged element is in the range of a certain grid square, if clicked the mouse while
        on top of this square, it returns the (i, j) coordinates of the choosen block and calls the place_to_map function
        
        Args:
            mouse_pos: tuple (x, y) of mouse position
            
        Returns:
            tuple or None: (row, col) if valid grid position, None otherwise
        """
        if not self.dragging:
            return None
            
        x, y = mouse_pos
        
        # Check if within grid bounds
        if (x < self.grid_offset_x or 
            y < self.grid_offset_y or 
            y >= self.grid_offset_y + self.n * self.tile_size):
            return None
        
        # Calculate grid position
        grid_col = (x - self.grid_offset_x) // self.tile_size
        grid_row = (y - self.grid_offset_y) // self.tile_size
        
        # Check if valid grid position
        if grid_col < 0 or grid_col >= self.n_tiles or grid_row < 0 or grid_row >= self.n:
            return None
        
        # Convert to actual map column
        actual_col = self.scroll_offset + grid_col
        if actual_col >= self.map_size:
            return None
        
        return (grid_row, actual_col)

    def place_to_map(self, pos:tuple[int,int]):
        """once a block is placed on the grid block, translate it into its relative case in the map matrix
        like the one described in the settings.py file

        Args:
            pos (int, int): indexes of the grid on the map (row, column)
        """
        if self.dragged_block and pos:
            row, col = pos
            if 0 <= row < self.n and 0 <= col < self.map_size:
                self.map[row][col] = self.dragged_block

    def scroll_map(self, direction:int):
        """scrolls the map in the given direction

        Args:
            direction (int): 1 (forward), -1 (backwards)
        """
        new_offset = self.scroll_offset + direction
        
        # Ensure we don't scroll out of bounds
        if new_offset >= 0 and new_offset + self.n_tiles <= self.map_size:
            self.scroll_offset = new_offset

    def update_drag(self, mouse_pos):
        """Update the position of the dragged block
        
        Args:
            mouse_pos: tuple (x, y) of current mouse position
        """
        if self.dragging:
            self.drag_pos = mouse_pos

    def stop_drag(self, mouse_pos):
        """Stop dragging and place block if over valid grid position
        
        Args:
            mouse_pos: tuple (x, y) of mouse position when released
        """
        if self.dragging:
            grid_pos = self.detect_block(mouse_pos)
            if grid_pos:
                self.place_to_map(grid_pos)
            
            self.dragging = False
            self.dragged_block = None

    def return_map(self):
        """returns the map matrix if clicked on the save button
        
        Returns:
            list: The map as a list of strings (one string per row)
        """
        # Convert the 2D list to list of strings format like in settings.py
        return [''.join(row) for row in self.map]