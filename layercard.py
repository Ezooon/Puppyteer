import pygame
from util import MySurface, write
from button import Button
from os.path import split, exists
from layer import Layer


class LayerCard(MySurface):
    """
    Representation of a graphical UI component to manage layers in a surface.

    The LayerCard class extends the MySurface class, providing specialized features for
    displaying and managing layer information in a UI. It allows interactions through
    mouse events, supports visual effects when hovered or pressed, and can toggle
    between states. The class also provides drawing functionality to render its
    visual representation and contains UI elements such as buttons for additional actions.

    :ivar selected: Stores the currently selected LayerCard instances.
    :type selected: list[LayerCard]
    :ivar layer_image: Scaled image representation of the layer.
    :type layer_image: pygame.Surface
    :ivar name: Optional name for the layer, defaults to the name of the filename if not specified.
    :type name: str
    :ivar uix: List of Button instances embedded in the LayerCard for specific actions.
    :type uix: list[Button]
    :ivar background: Color of the LayerCard background when not hovered or pressed.
    :type background: tuple[int, int, int, int]
    :ivar pressed_color: Color of the LayerCard background when pressed.
    :type pressed_color: tuple[int, int, int, int]
    :ivar hovered_over_color: Color of the background when hovered but not pressed.
    :type hovered_over_color: tuple[int, int, int, int]
    :ivar hovered_over_pressed_color: Color of the background when both hovered and pressed.
    :type hovered_over_pressed_color: tuple[int, int, int, int]
    :ivar toggle: Indicates whether the LayerCard is toggleable.
    :type toggle: bool
    :ivar pressed: Indicates if the LayerCard is currently pressed.
    :type pressed: bool
    :ivar hovered_over: Indicates whether the cursor is hovering over the LayerCard.
    :type hovered_over: bool
    :ivar on_press: Callback function triggered when the LayerCard is pressed.
    :type on_press: callable
    :ivar on_release: Callback function triggered when the LayerCard is released.
    :type on_release: callable
    """
    selected = []
    
    all = dict()

    home = None

    pin_selection_mode = False

    def __init__(self, pos=(0, 0), size=(175, 50), filename="assets/no_layer.png", surface=None, name=None):
        super().__init__(pos, size)

        self.pined_to_layer = None
        self.filename = filename
        layer_image = surface or pygame.image.load(filename).convert_alpha()
        self.layer = Layer(layer_image, filename)
        self.layer_image = pygame.transform.scale(layer_image, [self.size[1]]*2)
        self.name = name or (split(filename)[-1])[:-4].replace("_", " ")
        self.visible = False

        if filename in LayerCard.all:
            filename += "0"  # Todo, instead save the new surface as a file and use it here
        self.filename = filename
        LayerCard.all[self.filename] = self

        self._set_ui()

        self.toggle = True
        self.pressed = False
        self.hovered_over = False
        self.on_press = print
        self.on_release = print

    def _set_ui(self):
        self.visible_button = Button(pos=(50, 25), icon="assets/eye.png",
                                     pressed_icon="assets/eye_closed.png", toggle=True)
        self.visible_button.pressed = True
        self.visible_button.on_press = self.show_hide

        self.delete_button = Button(pos=(75, 25), icon="assets/trash.png")
        self.delete_button.on_release = self.delete

        self.duplicate_button = Button(pos=(100, 25), icon="assets/mirror.png")
        self.duplicate_button.on_release = self.duplicate

        self.move_down_button = Button(pos=(125, 25), icon="assets/arrow_down.png")
        self.move_down_button.on_release = self.move_down

        self.move_up_button = Button(pos=(150, 25), icon="assets/arrow_up.png")
        self.move_up_button.on_release = self.move_up

        self.uix = [
            self.visible_button,
            self.delete_button,
            self.duplicate_button,
            self.move_up_button,
            self.move_down_button,
        ]

        self.background = (50, 50, 50, 100)
        self.pressed_color = (50, 50, 50, 150)
        self.hovered_over_color = (100, 100, 100, 100)
        self.hovered_over_pressed_color = (100, 100, 100, 150)


    def show_hide(self):
        self.visible = not self.visible
        if self.visible:
            if self in LayerCard.selected:
                LayerCard.selected.remove(self)
            LayerCard.selected.append(self)

    def draw(self):
        if self.pressed and not self.hovered_over:
            self.fill(self.pressed_color)
        elif self.hovered_over and self.pressed:
            self.fill(self.hovered_over_pressed_color)
        elif self.hovered_over and not self.pressed:
            self.fill(self.hovered_over_color)
        else:
            self.fill(self.background)

        self.visible_button.pressed = not self.visible

        self.blit(self.layer_image, (0, 0), self.get_rect())
        write(self, self.name, 12, (self.size[1] + 5, 0))

        return super().draw()

    def loop(self, events):
        super().loop(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(*pygame.mouse.get_pos()):
                if event.button == 1: # only the left mouse button
                    self.card_down()
                    if self.toggle:
                        self.pressed = not self.pressed
                    else:
                        self.pressed = True
                    break
            elif event.type == pygame.MOUSEBUTTONUP and self.pressed and not self.toggle:
                if event.button < 4: # to exclude scrolling
                    self.card_up()
                    self.pressed = False
                    break

            # if self.pressed and self not in LayerCard.selected:
            #     LayerCard.selected.append(self)
            # elif not self.pressed and self in LayerCard.selected:
            #     LayerCard.selected.remove(self) # Todo remove thtis block if no trouble happen

            if event.type == pygame.MOUSEMOTION and self.collidepoint(*pygame.mouse.get_pos()):
                self.hovered_over = True
                break
            else:
                self.hovered_over = False
                break
        if self.visible and self in LayerCard.selected:
            self.layer.loop(events)

    def delete(self):
        self.parent.remove_widget(self)
        LayerCard.all.pop(self.filename)
        del self

    def move_up(self):
        i = self.parent._uix.index(self)
        self.parent._uix.pop(i)
        self.parent._uix.insert(i-1, self)

    def move_down(self):
        i = self.parent._uix.index(self)
        self.parent._uix.pop(i)
        self.parent._uix.insert(i+1, self)

    def duplicate(self):
        new = LayerCard(filename=self.filename, name=(self.name + "_duplicate"))
        new.layer.angle = self.layer.angle
        new.layer.scale = self.layer.scale
        new.layer.image_rect = self.layer.image_rect

        i = self.parent._uix.index(self)
        # self.parent._uix.insert(i + 1, new)
        self.parent.add_widget(new, i+1)

    def card_down(self):
        if LayerCard.pin_selection_mode and LayerCard.selected:
            LayerCard.selected[-1].layer.pined_to_layer = self.layer

            ptx, pty, *_ = self.layer.image_rect
            x, y, *_ = LayerCard.selected[-1].layer.image_rect
            LayerCard.selected[-1].layer.pin_pos = x - ptx, y - pty

            LayerCard.selected[-1].pined_to_layer = self
            LayerCard.pin_selection_mode = False
            return

        if self in LayerCard.selected:
            LayerCard.selected.remove(self)
        else:
            LayerCard.selected.append(self)

    def card_up(self):
        pass

    @classmethod
    def get(cls, filename):
        layercard = cls.all.get(filename)

        if layercard is not None:
            return layercard

        if exists(filename):
            layercard = LayerCard(filename=filename)
            cls.home.layers_list.add_widget(layercard)
            cls.selected.append(layercard)
            return layercard

        return None

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + self.name
