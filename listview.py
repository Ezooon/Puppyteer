import pygame
from util import MySurface

class ListView(MySurface):
    def __init__(self, pos, size=(100, 100), spacing=1, padding=(1, 5)):
        super().__init__(pos, size)
        self.spacing = spacing
        self.padding = padding
        self.background = (10, 100, 255)
        self.y_offset = 0
        self.height = 0

    def draw(self):
        self.fill(self.background)
        y = self.y_offset
        self.height = 0
        for widget in self.uix:
            widget.pos = [self.padding[0], y]
            self.blit(*widget.draw())
            y = y + self.spacing + widget.size[1]
            self.height += self.spacing + widget.size[1]

        return self, [*self.pos, *self.size]

    def loop(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if self.collidepoint(*pygame.mouse.get_pos()):
                    if event.y == 1:
                        self.y_offset += 40
                    elif event.y == -1:
                        self.y_offset -= 40
                    if self.y_offset > 0:
                        self.y_offset = 0
                    elif self.height < abs(self.y_offset) + self.size[1]:
                        self.y_offset = self.size[1] - self.height

                    events.remove(event)
                break
        super().loop(events)
