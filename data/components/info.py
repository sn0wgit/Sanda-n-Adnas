import pygame as pg
from os import path
from .. import setup
from .. import constants as c
from . import flashing_coin


class Character(pg.sprite.Sprite):
    """Parent class for all characters used for the overhead level info"""
    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()

class OverheadInfo(object):
    """Class for level information like score, coin total,
        and time remaining"""
    def __init__(self, game_info, state):
        self.sprite_sheet = setup.GFX['text_images']
        self.IsSingleGame = ""
        self.game_mode()
        self.coin_total = game_info[c.COIN_TOTAL]
        self.time = 401
        self.current_time = 0
        self.sanda_lives = game_info[c.SANDA_LIVES]
        if self.game_mode() == c.PLAYER2: self.adnas_lives = game_info[c.ADNAS_LIVES]
        self.state = state
        self.special_state = None
        self.game_info = game_info
        self.create_image_dict()
        self.create_sanda_score_group()
        if self.game_mode() == c.PLAYER2: self.create_adnas_score_group()
        self.create_info_labels()
        self.create_countdown_clock()
        self.create_coin_counter()
        self.create_flashing_coin()
        self.create_sanda_image()
        if self.game_mode() == c.PLAYER2: self.create_adnas_image()
        self.create_game_over_label()
        self.create_time_out_label()
        self.create_main_menu_labels()

    def create_image_dict(self):
        """Creates the initial images for the score"""
        self.image_dict = {}
        image_list = []
        image_list.append(self.get_image(3, 230, 7, 7))  #0
        image_list.append(self.get_image(11, 230, 7, 7)) #1
        image_list.append(self.get_image(19, 230, 7, 7)) #2
        image_list.append(self.get_image(27, 230, 7, 7)) #3
        image_list.append(self.get_image(35, 230, 7, 7)) #4
        image_list.append(self.get_image(43, 230, 7, 7)) #5
        image_list.append(self.get_image(51, 230, 7, 7)) #6
        image_list.append(self.get_image(59, 230, 7, 7)) #7
        image_list.append(self.get_image(67, 230, 7, 7)) #8
        image_list.append(self.get_image(75, 230, 7, 7)) #9
        image_list.append(self.get_image(83, 230, 7, 7)) #A
        image_list.append(self.get_image(91, 230, 7, 7)) #B
        image_list.append(self.get_image(99, 230, 7, 7)) #C
        image_list.append(self.get_image(107, 230, 7, 7))#D
        image_list.append(self.get_image(115, 230, 7, 7))#E
        image_list.append(self.get_image(123, 230, 7, 7))#F
        image_list.append(self.get_image(3, 238, 7, 7))  #G
        image_list.append(self.get_image(11, 238, 7, 7)) #H
        image_list.append(self.get_image(20, 238, 7, 7)) #I
        image_list.append(self.get_image(27, 238, 7, 7)) #J
        image_list.append(self.get_image(35, 238, 7, 7)) #K
        image_list.append(self.get_image(43, 238, 7, 7)) #L
        image_list.append(self.get_image(51, 238, 7, 7)) #M
        image_list.append(self.get_image(59, 238, 7, 7)) #N
        image_list.append(self.get_image(67, 238, 7, 7)) #O
        image_list.append(self.get_image(75, 238, 7, 7)) #P
        image_list.append(self.get_image(83, 238, 7, 7)) #Q
        image_list.append(self.get_image(91, 238, 7, 7)) #R
        image_list.append(self.get_image(99, 238, 7, 7)) #S
        image_list.append(self.get_image(108, 238, 6, 7))#T
        image_list.append(self.get_image(115, 238, 7, 7))#U
        image_list.append(self.get_image(123, 238, 7, 7))#V
        image_list.append(self.get_image(3, 246, 7, 7))  #W
        image_list.append(self.get_image(11, 246, 7, 7)) #X
        image_list.append(self.get_image(20, 246, 7, 7)) #Y
        image_list.append(self.get_image(27, 246, 7, 7)) #Z
        image_list.append(self.get_image(48, 246, 7, 7)) # 
        image_list.append(self.get_image(68, 249, 6, 2)) #-
        image_list.append(self.get_image(75, 247, 7, 7)) #x

        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image


    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((92, 148, 252))
        image = pg.transform.scale(image,
                                   (int(rect.width*c.MULTIPLIER),
                                    int(rect.height*c.MULTIPLIER)))
        return image

    def create_sanda_score_group(self):
        """Creates the initial empty score (000000)"""
        self.sanda_score_images = []
        self.create_label(self.sanda_score_images, '00000', 75, 55)

    def create_adnas_score_group(self):
        self.adnas_score_images = []
        self.create_label(self.adnas_score_images, '00000', 712, 55)

    def create_info_labels(self):
        """Creates the labels that describe each info"""
        self.sanda_label = []
        self.adnas_label = []
        self.time_label = []

        self.create_label(self.sanda_label, 'SANDA', 75, 30)
        self.create_label(self.adnas_label, 'ADNAS', 712, 30)
        self.create_label(self.time_label, 'TIME', 401, 30)
        self.label_list = [self.sanda_label,
                           self.adnas_label,
                           self.time_label]

    def create_countdown_clock(self):
        """Creates the count down clock for the level"""
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 420, 55)

    def create_label(self, label_list, string, x, y):
        """Creates a label (WORLD, TIME, MARIO)"""
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))

        self.set_label_rects(label_list, x, y)

    def set_label_rects(self, label_list, x, y):
        """Set the location of each individual character"""
        for i, letter in enumerate(label_list):
            letter.rect.x = x + ((letter.rect.width + 3) * i)
            letter.rect.y = y
            if letter.image == self.image_dict['-']:
                letter.rect.y += 7
                letter.rect.x += 2

    def create_coin_counter(self):
        """Creates the info that tracks the number of coins Mario collects"""
        self.coin_count_images = []
        self.create_label(self.coin_count_images, '*00', 98, 87)

    def create_flashing_coin(self):
        """Creates the flashing coin next to the coin total"""
        self.flashing_coin = flashing_coin.Coin(75, 80)

    def create_sanda_image(self):
        """Get the mario image"""
        self.life_times_image = self.get_image(75, 247, 6, 6)
        self.life_times_rect = self.life_times_image.get_rect(center=(378, 295))
        self.life_sanda_label = []
        self.create_label(self.life_sanda_label, str(self.sanda_lives), 450, 285)
        self.sprite_sheet = setup.GFX['characters']
        self.sanda_image = self.get_image(228, 1, 22, 31)
        self.sanda_rect = self.sanda_image.get_rect(center=(320, 290))

    def create_adnas_image(self):
        """Get the mario image"""
        print("create adnas image")
        self.life_times_image = self.get_image(75, 247, 6, 6)
        self.life_times_rect = self.life_times_image.get_rect(center=(378, 395))
        self.life_adnas_label = []
        self.create_label(self.life_adnas_label, str(self.adnas_lives), 450, 385)
        self.sprite_sheet = setup.GFX['characters']
        self.adnas_image = self.get_image(72, 1, 26, 31)
        self.adnas_rect = self.adnas_image.get_rect(center=(320, 390))

    def create_game_over_label(self):
        """Create the label for the GAME OVER screen"""
        game_over_label = []
        self.create_label(game_over_label, 'GAME OVER', 341, 325)
        self.game_over_label = [game_over_label]

    def create_time_out_label(self):
        """Create the label for the time out screen"""
        time_out_label = []
        self.create_label(time_out_label, 'TIME OUT', 351, 325)
        self.time_out_label = [time_out_label]

    def create_main_menu_labels(self):
        """Create labels for the MAIN MENU screen"""
        player_one_game = []
        player_two_game = []
        self.create_label(player_one_game, '1 PLAYER', 272, 400)
        self.create_label(player_two_game, '2 PLAYERS', 272, 445)
        self.main_menu_labels = [player_one_game, player_two_game]

    def update(self, level_info, sanda=None, adnas=None):
        """Updates all overhead info"""
        self.sanda = sanda
        self.adnas = adnas
        self.handle_level_state(level_info)

    def game_mode(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "states", "mode.txt"))
        f = open(filepath, "r")
        if f.read() == "1": self.IsSingleGame = c.PLAYER1
        elif f.read() == "2": self.IsSingleGame = c.PLAYER2
        return(self.IsSingleGame)

    def handle_level_state(self, level_info):
        """Updates info based on what state the game is in"""
        if self.state == c.MAIN_MENU:
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])

        elif self.state == c.LOAD_SCREEN:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.sanda_score_images, self.score)
            if self.game_mode() == c.PLAYER2: self.update_score_images(self.adnas_score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.LEVEL:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.sanda_score_images, self.score)
            if self.game_mode() == c.PLAYER2:
                self.update_score_images(self.adnas_score_images, self.score)
                if level_info[c.LEVEL_STATE] != c.FROZEN \
                and self.sanda.state != c.WALKING_TO_CASTLE \
                and self.sanda.state != c.END_OF_LEVEL_FALL \
                and self.adnas.state != c.WALKING_TO_CASTLE \
                and self.adnas.state != c.END_OF_LEVEL_FALL \
                and not self.sanda.dead and not self.adnas.dead:
                    self.update_count_down_clock(level_info)
            else:
                if level_info[c.LEVEL_STATE] != c.FROZEN \
                and self.sanda.state != c.WALKING_TO_CASTLE \
                and self.sanda.state != c.END_OF_LEVEL_FALL \
                and not self.sanda.dead:
                    self.update_count_down_clock(level_info)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])

        elif self.state == c.TIME_OUT:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.sanda_score_images, self.score)
            if self.game_mode == c.PLAYER2: self.update_score_images(self.adnas_score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.GAME_OVER:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.sanda_score_images, self.score)
            if self.game_mode == c.PLAYER2: self.update_score_images(self.adnas_score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.FAST_COUNT_DOWN:
            level_info[c.SCORE] += 50
            self.score = level_info[c.SCORE]
            self.update_count_down_clock(level_info)
            self.update_score_images(self.sanda_score_images, self.score)
            if self.game_mode == c.PLAYER2: self.update_score_images(self.adnas_score_images, self.score)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])
            if self.time == 0:
                self.state = c.END_OF_LEVEL

        elif self.state == c.END_OF_LEVEL:
            self.flashing_coin.update(level_info[c.CURRENT_TIME])

    def update_score_images(self, images, score):
        """Updates what numbers are to be blitted for the score"""
        index = len(images) - 1

        for digit in reversed(str(score)):
            rect = images[index].rect
            images[index] = Character(self.image_dict[digit])
            images[index].rect = rect
            index -= 1

    def update_count_down_clock(self, level_info):
        """Updates current time"""
        if self.state == c.FAST_COUNT_DOWN:
            self.time -= 1

        elif (level_info[c.CURRENT_TIME] - self.current_time) > 400:
            self.current_time = level_info[c.CURRENT_TIME]
            self.time -= 1
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 413, 55)
        if len(self.count_down_images) < 2:
            for i in range(2):
                self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 413, 55)
        elif len(self.count_down_images) < 3:
            self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 413, 55)

    def update_coin_total(self, level_info):
        """Updates the coin total and adjusts label accordingly"""
        self.coin_total = level_info[c.COIN_TOTAL]

        coin_string = str(self.coin_total)
        if len(coin_string) < 2:
            coin_string = '*0' + coin_string
        elif len(coin_string) > 2:
            coin_string = '*00'
        else:
            coin_string = '*' + coin_string

        x = self.coin_count_images[0].rect.x
        y = self.coin_count_images[0].rect.y

        self.coin_count_images = []

        self.create_label(self.coin_count_images, coin_string, x, y)

    def draw(self, surface):
        """Draws overhead info based on state"""
        if self.state == c.MAIN_MENU:
            self.draw_main_menu_info(surface)
        elif self.state == c.LOAD_SCREEN:
            self.draw_loading_screen_info(surface)
        elif self.state == c.LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == c.GAME_OVER:
            self.draw_game_over_screen_info(surface)
        elif self.state == c.FAST_COUNT_DOWN:
            self.draw_level_screen_info(surface)
        elif self.state == c.END_OF_LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == c.TIME_OUT:
            self.draw_time_out_screen_info(surface)
        else:
            pass

    def draw_main_menu_info(self, surface):
        """Draws info for main menu"""
        for info in self.sanda_score_images:
            surface.blit(info.image, info.rect)

        if self.game_mode() == c.PLAYER2: 
            for info in self.adnas_score_images:
                surface.blit(info.image, info.rect)

        for label in self.main_menu_labels:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_loading_screen_info(self, surface):
        """Draws info for loading screen"""
        for info in self.sanda_score_images:
            surface.blit(info.image, info.rect)
        if self.IsSingleGame == c.PLAYER2:
            for info in self.adnas_score_images:
                surface.blit(info.image, info.rect)

        for word in self.life_sanda_label:
            surface.blit(word.image, word.rect)
        if self.IsSingleGame == c.PLAYER2:
            for word in self.life_adnas_label:
                surface.blit(word.image, word.rect)

        surface.blit(self.sanda_image, self.sanda_rect)
        if self.IsSingleGame == c.PLAYER2: surface.blit(self.adnas_image, self.adnas_rect)
        surface.blit(self.life_times_image, self.life_times_rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_level_screen_info(self, surface):
        """Draws info during regular game play"""
        for info in self.sanda_score_images:
            surface.blit(info.image, info.rect)

        if self.game_mode() == c.PLAYER2:
            for info in self.adnas_score_images:
                surface.blit(info.image, info.rect)

        for digit in self.count_down_images:
                surface.blit(digit.image, digit.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_game_over_screen_info(self, surface):
        """Draws info when game over"""
        for info in self.sanda_score_images:
            surface.blit(info.image, info.rect)

        if self.game_mode() == c.PLAYER2:
            for info in self.sanda_score_images:
                surface.blit(info.image, info.rect)

        for word in self.game_over_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_time_out_screen_info(self, surface):
        """Draws info when on the time out screen"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.time_out_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)