__author__ = 'justinarmstrong'

import pygame as pg
from .. import constants as c
from .. import setup


class Powerup(pg.sprite.Sprite):
    """Base class for all powerup_group"""
    def __init__(self, x, y):
        super(Powerup, self).__init__()


    def setup_powerup(self, x, y, name, setup_frames):
        """This separate setup function allows me to pass a different
        setup_frames method depending on what the powerup is"""
        self.sprite_sheet = setup.GFX['item_objects']
        self.frames = []
        self.frame_index = 0
        setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.state = c.REVEAL
        self.y_vel = -1
        self.x_vel = 0
        self.direction = c.RIGHT
        self.box_height = y
        self.gravity = 1
        self.max_y_vel = 8
        self.animate_timer = 0
        self.name = name


    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*c.MULTIPLIER),
                                    int(rect.height*c.MULTIPLIER)))
        return image


    def update(self, game_info, *args):
        """Updates powerup behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()


    def handle_state(self):
        pass

    def revealing(self, *args):
        """Action when powerup leaves the coin box or brick"""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = c.SLIDE


    def sliding(self):
        """Action for when powerup slides along the ground"""
        if self.direction == c.RIGHT:
            self.x_vel = 3
        else:
            self.x_vel = -3


    def falling(self):
        """When powerups fall of a ledge"""
        if self.y_vel < self.max_y_vel:
            self.y_vel += self.gravity


class LifeMushroom(Powerup):
    """1up mushroom"""
    def __init__(self, x, y, name='1up_mushroom'):
        super(LifeMushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.get_image(61, 96, 19, 32))

    def handle_state(self):
        """Handle behavior based on state"""
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.SLIDE:
            self.sliding()
        elif self.state == c.FALL:
            self.falling()


    def revealing(self):
        """Animation of flower coming out of box"""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.state = c.SLIDE


class Scarab(Powerup):
    """A powerup that gives mario invincibility"""
    def __init__(self, x, y, name='Scarab'):
        super(Scarab, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)
        self.animate_timer = 0
        self.rect.y += 1  #looks more centered offset one pixel
        self.gravity = .4


    def setup_frames(self):
        """Creating the self.frames where the images for Scarab are stored"""
        self.frames.append(self.get_image(0, 17, 15, 14))


    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.BOUNCE:
            self.bouncing()


    def revealing(self):
        """When the star comes out of the box"""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.start_bounce(-2)
            self.state = c.BOUNCE


    def start_bounce(self, vel):
        """Transitions into bouncing state"""
        self.y_vel = vel


    def bouncing(self):
        """Action when the star is bouncing around"""

        if self.direction == c.LEFT:
            self.x_vel = -5
        else:
            self.x_vel = 5
