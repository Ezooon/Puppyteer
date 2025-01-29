import pygame
from util import MySurface, Movable


class Button(MySurface, Movable):
    def __init__(self, pos=(0, 0), size=25,
                 icon="assets/eye.png", pressed_icon="", toggle=False):
        super(Button, self).__init__(pos, [size, size])

        self.color = (153, 117, 56)
        self.pressed_color = (133, 97, 36)
        self.hovered_over_color = (163, 127, 66)

        self.toggle = toggle
        self.pressed = False
        self.hovered_over = False

        icon_file = pygame.image.load(icon).convert_alpha()
        self.icon = pygame.transform.scale(icon_file, [size - (size/10)]*2)
        if not pressed_icon:
            self.pressed_icon = self.icon
        else:
            pressed_icon_file = pygame.image.load(pressed_icon).convert_alpha()
            self.pressed_icon = pygame.transform.scale(pressed_icon_file, [size]*2)

        self.on_press = lambda: None
        self.on_release = lambda: None

    def draw(self):
        self.fill((0, 0, 0, 0))
        rect = self.get_rect()
        pygame.draw.circle(self, (self.pressed_color if self.pressed else self.color), rect.center, rect.width/2)
        if self.hovered_over and not self.pressed:
            pygame.draw.circle(self, self.hovered_over_color, rect.center, rect.width / 2)
        d = self.size[0] / 20
        if self.pressed:
            self.blit(self.pressed_icon, (d, d), (1, 1, 100, 100))
        else:
            self.blit(self.icon, (d, d), (1, 1, 100, 100))

        return self, [*self.pos, *self.size]

    def loop(self, events):
        super().loop(events)
        # self.drag_loop(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(*pygame.mouse.get_pos()):
                self.button_down(event.button)
                events.remove(event)
                break
            elif event.type == pygame.MOUSEBUTTONUP and self.pressed and not self.toggle:
                self.button_up(event.button)
                events.remove(event)
                break

            if event.type == pygame.MOUSEMOTION and self.collidepoint(*pygame.mouse.get_pos()):
                self.hovered_over = True
                break
            else:
                self.hovered_over = False
                break

    def button_down(self, button):
        if button == 1:  # only the left mouse button
            self.on_press()
            if self.toggle:
                self.pressed = not self.pressed
            else:
                self.pressed = True

    def button_up(self, button):
        if button < 4:  # to exclude scrolling
            self.pressed = False
            if self.collidepoint(*pygame.mouse.get_pos()):
                self.on_release()


class WheelButton(Button):
    def __init__(self, pos=(0, 0), size=50, cw_icon="assets/rotate_clock_wise.png",
                 acw_icon="assets/rotate_anti_clock_wise.png"):
        super().__init__(pos=pos, size=size,
                 icon=acw_icon, pressed_icon=cw_icon, toggle=False)

        cw_icon = pygame.image.load(cw_icon).convert_alpha()
        self.cw_icon = pygame.transform.scale(cw_icon, [size - (size / 10)] * 2)
        acw_icon = pygame.image.load(acw_icon).convert_alpha()
        self.acw_icon = pygame.transform.scale(acw_icon, [size - (size / 10)] * 2)

        self.pressed_color = self.hovered_over_color
        self.value = 0
        self.on_value = lambda: None

    def draw(self):
        self.fill((0, 0, 0, 0))

        self.icon = pygame.transform.rotate(self.acw_icon, self.value)
        self.pressed_icon = pygame.transform.rotate(self.cw_icon, self.value)

        # return super().draw()

        rect = self.get_rect()
        pygame.draw.circle(self, (self.pressed_color if self.pressed else self.color), rect.center, rect.width/2)
        if self.hovered_over and not self.pressed:
            pygame.draw.circle(self, self.hovered_over_color, rect.center, rect.width / 2)
        d = -((self.pressed_icon.get_rect().width - rect.width)/2)
        if self.pressed:
            self.blit(self.pressed_icon, (d, d), self.pressed_icon.get_rect())
        else:
            self.blit(self.icon, (d, d), self.pressed_icon.get_rect())

        return self, [*self.pos, *self.size]

    def button_down(self, button):
        if button == 5: # clock wise
            self.pressed = True
            self.value -= 5
            self.on_value(-5)
        elif button == 4: # anit clock wise
            self.pressed = False
            self.value += 1
            self.on_value(1)

    def button_up(self, button):
        pass

    def loop(self, events):
        super().loop(events)

