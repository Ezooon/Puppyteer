from os import listdir, path, makedirs

import json
import pygame

from datetime import datetime
from button import Button, WheelButton
from presetcard import PresetCard
from wheeldial import WheelDial
from layercard import LayerCard
from listview import ListView
from layer import Layer

import win32com.client


class HomeScreen(pygame.Surface):
    """
    Represents the home screen of the application. This is a custom surface built upon
    pygame.Surface to display the application's main UI components.

    The class provides methods for initializing UI, loading folder contents, rendering
    graphics, handling user input events, and opening a folder chooser dialog. It organizes
    the UI into layers and presets while allowing the user to interact with these elements.

    :ivar background_color: The background color of the home screen surface.
    :type background_color: tuple
    :ivar folder: The absolute or relative path to the folder that holds assets.
    :type folder: str
    :ivar layers_list: Widget for listing and interacting with layer items.
    :type layers_list: ListView
    :ivar preset_list: Widget for listing and interacting with preset items.
    :type preset_list: ListView
    :ivar uix: List of all UI components/widgets appearing on the home screen.
    :type uix: list
    """
    def __init__(self, size):
        super(HomeScreen, self).__init__(size)
        self.selected_layer_box_pos = (10, self.get_height() - 85)
        self.background_color = (0, 50, 100)
        self.folder = "assets_1"
        self.abs_pos = (0, 0)

        LayerCard.home = self

        self._set_ui()

        self.load_folder()

    def _set_ui(self):
        size = w, h = self.get_size()

        self.layers_list = ListView((size[0]-175, 0), (175, size[1]))
        self.preset_list = ListView((size[0]-self.layers_list.size[0]-71, 0), (70, size[1] - 150), padding=[2, 0])

        self.new_preset_button = Button(
            pos=(
                self.preset_list.pos[0] - (self.preset_list.size[0] / 2) + 3,
                self.preset_list.pos[1] + self.preset_list.size[1] - (self.preset_list.size[0] / 2) + 3),
            size=(self.preset_list.size[0] - 6),
            icon="assets/plus.png"
        )
        self.new_preset_button.on_release = self.new_preset

        folder_button = Button(pos=[size[0] - 45, size[1] - 45], size=40, icon="assets/folder.png")
        folder_button.on_press = self.choose_folder

        save_button = Button(pos=[size[0] - 45, size[1] - 90], size=40, icon="assets/save.png")
        save_button.on_press = self.save

        self.export_button = Button(icon="assets/export.png", size=40, pos=(5, h - 195))
        self.export_button.on_press = self.export_image

        # mirror the selected_cards layers to the left
        self.mirror_button = Button(icon="assets/mirror.png", size=40,
                                    pos=(5, h - 150))
        self.mirror_button.on_press = self.mirror_selected

        # mirror the selected_cards layers without flipping them
        self.mirror_copy_button = Button(icon="assets/mirror_copy.png", size=40,
                                         pos=(50, h - 150))
        self.mirror_copy_button.on_press = self.mirror_copy_selected

        # replace the selected_cards layers with a flipped version
        self.mirror_cut_button = Button(icon="assets/mirror_cut.png", size=40,
                                        pos=(95, h - 150))
        self.mirror_cut_button.on_press = self.mirror_cut_selected

        # replace the selected_cards layers with a flipped version
        self.show_boarders_button = Button(icon="assets/borders_eye.png", size=40,
                                           pos=(140, h - 150))
        self.show_boarders_button.on_press = lambda: setattr(Layer, "show_boarders", not Layer.show_boarders)

        plus_icon = pygame.image.load("assets/plus.png").convert_alpha()
        self.x_icon = pygame.transform.rotate(plus_icon, 45)
        self.x_icon = pygame.transform.scale(self.x_icon, (25, 25))
        self.selected_layer_width = WheelDial(pos=(50, h - 25), size=30)
        self.selected_layer_width.on_value = self.selected_layer_width_change
        self.selected_layer_height = WheelDial(pos=(115, h - 25), size=30)
        self.selected_layer_height.on_value = self.selected_layer_height_change

        self.pin_button = Button((191 - 15, h - 90 + 15), size=30, icon="assets/pin.png")
        self.pin_button.on_press = lambda: setattr(LayerCard, "pin_selection_mode", True)

        self.merge_button = Button(pos=(w - 226, h - 52), size=50, icon="assets/merge.png")
        self.merge_button.on_release = self.merge

        self.uix = [self.layers_list, self.preset_list,
                    self.export_button,
                    self.mirror_button,
                    self.mirror_copy_button,
                    self.mirror_cut_button,
                    self.show_boarders_button,
                    folder_button,
                    save_button,
                    self.selected_layer_width,
                    self.selected_layer_height,
                    self.new_preset_button,
                    self.pin_button,
                    self.merge_button,
                    ]

        # Set each object's parent to self
        for widget in self.uix:
            widget.parent = self

    def draw(self):

        w, h = self.get_size()
        self.fill(self.background_color)
        self.fill((200, 100, 50), [0, h-150, w - 150, 150])
        pygame.draw.circle(self, self.layers_list.background, (w - 195, h - 20), 40)


        # size control
        self.blit(self.x_icon, (75, h - 30), self.x_icon.get_rect())
        pygame.draw.rect(self, (0, 255, 0), (5, h - 90, 185, 60))
        pygame.draw.rect(self, (255, 255, 0), (191, h - 90, 185, 60))
        self.selected_layer_box_pos = (10, h - 85)
        if LayerCard.selected_cards:
            card = LayerCard.selected_cards[-1]
            self.selected_layer_width.value = card.layer.layer_width
            self.selected_layer_height.value = card.layer.layer_height
            self.blit(card, (10, h - 85), card.get_rect())
            if card.pined_to_layer:
                self.blit(card.pined_to_layer, (196, h - 85), card.get_rect())

        pygame.draw.circle(self, self.preset_list.background,
                           (self.preset_list.pos[0] #+ (self.preset_list.size[0]/2)
                            ,self.preset_list.pos[1] + self.preset_list.size[1]), self.preset_list.size[0] / 2)

        for widget in self.uix:
            self.blit(*widget.draw())

        for layercard in reversed(self.layers_list.uix):
            if layercard.visible:
                self.blit(*layercard.layer.draw())

    def loop(self, events):
        for widget in self.uix:
            widget.loop(events)

    def choose_folder(self):
        """Opens the native Windows folder chooser dialog."""
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.BrowseForFolder(0, "Select a folder", 0)
        if folder:
            self.folder = folder.Self.Path  # Returns the folder path as a string
            self.load_folder()
        return None

    def mirror_selected(self):
        LayerCard.selected_cards[-1].layer.mirror()

    def mirror_copy_selected(self):
        LayerCard.selected_cards[-1].layer.mirror_copy()

    def mirror_cut_selected(self):
        LayerCard.selected_cards[-1].layer.mirror_cut()

    def selected_layer_width_change(self, value):
        LayerCard.selected_cards[-1].layer.layer_width += value

    def selected_layer_height_change(self, value):
        LayerCard.selected_cards[-1].layer.layer_height += value

    def merge(self):
        right = bottom =  0
        left, top = self.get_size()
        layers = []
        Layer.show_boarders = False
        for layercard in reversed(self.layers_list.uix):
            if layercard.visible:
                layers.append(layercard.layer)
                layercard.visible = False

                x, y, w, h =  layercard.layer.image_rect
                left = x if left > x else left
                right = (x + w) if right < (x + w) else right
                top = y if top > y else top
                bottom = (y + h) if bottom < (y + h) else bottom
        if not layers:
            return

        surface = pygame.Surface((right - left, bottom - top), pygame.SRCALPHA, 32)
        Layer.show_boarders = False
        for layer in layers:
            sur, rect = layer.draw()
            x, y, w, h = rect
            surface.blit(sur, (x - left, y - top, w, h))

        filename = "merge_" +  str(datetime.now()) + ".png"
        filename = filename.replace(":", "_")
        pygame.image.save(surface, path.join(self.folder, filename))
        print(path.exists(path.join(self.folder, filename)))
        card = LayerCard(filename=path.join(self.folder, filename), name="merger")
        card.visible = True

        LayerCard.selected_cards = []
        LayerCard.selected_cards.append(card)
        self.layers_list.add_widget(card)

    def export_image(self):
        right = bottom =  0
        left, top = self.get_size()
        layers = []
        Layer.show_boarders = False
        for layercard in reversed(self.layers_list.uix):
            if layercard.visible:
                layers.append(layercard.layer)
                layercard.visible = False

                x, y, w, h =  layercard.layer.image_rect
                left = x if left > x else left
                right = (x + w) if right < (x + w) else right
                top = y if top > y else top
                bottom = (y + h) if bottom < (y + h) else bottom
        if not layers:
            return

        surface = pygame.Surface((right - left, bottom - top), pygame.SRCALPHA, 32)
        for layer in layers:
            sur, rect = layer.draw()
            x, y, w, h = rect
            surface.blit(sur, (x - left, y - top, w, h))

        makedirs(path.join(self.folder, "exported"), exist_ok=True)
        filename = path.join(self.folder, "exported", str(datetime.now()) + ".png")
        filename = filename.replace(":", "_")
        pygame.image.save(surface, filename)

    def new_preset(self):
        right = bottom =  0
        left, top = self.get_size()
        layers = []
        data = dict()
        Layer.show_boarders = False
        for layercard in reversed(self.layers_list.uix):
            if layercard.visible:
                layers.append(layercard.layer)
                layercard.visible = False
                data[layercard.filename] = layercard.layer.save_data()

                x, y, w, h =  layercard.layer.image_rect
                left = x if left > x else left
                right = (x + w) if right < (x + w) else right
                top = y if top > y else top
                bottom = (y + h) if bottom < (y + h) else bottom
        if not layers:
            return

        surface = pygame.Surface((right - left, bottom - top), pygame.SRCALPHA|pygame.RESIZABLE, 32)
        for layer in layers:
            sur, rect = layer.draw()
            x, y, w, h = rect
            surface.blit(sur, (x - left, y - top, w, h))

        card = PresetCard(surface=surface, data=data)

        self.preset_list.add_widget(card, 0)

    def save(self):
        data = {"presets": []}
        for layercard in reversed(self.layers_list.uix):
            data[layercard.filename] = layercard.layer.save_data()

        for presetcard in self.preset_list.uix:
            data["presets"].append(presetcard.data)

        folder_name = path.split(self.folder)[-1]
        with open(path.join(self.folder, folder_name + ".json"), "w") as f:
            json.dump(data, f, indent=4)

    def load_folder(self):
        '''loading layers from folder'''

        LayerCard.all = dict()
        LayerCard.selected_cards = []

        data = dict()

        folder_name = path.split(self.folder)[-1]
        if path.exists(path.join(self.folder, folder_name + ".json")):
            with open(path.join(self.folder, folder_name + ".json"), "r") as f:
                data = json.load(f)

        presets = data.get("presets") or []

        for filename in reversed(listdir(self.folder)):

            layer_file = path.join(self.folder, filename)
            if not layer_file.endswith("png"):
                continue

            if layer_file in data.keys():
                layer_data = data[layer_file]
            else:
                layer_data = dict()

            layercard = LayerCard.get(layer_file)
            if layer_data.get("pined_to_layer"):
                pined_to_layer = LayerCard.get(layer_data["pined_to_layer"])
                layercard.pined_to_layer = pined_to_layer
                layercard.layer.load_data(layer_data, pined_to_layer.layer)
            else:
                layercard.layer.load_data(layer_data)

        for preset_data in presets:
            # loading the presets to make take the thumbnails
            PresetCard.load_layers(preset_data)
            self.new_preset()
