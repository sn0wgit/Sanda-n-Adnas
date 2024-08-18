import re
from re import search
import pygame as pg
from .. import setup, tools
from .. import constants as c
from .. components import info, sanda, adnas


class Menu(tools._State):
    def __init__(self):
        """Initializes the state"""
        tools._State.__init__(self)
        IsSingleGame = c.PLAYER1
        persist = {c.COIN_TOTAL: 0,
                   c.SCORE: 0,
                   c.SANDA_LIVES: 3,
                   c.ADNAS_LIVES: 3,
                   c.CURRENT_TIME: 0.0,
                   c.LEVEL_STATE: None,
                   c.CAMERA_START_X: 0,
                   c.SANDA_DEAD: False,
                   c.ADNAS_DEAD: False,
                   c.IsSingleGame: IsSingleGame}
        self.startup(0.0, persist)

    def startup(self, current_time, persist):
        """Called every time the game's state becomes this one. Initializes certain values"""
        self.IsSingleGame = persist[c.IsSingleGame]
        self.next = c.LOAD_SCREEN
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.OverheadInfo(self.game_info, c.MAIN_MENU)

        self.sprite_sheet = setup.GFX['title_screen']
        self.setup_background()
        self.setup_sanda()
        self.setup_adnas()
        self.setup_cursor()

    def setup_cursor(self):
        """Creates the arrow cursor to select 1 or 2 players game mode"""
        self.cursor = pg.sprite.Sprite()
        dest = (220, 358)
        self.cursor.image, self.cursor.rect = self.get_image(24, 160, 8, 8, dest, setup.GFX['item_objects'])
        self.cursor.state = c.PLAYER1


    def setup_sanda(self):
        """Places Sanda at the beginning of the level"""
        self.sanda = sanda.Sanda()
        self.sanda.rect.x = 160
        self.sanda.rect.bottom = c.GROUND_HEIGHT


    def setup_adnas(self):
        """Places Adnas at the beginning of the level"""
        self.adnas = adnas.Adnas()
        self.adnas.rect.bottom = c.GROUND_HEIGHT

    def save_mode(self, mode):
        """Saves 1 player or 2 players mode to file"""
        f = open("mode.txt", "w")
        if search("1", mode): number = "1"
        if search("2", mode): number = "2"
        f.write(number)
        f = open("mode.txt", "r")
        f.close

    def setup_background(self):
        """Setup the background image to blit"""
        self.background = setup.GFX['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                   (int(self.background_rect.width*c.MULTIPLIER),
                                    int(self.background_rect.height*c.MULTIPLIER)))
        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)

        self.image_dict = {}
        self.image_dict['GAME_NAME_BOX'] = self.get_image(1, 60, 176, 88, (184, 128), setup.GFX['title_screen'])



    def get_image(self, x, y, width, height, dest, sprite_sheet):
        """Returns images and rects to blit onto the screen"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        if sprite_sheet == setup.GFX['title_screen']:
            image.set_colorkey((255, 0, 220))
            image = pg.transform.scale(image,
                                   (int(rect.width*c.MULTIPLIER),
                                    int(rect.height*c.MULTIPLIER)))
        else:
            image.set_colorkey(c.BLACK)
            image = pg.transform.scale(image,
                                   (int(rect.width*c.MULTIPLIER),
                                    int(rect.height*c.MULTIPLIER)))

        rect = image.get_rect()
        rect.x = dest[0]
        rect.y = dest[1]
        return (image, rect)


    def update(self, surface, keys, current_time):
        """Updates the state every refresh"""
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.update_cursor(keys)
        self.IsSingleGame = self.check_cursor()
        self.overhead_info.update(self.game_info, self.IsSingleGame)

        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                     self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.sanda.image, self.sanda.rect)
        surface.blit(self.adnas.image, self.adnas.rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)


    def check_cursor(self):
        if self.cursor.state == c.PLAYER1:
            return(c.PLAYER1)
            print("c.PLAYER1")
        elif self.cursor.state == c.PLAYER2:
            return(c.PLAYER2)
            print("c.PLAYER2")

    def update_cursor(self, keys):
        """Update the position of the cursor"""
        input_list = [pg.K_RETURN]

        if self.cursor.state == c.PLAYER1:
            self.adnas.rect.x = -96
            self.cursor.rect.y = 398
            IsSingleGame = c.PLAYER2
            if keys[pg.K_DOWN]:
                self.cursor.state = c.PLAYER2
            for input in input_list:
                if keys[input]:
                    self.reset_game_info()
                    self.done = True
                    self.save_mode(self.cursor.state)
        elif self.cursor.state == c.PLAYER2:
            self.cursor.rect.y = 443
            self.adnas.rect.x = 112
            IsSingleGame = c.PLAYER2
            if keys[pg.K_UP]:
                self.cursor.state = c.PLAYER1
            for input in input_list:
                if keys[input]:
                    self.reset_game_info()
                    self.done = True
                    self.save_mode(self.cursor.state)


    def reset_game_info(self):
        """Resets the game info in case of a Game Over and restart"""
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.SANDA_LIVES] = 3
        self.game_info[c.ADNAS_LIVES] = 3
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_STATE] = None
        self.persist = self.game_info
