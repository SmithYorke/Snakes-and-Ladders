import pygame
import sys
# Absolute import (Ensure these files exist in your project structure)
from board import Board
from player import Player
from dice import Dice
from chess import ChessManager
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, INFO_PANEL_WIDTH


class Button:
    # Simple clickable button class
    def __init__(self, rect, text, font, color=(100, 200, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color

    def draw(self, screen):
        # Draws a rounded rectangle and centers the text inside
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, BLACK)
        txt_r = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_r)

    def is_clicked(self, pos):
        # Checks if a mouse click was inside this button
        return self.rect.collidepoint(pos)


INFO_PANEL_WIDTH = 120 
NEW_BOARD_X = 120 


class Game:
    def __init__(self):
        pygame.init()
        
        # Setting up fonts
        self.font = pygame.font.Font(None, 24) 
        self.large_font = pygame.font.Font(None, 48)
        
        # Main game window setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snakes and Ladders")
        
        # Game state variables
        self.current_player = 0
        self.game_state = 'running'  # Can be 'running' or 'end'
        self.winner = None
        
        # Create 4 players named Player 1–4
        self.players = [Player(i, f"Player {i+1}") for i in range(4)]
   
        # Create game components
        self.board = Board()
        self.dice = Dice()
        self.chess_manager = ChessManager()
        
        # Display message on top of the board
        self.message = "Click the dice to start the round!" 

        # Buttons for when the game ends
        self.restart_button = Button((SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50, 100, 50), 
                                     "PLAY AGAIN", self.font, (0, 255, 0))
        self.quit_button = Button((SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50, 100, 50), 
                                  "EXIT", self.font, (255, 0, 0))

    def reset_game(self):
        # Fully reset all players and game state
        self.players = [Player(i, f"Player {i+1}") for i in range(4)]
        self.current_player = 0
        self.game_state = 'running'
        self.winner = None
        self.message = "Game reset. Click the dice!"
        self.dice.value = 1

    def draw_text(self, screen, text, color, pos, font):
        # Helper to draw text on the screen
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, pos)


    def draw_info_panel(self, screen):
        # Draws the left info panel showing player info
        panel_rect = pygame.Rect(0, 0, INFO_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, BLACK, panel_rect)
        


        for i, player in enumerate(self.players):
            y_start = 50 + i * 120
            icon_pos = (INFO_PANEL_WIDTH // 2, y_start) 
            # Draws the player's little chess icon



            self.chess_manager.draw_chess_piece(screen, i, icon_pos)
            


            # Highlight current player
            is_current = (i == self.current_player)
            name_color = (255, 255, 0) if is_current else WHITE
            


            # Player name and position
            self.draw_text(screen, player.name[:8], name_color, (5, y_start + 25), self.font)
            self.draw_text(screen, f"Pos: {player.position}", WHITE, (5, y_start + 45), self.font)
            

            # Green border box around current player's info
            if is_current:
                 pygame.draw.rect(screen, (0, 255, 0), (0, y_start - 30, INFO_PANEL_WIDTH, 100), 2)





    def draw(self):
        # Handles all drawing for both running and end states
        if self.game_state == 'running':
            self.screen.fill(WHITE)
            

            # Draw game board and info
            self.draw_info_panel(self.screen)
            self.board.draw(self.screen) 
            
            # Draw all player pieces on their current tiles
            for i, player in enumerate(self.players):
                pos = self.board.get_tile_center(player.position)
                self.chess_manager.draw_chess_piece(self.screen, i, pos)
            

            # Display message + dice
            self.draw_text(self.screen, self.message, BLACK, (NEW_BOARD_X, 10), self.font) 
            self.dice.draw(self.screen)

        elif self.game_state == 'end':

            # Show winner screen
            self.screen.fill(BLACK)


            win_msg = f" {self.winner.name} WINS! "
            
            self.draw_text(self.screen, win_msg, (255, 255, 0), 
                           (SCREEN_WIDTH // 2 - len(win_msg) * 10, SCREEN_HEIGHT // 2 - 50), 
                           self.large_font)
            

            # Show play again + exit buttons
            self.restart_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            

        # Update the display each frame
        pygame.display.flip() 
    

    def handle_move(self, steps):


        # Moves the current player according to dice roll
        player = self.players[self.current_player]
        old_pos = player.position
        

        # Player handles movement logic (and detects ladder/snake/win)
        move_type, is_winner = player.move(steps, self.board)
        new_pos = player.position
        


        # Build an on-screen message depending on what happened
        if is_winner:
             self.message = f" {player.name} WINS!"
             self.winner = player
             self.game_state = 'end' 
        elif old_pos + steps > 100:
             self.message = f"{player.name} overshoots. Stays at {old_pos}."
        elif move_type == 'ladder':
             self.message = f" {player.name} climbs a ladder to {new_pos}!"
        elif move_type == 'snake':
             self.message = f" {player.name} slides down a snake to {new_pos}!"
        else:
             self.message = f"{player.name} rolled {steps}, moves to {new_pos}."


        # Only switch turns if game hasn’t ended
        if self.game_state == 'running':
             self.current_player = (self.current_player + 1) % len(self.players)
    


    def run(self):
        # Main game loop – keeps running until quit
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == 'running':
                        # Player clicks on dice to roll
                        if self.dice.rect.collidepoint(event.pos):
                            steps = self.dice.roll()
                            self.handle_move(steps)
                    
                    elif self.game_state == 'end':
                        # Handle clicks on restart or quit buttons
                        if self.restart_button.is_clicked(event.pos):
                            self.reset_game()
                        elif self.quit_button.is_clicked(event.pos):
                            running = False
            


            # Draw current frame
            self.draw()
            pygame.time.Clock().tick(60)
        

        # Quit everything cleanly
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
