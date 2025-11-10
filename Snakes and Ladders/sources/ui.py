import pygame

class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = (100, 200, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, (0,0,0))
        txt_r = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_r)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
