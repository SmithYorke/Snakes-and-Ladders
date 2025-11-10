# File: board.py
import pygame
from constants import BOARD_POS, BOARD_SIZE, TILE_COUNT
from pathlib import Path
from constants import BOARD_SIZE, BOARD_POS # Duplicated import, but kept as in original


BASE_DIR = Path(__file__).resolve().parent.parent



# --- Snakes and Ladders Mapping (start -> end) ---
# Note: These values define the game's movement rules.
SNAKES = {34:1,25:5,87:57,47:19,91:61,99:69}
LADDERS ={3:57,6:27,20:70,63:95,68:98,36:95}






# --- Core Class ---
class Board:
    def __init__(self):
        
        # Using an absolute path to load the image for stability
        # IMPORTANT: Adjust this path to your actual file location!
        IMAGE_PATH = BASE_DIR / "assets" / "borad.jpg"
        
        try:
            # Load the image using the Path object converted to string
            self.image = pygame.image.load(str(IMAGE_PATH)).convert()
            print(f"Successfully loaded board image: {IMAGE_PATH}")


        except pygame.error as e:
            # Handle Pygame errors (e.g., file not found or corrupted)
            print(f"Pygame load error: {e}")
            print(" Warning: Using temporary background. Check your image path and file.")
            
            # Create a temporary fallback board (Orange/Brown)
            self.image = pygame.Surface(BOARD_SIZE)
            self.image.fill((200, 150, 100))
        


        # Initialize board dimensions and scaling
        self.image = pygame.transform.smoothscale(self.image, BOARD_SIZE)
        self.x, self.y = BOARD_POS
        self.w, self.h = BOARD_SIZE



        # Pre-calculate tile dimensions for quick access
        self.tile_w = self.w / TILE_COUNT
        self.tile_h = self.h / TILE_COUNT


    def draw(self, screen):
        """Draw the scaled board background image onto the screen."""
        screen.blit(self.image, (self.x, self.y))


    def get_tile_center(self, position):
        """
        Calculates the center pixel coordinates (x, y) for a given tile number (1-100).
        --- Logic: All rows proceed Left-to-Right (NO Boustrophedon/Snakes and Ladders zigzag) ---
        """
        if position < 1 or position > 100:
            # Return a safe fallback position if input is out of bounds
            return BOARD_POS 

        # Calculate tile dimensions (using constants for 10x10 grid)
        tile_width = BOARD_SIZE[0] / 10
        tile_height = BOARD_SIZE[1] / 10

        # 1. Determine the row index (row_index): 0 is the bottom row (1-10), 9 is the top row (91-100)
        row_index = (position - 1) // 10 
        col_index = (position - 1) % 10
        

        # 3. Calculate the screen Y index (screen_y_index)
        screen_y_index = 9 - row_index 
        

        # 4. Calculate the pixel center coordinates


        # Center X = Board Start X + (Column Index * Tile Width) + (Half Tile Width)
        center_x = BOARD_POS[0] + (col_index * tile_width) + (tile_width / 2)


        # Center Y = Board Start Y + (Screen Y Index * Tile Height) + (Half Tile Height)
        center_y = BOARD_POS[1] + (screen_y_index * tile_height) + (tile_height / 2)

        return (center_x, center_y)






    def apply_snakes_ladders(self, pos):
        """Returns the final position and the jump type after hitting a snake or ladder."""
        if pos in LADDERS:
            return LADDERS[pos], 'ladder'
        if pos in SNAKES:
            return SNAKES[pos], 'snake'
        # If no rule applies, the position stays the same, and the type is None
        return pos, None