from os.path import join

import pygame


class MySurface(pygame.Surface):
    def __init__(self, pos=(0, 0), size=(0, 0)):
        super().__init__(size, pygame.SRCALPHA|pygame.RESIZABLE, 32)
        self.parent = None
        self.pos = pos
        self.size = size
        self._uix = []
        self.background = (255, 255, 255)

    def add_widget(self, widget, i=None):
        if issubclass(type(widget), MySurface):
            widget.parent = self
        if i is not None:
            self._uix.insert(i, widget)
            return
        self._uix.append(widget)

    def remove_widget(self, widget):
        if widget in self._uix:
            self._uix.remove(widget)
            widget.parent = None

    @property
    def uix(self):
        return self._uix

    @uix.setter
    def uix(self, uix):
        self._uix = []
        for x in uix:
            self.add_widget(x)

    @property
    def abs_pos(self):
        if self.parent:
            x, y = self.pos
            px, py = self.parent.abs_pos
            return px + x, py + y

        return self.pos

    def local_pos(self, x, y):
        if self.parent:
            px, py = self.parent.abs_pos
            return x - px, y - py

        return self.pos

    @property
    def center(self):
        x, y = self.pos
        w, h = self.size
        return x + (w / 2), y + (h / 2)

    @center.setter
    def center(self, pos):
        x, y = pos
        w, h = self.size
        self.pos = x - (w / 2), y - (h / 2)

    def collidepoint(self, x, y):
        x1, y1 = self.abs_pos
        w, h = self.size
        x2 = x1 + w
        y2 = y1 + h
        return x1 <= x <= x2 and y1 <= y <= y2

    def draw(self):
        for widget in self.uix:
            self.blit(*widget.draw())

        return self, [*self.pos, *self.size]

    def loop(self, events):
        for widget in self.uix:
            widget.loop(events)

    def __repr__(self):
        return str(self.__class__.__name__)

class Movable:

    moving = None
    # the moving surface object for now

    dx, dy = (0, 0)
    # the distance of where them mouse down event was from the x, y of the moving surface

    def drag_loop(self, events):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(*pygame.mouse.get_pos())
                    and Movable.moving is None):
                Movable.moving = self
                mx, my = pygame.mouse.get_pos()
                x, y = self.pos
                Movable.dx, Movable.dy = mx - x, my - y
                break
            elif event.type == pygame.MOUSEBUTTONUP and Movable.moving is not None:
                # print(Movable.moving, *Movable.moving.pos)
                Movable.moving = None
                Movable.dx = 0
                Movable.dy = 0
                break

            if event.type == pygame.MOUSEMOTION and self.moving is not None:
                mx, my = event.pos
                Movable.moving.pos = mx - Movable.dx, my - Movable.dy
                break


def write(screen=None, text="", text_size=20, pos=(0, 0), color=(0, 0, 0), center=False, d_rect=False,
          font_name=None):
    wfont = pygame.font.Font(font_name, text_size)
    text_image = wfont.render(text, True, color)
    text_rect = text_image.get_rect()

    if center:
        text_rect.center = pos
        if screen:
            screen.blit(text_image, text_rect)
        if d_rect:
            pygame.draw.rect(screen, color, text_rect, 1)
        return text_image

    if screen:
        screen.blit(text_image, pos)
    return text_image


