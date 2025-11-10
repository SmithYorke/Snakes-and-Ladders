import pygame
from constants import CHESS_SIZE, CHESS_COUNT
from pathlib import Path
import sys

class ChessManager:
    def __init__(self):
        self.chess_pieces = self._load_chess_pieces()
    
    def _load_chess_pieces(self):
        pieces = []
      
        try:
            current_dir = Path(__file__).parent.resolve()
            project_root = current_dir.parent
            ASSETS_DIR = project_root / "assets"
            
            for i in range(1, CHESS_COUNT + 1):
               
                filename = f"chess{i}.png"
                image_path = ASSETS_DIR / filename
                
                piece_surface = pygame.image.load(str(image_path)).convert_alpha()
                
                piece_surface = pygame.transform.smoothscale(piece_surface, CHESS_SIZE)
                pieces.append(piece_surface)
            
            print("Successfully loaded four chess piece images。")
            return pieces
        
        except (FileNotFoundError, pygame.error, NameError) as e:
        
            colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
            for color in colors:
                piece = pygame.Surface(CHESS_SIZE, pygame.SRCALPHA)
                pygame.draw.circle(piece, color, 
                                 (CHESS_SIZE[0]//2, CHESS_SIZE[1]//2), 
                                 CHESS_SIZE[0]//2 - 5)
                pieces.append(piece)
            return pieces

    def get_chess_piece(self, player_id):
        
        if 0 <= player_id < len(self.chess_pieces):
            return self.chess_pieces[player_id]
        return self.chess_pieces[0]
    
    def draw_chess_piece(self, screen, player_id, position):
        
        chess_piece = self.get_chess_piece(player_id)
        rect = chess_piece.get_rect(center=position)
        screen.blit(chess_piece, rect)