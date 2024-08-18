__author__ = 'justinarmstrong'

import pygame as pg
from . import setup
from . import constants as c

class Sound(object):
    """Handles all sound for the game"""
    def __init__(self, overhead_info):
        """Initialize the class"""
        self.sfx_dict = setup.SFX
        self.music_dict = setup.MUSIC
        self.overhead_info = overhead_info
        self.game_info = overhead_info.game_info
        self.set_music_mixer()



    def set_music_mixer(self):
        """Sets music for level"""
        if self.overhead_info.state == c.LEVEL:
            #pg.mixer.music.load(self.music_dict['main_theme'])
            #pg.mixer.music.play()
            self.state = c.NORMAL
        if self.overhead_info.state == c.GAME_OVER:
            pg.mixer.music.load(self.music_dict['game_over'])
            pg.mixer.music.play()
            self.state = c.GAME_OVER


    def update(self, game_info, sanda, adnas):
        """Updates sound object with game info"""
        self.game_info = game_info
        self.sanda = sanda
        self.adnas = adnas
        self.handle_state()

    def handle_state(self):
        """Handles the state of the soundn object"""
        if self.adnas != None:
            if self.state == c.NORMAL:
                if self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)
                elif self.sanda.dead or self.adnas.dead:
                    self.play_music('death', c.ADNAS_DEAD)
                #elif self.mario.invincible \
                #        and self.mario.losing_invincibility == False:
                #    self.play_music('invincible', c.MARIO_INVINCIBLE)
                elif self.sanda.state == c.FLAGPOLE or self.adnas.state == c.FLAGPOLE:
                    self.play_music('flagpole', c.FLAGPOLE)
                elif self.overhead_info.time == 100:
                    self.play_music('out_of_time', c.TIME_WARNING)

            elif self.state == c.FLAGPOLE:
                if self.sanda.state == c.WALKING_TO_CASTLE or self.adnas.state == c.WALKING_TO_CASTLE:
                    self.play_music('stage_clear', c.STAGE_CLEAR)

            elif self.state == c.STAGE_CLEAR:
                if self.sanda.in_castle or self.adnas.in_castle:
                    self.sfx_dict['count_down'].play()
                    self.state = c.FAST_COUNT_DOWN

            elif self.state == c.FAST_COUNT_DOWN:
                if self.overhead_info.time == 0:
                    self.sfx_dict['count_down'].stop()
                    self.state = c.WORLD_CLEAR

            elif self.state == c.TIME_WARNING:
                if pg.mixer.music.get_busy() == 0:
                    self.play_music('main_theme_sped_up', c.SPED_UP_NORMAL)
                elif self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)
                elif self.adnas.dead:
                    self.play_music('death', c.ADNAS_DEAD)

            elif self.state == c.SPED_UP_NORMAL:
                if self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)
                elif self.adnas.dead:
                    self.play_music('death', c.ADNAS_DEAD)
                elif self.sanda.state == c.FLAGPOLE or self.adnas.state == c.FLAGPOLE:
                    self.play_music('flagpole', c.FLAGPOLE)

            elif self.state == c.SANDA_INVINCIBLE:
                if (self.sanda.current_time - self.sanda.invincible_start_timer) > 11000:
                    self.play_music('main_theme', c.NORMAL)
                elif self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)

            elif self.state == c.ADNAS_INVINCIBLE:
                if (self.adnas.current_time - self.adnas.invincible_start_timer) > 11000:
                    self.play_music('main_theme', c.NORMAL)
                elif self.adnas.dead:
                    self.play_music('death', c.ADNAS_DEAD)

            elif self.state == c.WORLD_CLEAR or self.state == c.SANDA_DEAD or self.state == c.ADNAS_DEAD or self.state == c.GAME_OVER:
                pass


        elif self.adnas == None:
            if self.state == c.NORMAL:
                if self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)
                #elif self.mario.invincible \
                #        and self.mario.losing_invincibility == False:
                #    self.play_music('invincible', c.MARIO_INVINCIBLE)
                elif self.sanda.state == c.FLAGPOLE:
                    self.play_music('flagpole', c.FLAGPOLE)
                elif self.overhead_info.time == 100:
                    self.play_music('out_of_time', c.TIME_WARNING)

            elif self.state == c.FLAGPOLE:
                if self.sanda.state == c.WALKING_TO_CASTLE:
                    self.play_music('stage_clear', c.STAGE_CLEAR)

            elif self.state == c.STAGE_CLEAR:
                if self.sanda.in_castle:
                    self.sfx_dict['count_down'].play()
                    self.state = c.FAST_COUNT_DOWN

            elif self.state == c.FAST_COUNT_DOWN:
                if self.overhead_info.time == 0:
                    self.sfx_dict['count_down'].stop()
                    self.state = c.WORLD_CLEAR

            elif self.state == c.TIME_WARNING:
                if pg.mixer.music.get_busy() == 0:
                    self.play_music('main_theme_sped_up', c.SPED_UP_NORMAL)
                elif self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)

            elif self.state == c.SPED_UP_NORMAL:
                if self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)
                elif self.sanda.state == c.FLAGPOLE or self.adnas.state == c.FLAGPOLE:
                    self.play_music('flagpole', c.FLAGPOLE)

            elif self.state == c.SANDA_INVINCIBLE:
                if (self.sanda.current_time - self.sanda.invincible_start_timer) > 11000:
                    self.play_music('main_theme', c.NORMAL)
                elif self.sanda.dead:
                    self.play_music('death', c.SANDA_DEAD)

            elif self.state == c.WORLD_CLEAR or self.state == c.SANDA_DEAD or self.state == c.GAME_OVER:
                pass

    def play_music(self, key, state):
        """Plays new music"""
        pg.mixer.music.load(self.music_dict[key])
        pg.mixer.music.play()
        self.state = state

    def stop_music(self):
        """Stops playback"""
        pg.mixer.music.stop()
