import json
import pygame
from button import Button
from layercard import LayerCard


class PresetCard(Button):
    def __init__(self, pos=(0, 0), size=66, data=None, surface=None):
        super(PresetCard, self).__init__(pos, size)

        if surface:
            self.pressed_icon = self.icon = pygame.transform.scale(surface, [size - (size/10)]*2)

        self.data = data or dict()
        self.color = (153, 117, 56)
        self.pressed_color = (133, 97, 36)
        self.hovered_over_color = (163, 127, 66)
        self.on_press = print

    def draw(self):
        rect = self.get_rect()
        pygame.draw.rect(self, (self.pressed_color if self.pressed else self.color), rect, self.size[0], 5)
        if self.hovered_over and not self.pressed:
            pygame.draw.rect(self, self.hovered_over_color, rect, 4, 5)
        d = self.size[0] / 20
        if self.pressed:
            self.blit(self.pressed_icon, (d, d), (1, 1, 100, 100))
        else:
            self.blit(self.icon, (d, d), (1, 1, 100, 100))

        return self, [*self.pos, *self.size]

    def button_down(self, button):
        if button == 1:  # only the left mouse button
            self.on_press()
            self.load_layers(self.data)
            if self.toggle:
                self.pressed = not self.pressed
            else:
                self.pressed = True
        elif button == 3:
            self.delete()

    @classmethod
    def load_layers(cls, data):
        for layer_file, layer_data in data.items():
            layercard = LayerCard.get(layer_file)
            if layercard is None:
                continue
            layercard.visible = True
            if layer_data.get("pined_to_layer"):
                pined_to_layer = LayerCard.get(layer_data["pined_to_layer"])
                layercard.pined_to_layer = pined_to_layer
                pined_to_layer.visible = True
                layercard.layer.load_data(layer_data, pined_to_layer.layer)
            else:
                layercard.layer.load_data(layer_data)

    def delete(self):
        self.parent.remove_widget(self)
        print('dhi')
