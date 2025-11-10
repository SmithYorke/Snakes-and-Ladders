import pygame  # Imported Pygame library
import sys

# Import all core modules in the project
from board import Board
from player import Player
from dice import Dice
from chess import ChessManager
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, INFO_PANEL_WIDTH


class Button:
    # Helper class for drawing clickable buttons
    def __init__(self, rect, text, font, color=(100, 200, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, BLACK)
        txt_r = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_r)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Assumed starting X coordinate for the board after the info panel
NEW_BOARD_X = INFO_PANEL_WIDTH 


class Game:
    def __init__(self):
        # Set all basic components and initial states

        pygame.init() 
        # Initialize Pygame system

        self.font = pygame.font.Font(None, 24) 
        self.large_font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 96) # Font for the menu title
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        # Create the main display window
        
        pygame.display.set_caption("Snakes and Ladders") 
        
        self.game_state = 'menu'  # Initial game state
        self.winner = None
        self.message = "Click START GAME to begin!" # Game status message
        
        self.board = Board()     
        self.dice = Dice()
        self.chess_manager = ChessManager()
        # Instantiate core game components

        self.players = [
            Player(0, "Player 1"),
            Player(1, "Player 2"), 
            Player(2, "Player 3"),
            Player(3, "Player 4")
        ]
        self.current_player = 0 # Index of the current player (0 to 3)

        # Button definitions for Menu and End screen
        button_w, button_h = 200, 60
        button_y_start = SCREEN_HEIGHT // 2
        
        self.start_game_button = Button((SCREEN_WIDTH // 2 - button_w // 2, button_y_start, button_w, button_h), 
                                     "START GAME", self.large_font, (0, 200, 0))
        
        self.quit_menu_button = Button((SCREEN_WIDTH // 2 - button_w // 2, button_y_start + 80, button_w, button_h), 
                                    "QUIT GAME", self.large_font, (200, 0, 0))
        
        self.restart_button = Button((SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50, 100, 50), 
                                     "PLAY AGAIN", self.font, (0, 255, 0))
        self.quit_button = Button((SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50, 100, 50), 
                                  "EXIT", self.font, (255, 0, 0))
    

    # Utility method to draw text
    def draw_text(self, screen, text, color, pos, font):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, pos)

    # Method to draw the left side info panel
    def draw_info_panel(self, screen):
        panel_rect = pygame.Rect(0, 0, INFO_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, BLACK, panel_rect)
        
        
        for i, player in enumerate(self.players):
            y_start = 50 + i * 120
            icon_pos = (INFO_PANEL_WIDTH // 2, y_start) 
            self.chess_manager.draw_chess_piece(screen, i, icon_pos)
            
            is_current = (i == self.current_player)
            name_color = (255, 255, 0) if is_current else WHITE
            
            self.draw_text(screen, player.name[:8], name_color, (5, y_start + 25), self.font)
            self.draw_text(screen, f"Pos: {player.position}", WHITE, (5, y_start + 45), self.font)
            
            if is_current:
                 # Highlight the current player
                 pygame.draw.rect(screen, (0, 255, 0), (0, y_start - 30, INFO_PANEL_WIDTH, 100), 2)
    
    # Method to reset the game state
    def reset_game(self):
        self.players = [Player(i, f"Player {i+1}") for i in range(4)]
        self.current_player = 0
        self.game_state = 'running'
        self.winner = None
        self.message = "Game reset. Click the dice!"
        self.dice.value = 1

    # Method to handle player movement and update game messages
    def handle_move(self, steps):
        
        player = self.players[self.current_player]
        old_pos = player.position
        
        # player.move returns (move_type, is_winner)
        move_type, is_winner = player.move(steps, self.board) 
        new_pos = player.position
        
        # Message update logic
        if is_winner:
             self.message = f" {player.name} WINS!"
             self.winner = player
             self.game_state = 'end' # Change state to end
        elif old_pos + steps > 100:
             self.message = f"{player.name} overshoots. Stays at {old_pos}."
        elif move_type == 'ladder':
             self.message = f"{player.name} climbs a ladder to {new_pos}!"
        elif move_type == 'snake':
             self.message = f" {player.name} slides down a snake to {new_pos}!"
        else:
             self.message = f"{player.name} rolled {steps}, moves to {new_pos}."
        
        
    # Main drawing method, handling all three game states
    def draw(self):
        
        if self.game_state == 'menu':
            # --- Menu screen drawing ---
            self.screen.fill(BLACK)

            # Draw game title
            title_text = "SNAKES AND LADDERS"
            title_surf = self.title_font.render(title_text, True, (255, 255, 0)) 
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_surf, title_rect)
            
            # Draw menu buttons
            self.start_game_button.draw(self.screen)
            self.quit_menu_button.draw(self.screen)
        

        elif self.game_state == 'running':

            # --- Game active screen drawing ---
            self.screen.fill(WHITE) 

            # Draw info panel, board, dice, and status message
            self.draw_info_panel(self.screen) 
            self.board.draw(self.screen)
            self.dice.draw(self.screen)
            self.draw_text(self.screen, self.message, BLACK, (NEW_BOARD_X, 10), self.font)
            
            
            for i, player in enumerate(self.players):
            # Iterate through all players
            
                pos = self.board.get_tile_center(player.position)
            # Convert player's logical position (1-100) to pixel coordinates

                self.chess_manager.draw_chess_piece(self.screen, i, pos)

        elif self.game_state == 'end':
            # --- Game over screen drawing ---
            self.screen.fill(BLACK)
            win_msg = f"  {self.winner.name} win WIN wiiiiinn!"
            self.draw_text(self.screen, win_msg, (255, 255, 0), (SCREEN_WIDTH // 2 - len(win_msg) * 10, SCREEN_HEIGHT // 2 - 50), self.large_font)
            
            # Draw end screen buttons
            self.restart_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            
        
        pygame.display.flip()
        # Push the rendered frame to the physical display
    

    # Main game loop
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if self.game_state == 'menu': # Menu state input handler
                        if self.start_game_button.is_clicked(event.pos):
                            self.game_state = 'running'
                            self.message = "Click the dice to start the round!"
                        elif self.quit_menu_button.is_clicked(event.pos):
                            running = False
                    
                    elif self.game_state == 'running': # Running state input handler
                        if self.dice.rect.collidepoint(event.pos):
                            
                            steps = self.dice.roll()
                            self.handle_move(steps) # Execute movement and update messages
                            
                            # Switch to the next player only if the game is still running
                            if self.game_state == 'running':
                                self.current_player = (self.current_player + 1) % len(self.players)
                            
                            
                    elif self.game_state == 'end': # End state input handler
                        if self.restart_button.is_clicked(event.pos):
                            self.reset_game()
                        elif self.quit_button.is_clicked(event.pos):
                            running = False

            
            self.draw()
            pygame.time.Clock().tick(60) # Set max frame rate to 60 FPS
        
        pygame.quit()
        sys.exit()

# Script execution entry point
if __name__ == "__main__":
    game = Game()
    game.run()