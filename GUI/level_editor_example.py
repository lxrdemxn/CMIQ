import pygame as pg
from level_drawer import Draw_Level
import json
import os

# Initialize Pygame
pg.init()

# Create screen
screen = pg.display.set_mode((900, 650))
pg.display.set_caption("Level Editor")

# Load background image
background_path = os.path.join(os.path.dirname(__file__), '..', 'graphics', 'images_start_screen', 'resized_image.png')
try:
    menu_background = pg.image.load(background_path).convert()
    menu_background = pg.transform.scale(menu_background, (900, 650))
except:
    menu_background = None

# Levels file path
LEVELS_FILE = os.path.join(os.path.dirname(__file__), 'custom_levels.json')

# Load existing levels
def load_levels():
    if os.path.exists(LEVELS_FILE):
        try:
            with open(LEVELS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# Save level to JSON file
def save_level(level_map, level_name, creator_name):
    levels = load_levels()
    levels.append({
        'name': level_name,
        'creator': creator_name,
        'map': level_map
    })
    
    with open(LEVELS_FILE, 'w') as f:
        json.dump(levels, f, indent=2)

# Delete level from JSON file
def delete_level(level_index):
    levels = load_levels()
    if 0 <= level_index < len(levels):
        levels.pop(level_index)
        with open(LEVELS_FILE, 'w') as f:
            json.dump(levels, f, indent=2)
        return True
    return False

# Level selection screen
def level_selection_screen():
    levels = load_levels()
    selected_level = None
    running = True
    scroll_offset = 0
    
    while running:
        # Draw background
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill((30, 30, 30))
        
        # Title
        title_font = pg.font.Font(None, 48)
        title = title_font.render("Select a Level", True, (255, 255, 255))
        screen.blit(title, (300, 30))
        
        # Instructions
        inst_font = pg.font.Font(None, 24)
        inst1 = inst_font.render("Click EDIT to edit level", True, (0, 0, 0))
        inst2 = inst_font.render("Click PLAY to play level", True, (0, 0, 0))
        inst3 = inst_font.render("Press N to create new level", True, (0, 0, 0))
        inst4 = inst_font.render("Press ESC to exit", True, (0, 0, 0))
        screen.blit(inst1, (280, 90))
        screen.blit(inst2, (280, 115))
        screen.blit(inst3, (280, 140))
        screen.blit(inst4, (280, 165))
        
        # Display levels
        y_offset = 210
        level_height = 60
        visible_levels = 6
        
        if len(levels) == 0:
            no_levels = pg.font.Font(None, 32).render("No levels created yet. Press N to create one!", True, (0, 0, 0))
            screen.blit(no_levels, (150, 300))
        else:
            for i in range(scroll_offset, min(scroll_offset + visible_levels, len(levels))):
                level = levels[i]
                y = y_offset + (i - scroll_offset) * level_height
                
                # Draw level info background
                info_rect = pg.Rect(100, y, 400, 50)
                pg.draw.rect(screen, (60, 60, 80), info_rect)
                pg.draw.rect(screen, (255, 255, 255), info_rect, 2)
                
                # Draw level name and creator
                name_font = pg.font.Font(None, 24)
                creator_info = f" by {level.get('creator', 'Unknown')}" if level.get('creator') else ""
                name_text = name_font.render(f"{i + 1}. {level['name']}{creator_info}", True, (255, 255, 255))
                screen.blit(name_text, (info_rect.x + 10, info_rect.y + 15))
                
                # Edit button
                edit_button_rect = pg.Rect(510, y, 70, 50)
                mouse_pos = pg.mouse.get_pos()
                if edit_button_rect.collidepoint(mouse_pos):
                    pg.draw.rect(screen, (80, 120, 80), edit_button_rect)
                else:
                    pg.draw.rect(screen, (60, 100, 60), edit_button_rect)
                pg.draw.rect(screen, (255, 255, 255), edit_button_rect, 2)
                edit_text = pg.font.Font(None, 24).render("EDIT", True, (255, 255, 255))
                screen.blit(edit_text, (edit_button_rect.x + 12, edit_button_rect.y + 15))
                
                # Play button
                play_button_rect = pg.Rect(590, y, 70, 50)
                if play_button_rect.collidepoint(mouse_pos):
                    pg.draw.rect(screen, (120, 80, 80), play_button_rect)
                else:
                    pg.draw.rect(screen, (100, 60, 60), play_button_rect)
                pg.draw.rect(screen, (255, 255, 255), play_button_rect, 2)
                play_text = pg.font.Font(None, 24).render("PLAY", True, (255, 255, 255))
                screen.blit(play_text, (play_button_rect.x + 10, play_button_rect.y + 15))
                
                # Delete button
                delete_button_rect = pg.Rect(670, y, 70, 50)
                if delete_button_rect.collidepoint(mouse_pos):
                    pg.draw.rect(screen, (140, 60, 60), delete_button_rect)
                else:
                    pg.draw.rect(screen, (100, 40, 40), delete_button_rect)
                pg.draw.rect(screen, (255, 255, 255), delete_button_rect, 2)
                delete_text = pg.font.Font(None, 20).render("DELETE", True, (255, 255, 255))
                screen.blit(delete_text, (delete_button_rect.x + 8, delete_button_rect.y + 15))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return None
                elif event.key == pg.K_n:
                    return {"action": "NEW"}
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = event.pos
                    for i in range(scroll_offset, min(scroll_offset + visible_levels, len(levels))):
                        y = y_offset + (i - scroll_offset) * level_height
                        edit_button_rect = pg.Rect(510, y, 70, 50)
                        play_button_rect = pg.Rect(590, y, 70, 50)
                        delete_button_rect = pg.Rect(670, y, 70, 50)
                        
                        if edit_button_rect.collidepoint(mouse_pos):
                            return {"action": "EDIT", "level": levels[i]}
                        elif play_button_rect.collidepoint(mouse_pos):
                            return {"action": "PLAY", "level": levels[i]}
                        elif delete_button_rect.collidepoint(mouse_pos):
                            return {"action": "DELETE", "level_index": i}
                
                # Mouse wheel scrolling
                elif event.button == 4:  # Scroll up
                    scroll_offset = max(0, scroll_offset - 1)
                elif event.button == 5:  # Scroll down
                    scroll_offset = min(max(0, len(levels) - visible_levels), scroll_offset + 1)
        
        pg.display.flip()
    
    return None

# Create level drawer with same dimensions as standard levels (8 rows × 200 columns)
# Standard game map is 200 cols wide, 8 rows tall with tile_size=50 for proper win screen centering
level_drawer = Draw_Level(n_tiles=13, map_size=200)

# State management
STATE_SELECTION = "selection"
STATE_EDITING = "editing"
STATE_SAVE = "save"

current_state = STATE_SELECTION
input_level_name = ""
input_creator_name = ""
active_input = "level"  # "level" or "creator"
clock = pg.time.Clock()
running = True

while running:
    if current_state == STATE_SELECTION:
        # Show level selection screen
        result = level_selection_screen()
        if result is None:
            running = False
        elif result.get("action") == "NEW":
            level_drawer = Draw_Level(n_tiles=13, map_size=200)
            current_state = STATE_EDITING
        elif result.get("action") == "EDIT":
            # Load selected level for editing
            level_drawer = Draw_Level(n_tiles=13, map_size=200)
            level_map = result["level"]["map"]
            # Load the map data
            for row_idx, row_data in enumerate(level_map):
                for col_idx, cell in enumerate(row_data):
                    if col_idx < level_drawer.map_size and row_idx < level_drawer.n:
                        level_drawer.map[row_idx][col_idx] = cell
            current_state = STATE_EDITING
        elif result.get("action") == "PLAY":
            # Play the selected level by running play_custom_level.py
            import subprocess
            import sys
            
            level_map = result["level"]["map"]
            level_name = result["level"]["name"]
            
            # Convert map to JSON string for passing as argument
            map_json = json.dumps(level_map)
            
            # Close pygame before launching
            pg.quit()
            
            # Run play_custom_level.py with the map as argument
            script_path = os.path.join(os.path.dirname(__file__), 'play_custom_level.py')
            subprocess.run([sys.executable, script_path, map_json])
            
            # Exit after game closes
            sys.exit()
        elif result.get("action") == "DELETE":
            # Delete the selected level
            level_index = result["level_index"]
            delete_level(level_index)
            # Stay in selection screen to see updated list
            current_state = STATE_SELECTION
    
    elif current_state == STATE_EDITING:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    level_drawer.select_block(event.pos)
            
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    level_drawer.stop_drag(event.pos)
            
            elif event.type == pg.MOUSEMOTION:
                level_drawer.update_drag(event.pos)
            
            elif event.type == pg.KEYDOWN:
                # Scroll with arrow keys
                if event.key == pg.K_RIGHT:
                    level_drawer.scroll_map(1)
                elif event.key == pg.K_LEFT:
                    level_drawer.scroll_map(-1)
                
                # Save map with S key
                elif event.key == pg.K_s:
                    current_state = STATE_SAVE
                    input_level_name = ""
                    input_creator_name = ""
                    active_input = "level"
                
                # Back to selection with ESC
                elif event.key == pg.K_ESCAPE:
                    current_state = STATE_SELECTION
                
                # Clear cell with Delete key
                elif event.key == pg.K_DELETE:
                    mouse_pos = pg.mouse.get_pos()
                    level_drawer.dragged_block = " "
                    level_drawer.dragging = True
                    grid_pos = level_drawer.detect_block(mouse_pos)
                    if grid_pos:
                        level_drawer.place_to_map(grid_pos)
                    level_drawer.dragging = False
                    level_drawer.dragged_block = None
        
        # Draw
        screen.fill((50, 50, 50))
        level_drawer.draw_grid(screen)
        
        # Draw instructions
        font = pg.font.Font(None, 20)
        instructions = [
            "Click blocks on left to select",
            "Click on grid to place",
            "Arrow keys: scroll map",
            "S: save map",
            "ESC: back to menu",
            "Delete: clear cell under mouse"
        ]
        
        y_offset = 520
        for instruction in instructions:
            text = font.render(instruction, True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += 20
        
        pg.display.flip()
        clock.tick(60)
    
    elif current_state == STATE_SAVE:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check which input box was clicked
                    level_box = pg.Rect(200, 280, 500, 50)
                    creator_box = pg.Rect(200, 380, 500, 50)
                    if level_box.collidepoint(event.pos):
                        active_input = "level"
                    elif creator_box.collidepoint(event.pos):
                        active_input = "creator"
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # Save the level
                    if input_level_name.strip() and input_creator_name.strip():
                        saved_map = level_drawer.return_map()
                        save_level(saved_map, input_level_name.strip(), input_creator_name.strip())
                        print(f"Level '{input_level_name.strip()}' by {input_creator_name.strip()} saved!")
                        current_state = STATE_SELECTION
                    elif not input_level_name.strip():
                        active_input = "level"
                    elif not input_creator_name.strip():
                        active_input = "creator"
                
                elif event.key == pg.K_TAB:
                    # Switch between input fields
                    active_input = "creator" if active_input == "level" else "level"
                
                elif event.key == pg.K_ESCAPE:
                    current_state = STATE_EDITING
                
                elif event.key == pg.K_BACKSPACE:
                    if active_input == "level":
                        input_level_name = input_level_name[:-1]
                    else:
                        input_creator_name = input_creator_name[:-1]
                
                else:
                    if event.unicode.isprintable():
                        if active_input == "level" and len(input_level_name) < 30:
                            input_level_name += event.unicode
                        elif active_input == "creator" and len(input_creator_name) < 30:
                            input_creator_name += event.unicode
        
        # Draw
        screen.fill((30, 30, 50))
        
        # Draw save dialog
        title_font = pg.font.Font(None, 48)
        title = title_font.render("Save Level", True, (255, 255, 255))
        screen.blit(title, (300, 150))
        
        prompt_font = pg.font.Font(None, 24)
        
        # Level name input
        prompt1 = prompt_font.render("Level Name:", True, (200, 200, 200))
        screen.blit(prompt1, (200, 250))
        
        level_box = pg.Rect(200, 280, 500, 50)
        box_color = (100, 100, 150) if active_input == "level" else (80, 80, 100)
        pg.draw.rect(screen, box_color, level_box)
        pg.draw.rect(screen, (255, 255, 255), level_box, 2)
        
        input_font = pg.font.Font(None, 28)
        level_surface = input_font.render(input_level_name, True, (255, 255, 255))
        screen.blit(level_surface, (level_box.x + 10, level_box.y + 12))
        
        # Creator name input
        prompt2 = prompt_font.render("Creator Name:", True, (200, 200, 200))
        screen.blit(prompt2, (200, 350))
        
        creator_box = pg.Rect(200, 380, 500, 50)
        box_color = (100, 100, 150) if active_input == "creator" else (80, 80, 100)
        pg.draw.rect(screen, box_color, creator_box)
        pg.draw.rect(screen, (255, 255, 255), creator_box, 2)
        
        creator_surface = input_font.render(input_creator_name, True, (255, 255, 255))
        screen.blit(creator_surface, (creator_box.x + 10, creator_box.y + 12))
        
        # Instructions
        inst_font = pg.font.Font(None, 20)
        inst1 = inst_font.render("Press ENTER to save (both fields required)", True, (150, 150, 150))
        inst2 = inst_font.render("Press TAB to switch fields", True, (150, 150, 150))
        inst3 = inst_font.render("Press ESC to cancel", True, (150, 150, 150))
        screen.blit(inst1, (250, 480))
        screen.blit(inst2, (300, 505))
        screen.blit(inst3, (325, 530))
        
        pg.display.flip()
        clock.tick(60)

pg.quit()
