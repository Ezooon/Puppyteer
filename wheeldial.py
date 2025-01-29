import pygame
from util import write
from button import WheelButton


class WheelDial(WheelButton):
    def draw(self):
        self.fill((0, 0, 0, 0))
        text = write(self, str(self.value), text_size=self.size[0] - 10, center=True)
        rect = text.get_rect()

        pygame.draw.rect(self, (200, 200, 200),  (*rect.topleft, rect.width + 3, rect.height + 3))
        if self.hovered_over and not self.pressed:
            pygame.draw.rect(self, (255, 255, 255),  (*rect.topleft, rect.width + 3, rect.height + 3))

        self.blit(text, rect)

        return self, [*self.pos, *self.size]
