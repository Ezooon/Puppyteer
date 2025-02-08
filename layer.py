import pygame
from util import MySurface, Movable
from math import sin, cos, radians

SIZE = WIDTH, HEIGHT = 1080, 720


class Layer(MySurface, Movable):
    all = dict()
    show_boarders = False

    def __init__(self, image, filename, layercard, **kwargs):
        self.layer_image = image
        self.layercard = layercard

        # Layer data
        self.data            = dict()
        self.image_rect      = image.get_rect()
        self.pined_to_layer  = kwargs.get("pined_to_layer")
        self.pin_pos         = kwargs.get("pin_pos")
        self.angle           = kwargs.get("angle") or 0
        self.scale           = kwargs.get("scale") or 1
        self.layer_width     = kwargs.get("layer_width") or self.image_rect.width
        self.layer_height    = kwargs.get("layer_height") or self.image_rect.height
        self.layer_image_pos = kwargs.get("layer_image_pos") or (0, 0)
        self.mirrored        = kwargs.get("mirrored")
        self.mirror_distance = kwargs.get("mirror_distance") or self.image_rect.width
        self.mirror_angle    = kwargs.get("mirror_angle") or 1
        self.flipped         = kwargs.get("flipped") or False
        self.flipped_mirror  = kwargs.get("flipped_mirror") if kwargs.get("flipped_mirror") is not None else True

        self.save_data()

        self.scale_control = True
        self.distance_control = False
        self.move_speed = 5
        self.x_vol = 0
        self.y_vol = 0
        super().__init__(size=SIZE)

        if filename in Layer.all:
            filename += "0"
        self.filename = filename
        Layer.all[self.filename] = filename

    def save_data(self):
        self.data["pined_to_layer"]  = self.pined_to_layer
        self.data["pin_pos"]         = self.pin_pos
        self.data["angle"]           = self.angle
        self.data["scale"]           = self.scale
        self.data["layer_width"]     = self.layer_width
        self.data["layer_height"]    = self.layer_height
        self.data["layer_image_pos"] = self.layer_image_pos
        self.data["mirrored"]        = self.mirrored
        self.data["mirror_distance"] = self.mirror_distance
        self.data["mirror_angle"]    = self.mirror_angle
        self.data["flipped"]         = self.flipped
        self.data["flipped_mirror"]  = self.flipped_mirror

        if self.pined_to_layer and type(self.pined_to_layer) is not str:
            self.data["pined_to_layer"]  = self.pined_to_layer.filename

        return self.data

    def load_data(self, data, pined_to_layer=None):
        self.data            = data
        self.pined_to_layer  = self.data.get("pined_to_layer")
        self.pin_pos         = self.data.get("pin_pos")
        self.angle           = self.data.get("angle") or 0
        self.scale           = self.data.get("scale") or 1
        self.layer_width     = self.data.get("layer_width") or self.image_rect.width
        self.layer_height    = self.data.get("layer_height") or self.image_rect.height
        self.layer_image_pos = self.data.get("layer_image_pos") or (0, 0)
        self.mirrored        = self.data.get("mirrored")
        self.mirror_distance = self.data.get("mirror_distance") or self.image_rect.width
        self.mirror_angle    = self.data.get("mirror_angle") or 1
        self.flipped         = self.data.get("flipped") or False
        self.flipped_mirror  = self.data.get("flipped_mirror") if data.get("flipped_mirror") is not None else True

        self.pined_to_layer = pined_to_layer

    def collidepoint(self, x, y):
        mx1, my1 = self.image_rect[:2]
        w, h = self.image_rect[2:]
        x2 = mx1 + w
        y2 = my1 + h
        return mx1 <= x <= x2 and my1 <= y <= y2

    def draw(self):
        self.fill((0, 0, 0, 0))
        rect = self.get_rect()

        image = pygame.transform.scale(self.layer_image,
                                       (self.layer_width * self.scale, self.layer_height * self.scale))
        image = pygame.transform.rotate(image, self.angle)

        self.image_rect = image.get_rect()

        d = dx, dy = self.layer_image_pos

        if self.pined_to_layer:
            if self.check_pin():
                dx, dy = self.pined_to_layer.layer_image_pos
                px, py, *_ = self.pin_pos
                dx += px
                dy += py
                d = dx, dy
                self.layer_image_pos = d

        self.blit(image, d, rect)

        if self.mirrored:
            mirrored_image = image
            if self.flipped_mirror:
                mirrored_image = pygame.transform.flip(image, True, False)
            dest = (dx + (self.mirror_distance * cos(radians(self.mirror_angle))),
                    dy + (self.mirror_distance * (sin(radians(self.mirror_angle)) or 1)))

            self.blit(mirrored_image, dest, rect)
            self.image_rect = [*d, image.get_size()[1] * 2, image.get_size()[0]]
        else:
            self.image_rect = [*d, *image.get_size()]

        if Layer.show_boarders:
            pygame.draw.rect(self, (255, 0, 0), (*d, *image.get_size()), width=1)
            if self.mirrored:
                pygame.draw.rect(self, (0, 0, 255),
                                 (*dest,
                                  *mirrored_image.get_size()), width=1)

        draw = super().draw()
        return draw[0], [0, 0, *draw[1][2:]]

    def loop(self, events):
        super().loop(events)
        self.drag_loop(events)

        x, y = self.layer_image_pos
        self.layer_image_pos = x + self.x_vol, y + self.y_vol

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.scale_control = False
                    break
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.distance_control = True
                    break

                # arrow keys moving
                if self.layercard.on_top:
                    d = self.move_speed
                    if not self.scale_control:
                        d = self.move_speed * 3
                    elif self.distance_control:
                        d = self.move_speed / 2

                    if event.key == pygame.K_UP:
                        self.y_vol = - d
                    elif event.key == pygame.K_DOWN:
                        self.y_vol = d
                    elif event.key == pygame.K_LEFT:
                        self.x_vol = - d
                    elif event.key == pygame.K_RIGHT:
                        self.x_vol = d

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.scale_control = True
                    break
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.distance_control = False
                    break

                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    self.y_vol = 0
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.x_vol = 0


            elif event.type == pygame.MOUSEWHEEL and self.collidepoint(*pygame.mouse.get_pos()):
                if event.y > 0:  # Wheel moving up / anti clock wise
                    if self.distance_control and not self.scale_control:
                        self.mirror_angle += 5
                        self.angle += 5
                        events.remove(event)
                        break

                    elif self.distance_control:
                        self.mirror_distance += 10
                        events.remove(event)
                        break
                    elif self.scale_control:
                        self.scale = min(2, self.scale + 0.05)
                        events.remove(event)
                        break
                    else:
                        self.angle += 5
                        events.remove(event)
                        break
                elif event.y < 0:  # Wheel moving down / clock wise
                    if self.distance_control and not self.scale_control:
                        self.mirror_angle -= 5
                        self.angle -= 5
                        events.remove(event)
                        break

                    elif self.distance_control:
                        self.mirror_distance -= 10
                        events.remove(event)
                        break
                    elif self.scale_control:
                        self.scale = max(0.05, self.scale - 0.01)
                        events.remove(event)
                        break
                    else:
                        self.angle -= 20
                        events.remove(event)
                        break

    def check_pin(self):
        if type(self.pined_to_layer) is not str:
            return True
        if not (self.pined_to_layer in Layer.all):
            return False

        self.pined_to_layer = Layer.all[self.pined_to_layer]

    def mirror(self):
        self.mirrored = not self.mirrored

    def mirror_copy(self):
        self.mirrored = self.flipped_mirror
        self.flipped_mirror = not self.flipped_mirror

    def mirror_cut(self):
        self.flipped = not self.flipped
        self.layer_image = pygame.transform.flip(self.layer_image, True, False)

    def drag_loop(self, events):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(*pygame.mouse.get_pos())
                    and Movable.moving is None):
                Movable.moving = self
                self.layercard.put_on_top()
                mx, my = pygame.mouse.get_pos()
                x, y = self.layer_image_pos
                Movable.dx, Movable.dy = mx - x, my - y
                break
            elif event.type == pygame.MOUSEBUTTONUP and Movable.moving is not None:
                Movable.moving = None
                Movable.dx = 0
                Movable.dy = 0
                break

            if event.type == pygame.MOUSEMOTION and self.moving is not None:
                mx, my = event.pos
                x, y = mx - Movable.dx, my - Movable.dy
                if self.pined_to_layer:
                    ptx, pty, ptw, pth = self.pined_to_layer.image_rect
                    Movable.moving.pin_pos = x - ptx, y - pty
                Movable.moving.layer_image_pos = x, y
                break

