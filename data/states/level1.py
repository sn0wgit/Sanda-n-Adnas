from __future__ import division


import pygame as pg
from .. import setup, tools
from .. import constants as c
from .. import game_sound
from .. components import sanda
from .. components import adnas
from .. components import collider
from .. components import bricks
from .. components import coin_box
from .. components import enemies
from .. components import checkpoint
from .. components import flagpole
from .. components import info
from .. components import score
from .. components import castle_flag


class Level1(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.SANDA_DEAD] = False
        self.game_info[c.ADNAS_DEAD] = False

        self.state = c.NOT_FROZEN
        self.death_timer = 0
        self.flag_timer = 0
        self.flag_score = None
        self.flag_score_total = 0

        self.moving_score_list = []
        self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)
        self.sound_manager = game_sound.Sound(self.overhead_info_display)

        self.setup_background()
        self.setup_ground()
        self.setup_vazes()
        self.setup_steps()
        self.setup_bricks()
        self.setup_coin_boxes()
        self.setup_flag_pole()
        self.setup_enemies()
        self.setup_sanda()
        if self.game_mode() == c.PLAYER2: self.setup_adnas()
        self.setup_checkpoints()
        self.setup_spritegroups()


    def setup_background(self):
        """Sets the background image, rect and scales it to the correct
        proportions"""
        self.background = setup.GFX['level_1']
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                  (int(self.back_rect.width*c.MULTIPLIER),
                                  int(self.back_rect.height*c.MULTIPLIER)))
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = setup.SCREEN.get_rect(bottom=self.level_rect.bottom)
        self.viewport.x = self.game_info[c.CAMERA_START_X]


    def setup_ground(self): #done
        """Creates collideable, invisible rectangles over top of the ground for
        sprites to walk on"""
        ground_rect1 = collider.Collider(0, c.GROUND_HEIGHT,    3360, 72)
        ground_rect2 = collider.Collider(3456, c.GROUND_HEIGHT,  672, 72)
        ground_rect3 = collider.Collider(4272, c.GROUND_HEIGHT, 3072, 72)
        ground_rect4 = collider.Collider(7440, c.GROUND_HEIGHT, 2736, 72)

        self.ground_group = pg.sprite.Group(ground_rect1,
                                           ground_rect2,
                                           ground_rect3,
                                           ground_rect4)


    def setup_vazes(self): #done
        """Create collideable rects for all the vases"""

        vaze0 = collider.Collider(528, 504, 66, 96)
        vaze1 = collider.Collider(1425, 534, 96, 66)
        vaze2 = collider.Collider(2223, 408, 66, 192)
        vaze3 = collider.Collider(2751, 408, 66, 192)
        vaze4 = collider.Collider(7839, 504, 66, 96)
        vaze5 = collider.Collider(8670, 504, 66, 96)

        self.vaze_group = pg.sprite.Group(vaze1, vaze2,
                                          vaze3, vaze4,
                                          vaze5, vaze0)


    def setup_steps(self): #кубики
        """Create collideable rects for all the steps"""
        step1  = collider.Collider(6528, 504, 96, 96)
        step2  = collider.Collider(6624, 408, 96, 192)
        step3  = collider.Collider(6720, 504, 96, 96)

        step4  = collider.Collider(7152, 504, 96, 96)
        step5  = collider.Collider(7248, 408, 96, 192)

        step6  = collider.Collider(7440, 408, 96, 192)
        step7  = collider.Collider(7536, 504, 96, 96)

        step8  = collider.Collider(8736, 504, 96, 96)
        step9  = collider.Collider(8832, 408, 96, 192)
        step10 = collider.Collider(8928, 312, 96, 288)
        step11 = collider.Collider(9024, 216, 96, 384)

        self.step_group = pg.sprite.Group(step1,  step2,
                                          step3,  step4,
                                          step5,  step6,
                                          step7,  step8,
                                          step9,  step10,
                                          step11)


    def setup_bricks(self):
        """Creates all the breakable bricks for the level. Coin and
        powerup groups are created so they can be passed to bricks."""
        self.coin_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()
        self.brick_pieces_group = pg.sprite.Group()

        brick6  = bricks.Brick(3840, 218)
        brick8  = bricks.Brick(3936, 218)
        brick10 = bricks.Brick(4032, 218)
        brick12 = bricks.Brick(4128, 218)
        brick15 = bricks.Brick(4416, 218)
        brick17 = bricks.Brick(4512, 409, c.SIXCOINS, self.coin_group)
        brick19 = bricks.Brick(4848, 409, c.SCARAB, self.powerup_group)
        brick20 = bricks.Brick(5664, 409)
        brick21 = bricks.Brick(5808, 218)
        brick23 = bricks.Brick(5904, 218)
        brick24 = bricks.Brick(6096, 218)
        brick25 = bricks.Brick(6192, 409)
        brick27 = bricks.Brick(6288, 218)
        brick28 = bricks.Brick(8064, 409)
        brick30 = bricks.Brick(8256, 409)

        self.brick_group = pg.sprite.Group(brick6,  brick8,
                                           brick10, brick12,
                                           brick15, brick17,
                                           brick19, brick20,
                                           brick21, brick23,
                                           brick24, brick25,
                                           brick25, brick27, 
                                           brick28, brick30)


    def setup_coin_boxes(self):
        """Creates all the coin boxes and puts them in a sprite group"""
        coin_box1  = coin_box.Coin_box(768, 360, c.COIN, self.coin_group)
        coin_box2  = coin_box.Coin_box(1008, 360, c.COIN, self.coin_group)
        coin_box3  = coin_box.Coin_box(1104, 360, c.COIN, self.coin_group)
        coin_box4  = coin_box.Coin_box(1056, 168, c.COIN, self.coin_group)
        coin_box5  = coin_box.Coin_box(3744, 409, c.COIN, self.coin_group)
        coin_box6  = coin_box.Coin_box(4512, 218, c.COIN, self.coin_group)
        coin_box7  = coin_box.Coin_box(5056, 409, c.COIN, self.coin_group)
        coin_box8  = coin_box.Coin_box(5232, 409, c.COIN, self.coin_group)
        coin_box9  = coin_box.Coin_box(5232, 218, c.COIN, self.coin_group)
        coin_box10 = coin_box.Coin_box(5408, 409, c.COIN, self.coin_group)
        coin_box11 = coin_box.Coin_box(6192, 218, c.COIN, self.coin_group)
        coin_box13 = coin_box.Coin_box(8160, 409, c.COIN, self.coin_group)

        self.coin_box_group = pg.sprite.Group(coin_box1,  coin_box2,
                                              coin_box3,  coin_box4,
                                              coin_box5,  coin_box6,
                                              coin_box7,  coin_box8,
                                              coin_box9,  coin_box10,
                                              coin_box11, coin_box13)


    def setup_flag_pole(self):
        """Creates the flag pole at the end of the level"""
        self.flag = flagpole.Flag(9525, 100)

        pole0 = flagpole.Pole(9525, 120)
        pole1 = flagpole.Pole(9525, 153)
        pole2 = flagpole.Pole(9525, 198)
        pole3 = flagpole.Pole(9525, 217)
        pole4 = flagpole.Pole(9525, 257)
        pole5 = flagpole.Pole(9525, 297)
        pole6 = flagpole.Pole(9525, 337)
        pole7 = flagpole.Pole(9525, 377)
        pole8 = flagpole.Pole(9525, 417)
        pole9 = flagpole.Pole(9525, 450)

        finial = flagpole.Finial(9531, 97)

        self.flag_pole_group = pg.sprite.Group(self.flag,
                                               finial,
                                               pole0,
                                               pole1,
                                               pole2,
                                               pole3,
                                               pole4,
                                               pole5,
                                               pole6,
                                               pole7,
                                               pole8,
                                               pole9)


    def setup_enemies(self):
        """Creates all the enemies and stores them in a list of lists."""
        goomba0 = enemies.Goomba()
        goomba1 = enemies.Goomba()
        goomba2 = enemies.Goomba()
        goomba3 = enemies.Goomba()
        goomba4 = enemies.Goomba(193)
        goomba5 = enemies.Goomba(193)
        goomba6 = enemies.Goomba()
        goomba7 = enemies.Goomba()
        goomba8 = enemies.Goomba()
        goomba9 = enemies.Goomba()
        goomba10 = enemies.Goomba()
        goomba11 = enemies.Goomba()
        goomba12 = enemies.Goomba()
        goomba13 = enemies.Goomba()
        goomba14 = enemies.Goomba()
        goomba15 = enemies.Goomba()

        koopa0 = enemies.Koopa()

        enemy_group1 = pg.sprite.Group(goomba0)
        enemy_group2 = pg.sprite.Group(goomba1)
        enemy_group3 = pg.sprite.Group(goomba2, goomba3)
        enemy_group4 = pg.sprite.Group(goomba4, goomba5)
        enemy_group5 = pg.sprite.Group(goomba6, goomba7)
        enemy_group6 = pg.sprite.Group(koopa0)
        enemy_group7 = pg.sprite.Group(goomba8, goomba9)
        enemy_group8 = pg.sprite.Group(goomba10, goomba11)
        enemy_group9 = pg.sprite.Group(goomba12, goomba13)
        enemy_group10 = pg.sprite.Group(goomba14, goomba15)

        self.enemy_group_list = [enemy_group1,
                                 enemy_group2,
                                 enemy_group3,
                                 enemy_group4,
                                 enemy_group5,
                                 enemy_group6,
                                 enemy_group7,
                                 enemy_group8,
                                 enemy_group9,
                                 enemy_group10]


    def setup_adnas(self):
        """Places Sanda at the beginning of the level"""
        self.adnas = adnas.Adnas()
        self.adnas.rect.x = self.viewport.x + 160
        self.adnas.rect.bottom = c.GROUND_HEIGHT


    def setup_sanda(self):
        """Places Sanda at the beginning of the level"""
        self.sanda = sanda.Sanda()
        self.sanda.rect.x = self.viewport.x + 160
        self.sanda.rect.bottom = c.GROUND_HEIGHT


    def setup_checkpoints(self):
        """Creates invisible checkpoints that when collided will trigger
        the creation of enemies from the self.enemy_group_list"""
        check1 = checkpoint.Checkpoint(510, "1")
        check2 = checkpoint.Checkpoint(1400, '2')
        check3 = checkpoint.Checkpoint(1740, '3')
        check4 = checkpoint.Checkpoint(3080, '4')
        check5 = checkpoint.Checkpoint(3750, '5')
        check6 = checkpoint.Checkpoint(4150, '6')
        check7 = checkpoint.Checkpoint(4470, '7')
        check8 = checkpoint.Checkpoint(4950, '8')
        check9 = checkpoint.Checkpoint(5100, '9')
        check10 = checkpoint.Checkpoint(6800, '10')
        check11 = checkpoint.Checkpoint(9524, '11', 5, 6)
        check12 = checkpoint.Checkpoint(9764, '12')
        check13 = checkpoint.Checkpoint(3072, 'secret_mushroom', 360, 40, 12)

        self.check_point_group = pg.sprite.Group(check1,  check2,  check3,
                                                 check4,  check5,  check6,
                                                 check7,  check8,  check9,
                                                 check10, check11, check12,
                                                 check13)

    def game_mode(self):
        f = open("mode.txt", "r")
        if f.read() == "1": IsSingleGame = c.PLAYER1
        else: IsSingleGame = c.PLAYER2
        return(IsSingleGame)

    def setup_spritegroups(self):
        """Sprite groups created for convenience"""
        self.sprites_about_to_die_group = pg.sprite.Group()
        self.shell_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        self.ground_step_vaze_group = pg.sprite.Group(self.ground_group,
                                                      self.vaze_group,
                                                      self.step_group)
        
        if self.game_mode() == c.PLAYER1: self.mario_and_enemy_group = pg.sprite.Group(self.sanda, self.enemy_group)
        else: self.mario_and_enemy_group = pg.sprite.Group(self.sanda, self.adnas, self.enemy_group)


    def update(self, surface, keys, current_time):
        """Updates Entire level using states.  Called by the control object"""
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states(keys)
        self.check_if_time_out()
        self.blit_everything(surface)
        if self.game_mode() == c.PLAYER2: self.sound_manager.update(self.game_info, self.sanda, self.adnas)
        else: self.sound_manager.update(self.game_info, self.sanda, None)


    def handle_states(self, keys):
        """If the level is in a FROZEN state, only mario will update"""
        if self.state == c.FROZEN:
            self.update_during_transition_state(keys)
        elif self.state == c.NOT_FROZEN:
            self.update_all_sprites(keys)
        elif self.state == c.IN_CASTLE:
            self.update_while_in_castle()
        elif self.state == c.FLAG_AND_FIREWORKS:
            self.update_flag_and_fireworks()


    def update_during_transition_state(self, keys):
        """Updates mario in a transition state (like becoming big, small,
        or dies). Checks if he leaves the transition state or dies to
        change the level state back"""
        self.sanda.update(keys, self.game_info, self.powerup_group)
        if self.game_mode() == c.PLAYER2: self.adnas.update(keys, self.game_info, self.powerup_group)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.coin_box_group.update(self.game_info)
        self.flag_pole_group.update(self.game_info)
        self.check_if_sanda_in_transition_state()
        if self.game_mode() == c.PLAYER2: self.check_if_adnas_in_transition_state()
        self.check_flag()
        self.check_for_sanda_death()
        if self.game_mode() == c.PLAYER2: self.check_for_adnas_death()
        if self.game_mode() == c.PLAYER2: self.overhead_info_display.update(self.game_info, self.sanda, self.adnas)
        else: self.overhead_info_display.update(self.game_info, self.sanda, None)


    def check_if_sanda_in_transition_state(self):
        """If Sanda is in a transition state, the level will be in a FREEZE
        state"""
        if self.sanda.in_transition_state:
            self.game_info[c.LEVEL_STATE] = self.state = c.FROZEN
        elif self.sanda.in_transition_state == False:
            if self.state == c.FROZEN:
                self.game_info[c.LEVEL_STATE] = self.state = c.NOT_FROZEN


    def check_if_adnas_in_transition_state(self):
        """If Adnas is in a transition state, the level will be in a FREEZE
        state"""
        if self.adnas.in_transition_state:
            self.game_info[c.LEVEL_STATE] = self.state = c.FROZEN
        elif self.adnas.in_transition_state == False:
            if self.state == c.FROZEN:
                self.game_info[c.LEVEL_STATE] = self.state = c.NOT_FROZEN


    def update_all_sprites(self, keys):
        """Updates the location of all sprites on the screen."""
        self.sanda.update(keys, self.game_info, self.powerup_group)
        if self.game_mode() == c.PLAYER2: self.adnas.update(keys, self.game_info, self.powerup_group)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.flag_pole_group.update()
        self.check_points_check()
        self.enemy_group.update(self.game_info)
        self.sprites_about_to_die_group.update(self.game_info, self.viewport)
        self.shell_group.update(self.game_info)
        self.brick_group.update()
        self.coin_box_group.update(self.game_info)
        self.powerup_group.update(self.game_info, self.viewport)
        self.coin_group.update(self.game_info, self.viewport)
        self.brick_pieces_group.update()
        self.adjust_sprite_positions()
        self.check_if_sanda_in_transition_state()
        self.check_for_sanda_death()
        if self.game_mode() == c.PLAYER2:
            self.check_if_adnas_in_transition_state()
            self.check_for_adnas_death()
            self.overhead_info_display.update(self.game_info, self.sanda, self.adnas)
        else: self.overhead_info_display.update(self.game_info, self.sanda, None)
        self.update_viewport()


    def check_points_check(self):
        """Detect if checkpoint collision occurs, delete checkpoint,
        add enemies to self.enemy_group"""
        checkpoint = []
        checkpoint.append(pg.sprite.spritecollideany(self.sanda, self.check_point_group))
        if self.game_mode() == c.PLAYER2: checkpoint.append(pg.sprite.spritecollideany(self.adnas, self.check_point_group))
        for i in checkpoint:
            n=0
            if checkpoint[n]:
                checkpoint[n].kill()

                for i in range(1,11):
                    if checkpoint[n].name == str(i):
                        for index, enemy in enumerate(self.enemy_group_list[i -1]):
                            enemy.rect.x = self.viewport.right + (index * 60)
                        self.enemy_group.add(self.enemy_group_list[i-1])

                if checkpoint[n].name == '11':
                    self.sanda.state = c.FLAGPOLE
                    if self.game_mode() == c.PLAYER2: self.adnas.state = c.FLAGPOLE
                    self.sanda.invincible = False
                    if self.game_mode() == c.PLAYER2: self.adnas.invincible = False
                    if n == 0:
                        self.sanda.flag_pole_right = checkpoint[n].rect.right
                        if self.sanda.rect.bottom < self.flag.rect.y:
                            self.sanda.rect.bottom = self.flag.rect.y
                    elif n == 1:
                        self.adnas.flag_pole_right = checkpoint[n].rect.right
                        if self.adnas.rect.bottom < self.flag.rect.y:
                            self.adnas.rect.bottom = self.flag.rect.y
                    self.flag.state = c.SLIDE_DOWN
                    self.create_flag_points(n)

                elif checkpoint[n].name == '12':
                    self.state = c.IN_CASTLE
                    self.sanda.kill()
                    self.sanda.state == c.STAND
                    self.sanda.in_castle = True
                    if self.game_mode() == c.PLAYER2:
                        self.adnas.kill()
                        self.adnas.state == c.STAND
                        self.adnas.in_castle = True
                    self.overhead_info_display.state = c.FAST_COUNT_DOWN


                elif checkpoint[n].name == 'secret_mushroom' and self.sanda.y_vel < 0:
                    mushroom_box = coin_box.Coin_box(checkpoint[n].rect.x,
                                        checkpoint[n].rect.bottom - 40,
                                        '1up_mushroom',
                                        self.powerup_group)
                    mushroom_box.start_bump(self.moving_score_list)
                    self.coin_box_group.add(mushroom_box)

                    self.sanda.y_vel = 7
                    self.sanda.rect.y = mushroom_box.rect.bottom
                    self.sanda.state = c.FALL


                elif checkpoint[n].name == 'secret_mushroom' and self.adnas.y_vel < 0 and self.game_mode() == c.PLAYER2:
                    mushroom_box = coin_box.Coin_box(checkpoint[n].rect.x,
                                        checkpoint[n].rect.bottom - 40,
                                        '1up_mushroom',
                                        self.powerup_group)
                    mushroom_box.start_bump(self.moving_score_list)
                    self.coin_box_group.add(mushroom_box)

                    self.adnas.y_vel = 7
                    self.adnas.rect.y = mushroom_box.rect.bottom
                    self.adnas.state = c.FALL

                self.mario_and_enemy_group.add(self.enemy_group)
            n+=1


    def create_flag_points(self, number):
        """Creates the points that appear when Mario touches the
        flag pole"""
        x = 9524
        y = c.GROUND_HEIGHT - 60
        sanda_bottom = self.sanda.rect.bottom
        if self.game_mode() == c.PLAYER2: adnas_bottom = self.adnas.rect.bottom
        if number == 0:
            if sanda_bottom > (c.GROUND_HEIGHT - 48 - 48):
                self.flag_score = score.Score(x, y, 100, True)
                self.flag_score_total = 100
            elif sanda_bottom > (c.GROUND_HEIGHT - 48 - 192):
                self.flag_score = score.Score(x, y, 400, True)
                self.flag_score_total = 400
            elif sanda_bottom > (c.GROUND_HEIGHT - 48 - 288):
                self.flag_score = score.Score(x, y, 800, True)
                self.flag_score_total = 800
            elif sanda_bottom > (c.GROUND_HEIGHT - 48 - 432):
                self.flag_score = score.Score(x, y, 2000, True)
                self.flag_score_total = 2000
            else:
                self.flag_score = score.Score(x, y, 5000, True)
                self.flag_score_total = 5000
        elif number == 1:
            if adnas_bottom > (c.GROUND_HEIGHT - 48 - 48):
                self.flag_score = score.Score(x, y, 100, True)
                self.flag_score_total = 100
            elif adnas_bottom > (c.GROUND_HEIGHT - 48 - 192):
                self.flag_score = score.Score(x, y, 400, True)
                self.flag_score_total = 400
            elif adnas_bottom > (c.GROUND_HEIGHT - 48 - 288):
                self.flag_score = score.Score(x, y, 800, True)
                self.flag_score_total = 800
            elif adnas_bottom > (c.GROUND_HEIGHT - 48 - 432):
                self.flag_score = score.Score(x, y, 2000, True)
                self.flag_score_total = 2000
            else:
                self.flag_score = score.Score(x, y, 5000, True)
                self.flag_score_total = 5000


    def adjust_sprite_positions(self):
        """Adjusts sprites by their x and y velocities and collisions"""
        self.adjust_sanda_position()
        if self.game_mode() == c.PLAYER2: self.adjust_adnas_position()
        self.adjust_enemy_position()
        self.adjust_shell_position()
        self.adjust_powerup_position()


    def adjust_sanda_position(self):
        """Adjusts Sanda's position based on his x, y velocities and
        potential collisions"""
        self.last_x_position = self.sanda.rect.right
        self.sanda.rect.x += round(self.sanda.x_vel)
        self.check_sanda_x_collisions()

        if self.sanda.in_transition_state == False:
            self.sanda.rect.y += round(self.sanda.y_vel)
            self.check_sanda_y_collisions()

        if self.sanda.rect.x < (self.viewport.x + 5):
            self.sanda.rect.x = (self.viewport.x + 5)

    def adjust_adnas_position(self):
        """Adjusts Sanda's position based on his x, y velocities and
        potential collisions"""
        self.last_x_position = self.adnas.rect.right
        self.adnas.rect.x += round(self.adnas.x_vel)
        self.check_adnas_x_collisions()

        if self.adnas.in_transition_state == False:
            self.adnas.rect.y += round(self.adnas.y_vel)
            self.check_adnas_y_collisions()

        if self.adnas.rect.x < (self.viewport.x + 5):
            self.adnas.rect.x = (self.viewport.x + 5)


    def check_sanda_x_collisions(self):
        """Check for collisions after Mario is moved on the x axis"""
        collider = pg.sprite.spritecollideany(self.sanda, self.ground_step_vaze_group)
        coin_box = pg.sprite.spritecollideany(self.sanda, self.coin_box_group)
        brick = pg.sprite.spritecollideany(self.sanda, self.brick_group)
        enemy = pg.sprite.spritecollideany(self.sanda, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.sanda, self.shell_group)
        powerup = pg.sprite.spritecollideany(self.sanda, self.powerup_group)

        if coin_box: self.adjust_sanda_for_x_collisions(coin_box)
        elif brick: self.adjust_sanda_for_x_collisions(brick)
        elif collider: self.adjust_sanda_for_x_collisions(collider)

        elif enemy:
            if self.sanda.invincible:
                setup.SFX['kick'].play()
                self.game_info[c.SCORE] += 100
                self.moving_score_list.append(score.Score(self.sanda.rect.right - self.viewport.x, self.sanda.rect.y, 100))
                enemy.kill()
                enemy.start_death_jump(c.RIGHT)
                self.sprites_about_to_die_group.add(enemy)
            elif self.sanda.big:
                #setup.SFX['pipe'].play()
                self.sanda.fire = False
                self.sanda.y_vel = -1
                self.sanda.start_death_jump(self.game_info)
            elif self.sanda.hurt_invincible: pass
            else:
                self.sanda.start_death_jump(self.game_info)
                self.state = c.FROZEN

        elif shell: self.adjust_sanda_for_x_shell_collisions(shell)

        elif powerup:
            if powerup.name == c.SCARAB:
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append(score.Score(self.sanda.rect.centerx - self.viewport.x, self.sanda.rect.y, 1000))
                self.sanda.invincible = True
                self.sanda.invincible_start_timer = self.current_time
            elif powerup.name == c.LIFE_MUSHROOM:
                self.moving_score_list.append(
                    score.Score(powerup.rect.right - self.viewport.x, powerup.rect.y, c.ONEUP))
                self.game_info[c.SANDA_LIVES] += 1
                setup.SFX['one_up'].play()

            powerup.kill()


    def check_adnas_x_collisions(self):
        """Check for collisions after Mario is moved on the x axis"""
        collider = pg.sprite.spritecollideany(self.adnas, self.ground_step_vaze_group)
        coin_box = pg.sprite.spritecollideany(self.adnas, self.coin_box_group)
        brick = pg.sprite.spritecollideany(self.adnas, self.brick_group)
        enemy = pg.sprite.spritecollideany(self.adnas, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.adnas, self.shell_group)
        powerup = pg.sprite.spritecollideany(self.adnas, self.powerup_group)

        if coin_box: self.adjust_adnas_for_x_collisions(coin_box)
        elif brick: self.adjust_adnas_for_x_collisions(brick)
        elif collider: self.adjust_adnas_for_x_collisions(collider)

        elif enemy:
            if self.adnas.invincible:
                setup.SFX['kick'].play()
                self.game_info[c.SCORE] += 100
                self.moving_score_list.append(score.Score(self.adnas.rect.right - self.viewport.x, self.adnas.rect.y, 100))
                enemy.kill()
                enemy.start_death_jump(c.RIGHT)
                self.sprites_about_to_die_group.add(enemy)
            elif self.adnas.big:
                #setup.SFX['pipe'].play()
                self.adnas.fire = False
                self.adnas.y_vel = -1
                self.adnas.start_death_jump(self.game_info)
            elif self.adnas.hurt_invincible: pass
            else:
                self.adnas.start_death_jump(self.game_info)
                self.state = c.FROZEN

        elif shell:
            self.adjust_sanda_for_x_shell_collisions(shell)

        elif powerup:
            if powerup.name == c.SCARAB:
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append( score.Score(self.sanda.rect.centerx - self.viewport.x, self.sanda.rect.y, 1000))
                self.sanda.invincible = True
                self.sanda.invincible_start_timer = self.current_time
            elif powerup.name == c.LIFE_MUSHROOM:
                self.moving_score_list.append(score.Score(powerup.rect.right - self.viewport.x, powerup.rect.y, c.ONEUP))
                self.game_info[c.ADNAS_LIVES] += 1
                setup.SFX['one_up'].play()

            powerup.kill()


    def adjust_sanda_for_x_collisions(self, collider):
        """Puts Sanda flush next to the collider after moving on the x axis"""
        if self.sanda.rect.x < collider.rect.x:
            self.sanda.rect.right = collider.rect.left
        else:
            self.sanda.rect.left = collider.rect.right

        self.sanda.x_vel = 0


    def adjust_adnas_for_x_collisions(self, collider):
        """Puts Adnas flush next to the collider after moving on the x axis"""
        if self.adnas.rect.x < collider.rect.x:
            self.adnas.rect.right = collider.rect.left
        else:
            self.adnas.rect.left = collider.rect.right

        self.adnas.x_vel = 0


    def adjust_sanda_for_x_shell_collisions(self, shell):
        """Deals with Sanda if he hits a shell moving on the x axis"""
        if shell.state == c.JUMPED_ON:
            if self.sanda.rect.x < shell.rect.x:
                self.game_info[c.SCORE] += 400
                self.moving_score_list.append(
                    score.Score(shell.rect.centerx - self.viewport.x,
                                shell.rect.y,
                                400))
                self.sanda.rect.right = shell.rect.left
                shell.direction = c.RIGHT
                shell.x_vel = 5
                shell.rect.x += 5

            else:
                self.sanda.rect.left = shell.rect.right
                shell.direction = c.LEFT
                shell.x_vel = -5
                shell.rect.x += -5

            shell.state = c.SHELL_SLIDE

        elif shell.state == c.SHELL_SLIDE:
            if self.sanda.big and not self.sanda.invincible:
                self.sanda.state = c.BIG_TO_SMALL
            elif self.sanda.invincible:
                self.game_info[c.SANDA_SCORE] += 200
                self.moving_score_list.append(
                    score.Score(shell.rect.right - self.viewport.x,
                                shell.rect.y, 200))
                shell.kill()
                self.sprites_about_to_die_group.add(shell)
                shell.start_death_jump(c.RIGHT)
            else:
                if not self.sanda.hurt_invincible and not self.sanda.invincible:
                    self.state = c.FROZEN
                    self.sanda.start_death_jump(self.game_info)


    def check_sanda_y_collisions(self):
        """Checks for collisions when Sanda moves along the y-axis"""
        ground_step_or_pipe = pg.sprite.spritecollideany(self.sanda, self.ground_step_vaze_group)
        enemy = pg.sprite.spritecollideany(self.sanda, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.sanda, self.shell_group)
        brick = pg.sprite.spritecollideany(self.sanda, self.brick_group)
        coin_box = pg.sprite.spritecollideany(self.sanda, self.coin_box_group)
        powerup = pg.sprite.spritecollideany(self.sanda, self.powerup_group)

        brick, coin_box = self.prevent_collision_conflict(brick, coin_box)

        if coin_box: self.adjust_sanda_for_y_coin_box_collisions(coin_box)
        elif brick: self.adjust_sanda_for_y_brick_collisions(brick)
        elif ground_step_or_pipe: self.adjust_sanda_for_y_ground_vaze_collisions(ground_step_or_pipe)
        elif enemy:
            if self.sanda.invincible:
                setup.SFX['kick'].play()
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                enemy.start_death_jump(c.RIGHT)
            else: self.adjust_sanda_for_y_enemy_collisions(enemy)
                #if self.game_mode() == c.PLAYER2: self.adjust_adnas_for_y_enemy_collisions(enemy)
        elif shell: self.adjust_sanda_for_y_shell_collisions(shell)
            #if self.game_mode() == c.PLAYER2: self.adjust_adnas_for_y_shell_collisions(shell)

        elif powerup:
            if powerup.name == c.SCARAB:
                setup.SFX['powerup'].play()
                powerup.kill()
                self.sanda.invincible = True
                self.sanda.invincible_start_timer = self.current_time

        self.test_if_sanda_is_falling()


    def adjust_adnas_for_x_shell_collisions(self, shell):
        """Deals with Adnas if he hits a shell moving on the x axis"""
        if shell.state == c.JUMPED_ON:
            if self.adnas.rect.x < shell.rect.x:
                self.game_info[c.SCORE] += 400
                self.moving_score_list.append(
                    score.Score(shell.rect.centerx - self.viewport.x,
                                shell.rect.y,
                                400))
                self.adnas.rect.right = shell.rect.left
                shell.direction = c.RIGHT
                shell.x_vel = 5
                shell.rect.x += 5

            else:
                self.adnas.rect.left = shell.rect.right
                shell.direction = c.LEFT
                shell.x_vel = -5
                shell.rect.x += -5

            shell.state = c.SHELL_SLIDE

        elif shell.state == c.SHELL_SLIDE:
            if self.adnas.big and not self.adnas.invincible:
                self.adnas.state = c.BIG_TO_SMALL
            elif self.adnas.invincible:
                self.game_info[c.SCORE] += 200
                self.moving_score_list.append(
                    score.Score(shell.rect.right - self.viewport.x,
                                shell.rect.y, 200))
                shell.kill()
                self.sprites_about_to_die_group.add(shell)
                shell.start_death_jump(c.RIGHT)
            else:
                if not self.adnas.hurt_invincible and not self.adnas.invincible:
                    self.state = c.FROZEN
                    self.adnas.start_death_jump(self.game_info)


    def check_adnas_y_collisions(self):
        """Checks for collisions when Adnas moves along the y-axis"""
        ground_step_or_pipe = pg.sprite.spritecollideany(self.adnas, self.ground_step_vaze_group)
        enemy = pg.sprite.spritecollideany(self.adnas, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.adnas, self.shell_group)
        brick = pg.sprite.spritecollideany(self.adnas, self.brick_group)
        coin_box = pg.sprite.spritecollideany(self.adnas, self.coin_box_group)
        powerup = pg.sprite.spritecollideany(self.adnas, self.powerup_group)

        brick, coin_box = self.prevent_collision_conflict(brick, coin_box)

        if coin_box: self.adjust_adnas_for_y_coin_box_collisions(coin_box)
        elif brick: self.adjust_adnas_for_y_brick_collisions(brick)
        elif ground_step_or_pipe: self.adjust_adnas_for_y_ground_vaze_collisions(ground_step_or_pipe)
        elif enemy:
            if self.adnas.invincible:
                setup.SFX['kick'].play()
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                enemy.start_death_jump(c.RIGHT)
            else:
                self.adjust_adnas_for_y_enemy_collisions(enemy)
        elif shell: self.adjust_adnas_for_y_shell_collisions(shell)
        elif powerup:
            if powerup.name == c.SCARAB:
                setup.SFX['powerup'].play()
                powerup.kill()
                self.adnas.invincible = True
                self.adnas.invincible_start_timer = self.current_time

        self.test_if_adnas_is_falling()


    def prevent_collision_conflict(self, obstacle1, obstacle2):
        """Allows collisions only for the item closest to marios centerx"""
        if obstacle1 and obstacle2:
            obstacle1_distance = self.sanda.rect.centerx - obstacle1.rect.centerx
            if obstacle1_distance < 0:
                obstacle1_distance *= -1
            if self.game_mode() == c.PLAYER2:
                obstacle2_distance = self.adnas.rect.centerx - obstacle2.rect.centerx
                if obstacle2_distance < 0:
                    obstacle2_distance *= -1

                if obstacle1_distance < obstacle2_distance:
                    obstacle2 = False
                else:
                    obstacle1 = False
            if obstacle2 != False: obstacle1 = False

        return obstacle1, obstacle2


    def adjust_sanda_for_y_coin_box_collisions(self, coin_box):
        """Sanda collisions with coin boxes on the y-axis"""
        if self.sanda.rect.y > coin_box.rect.y:
            if coin_box.state == c.RESTING:
                if coin_box.contents == c.COIN:
                    self.game_info[c.SCORE] += 200
                    coin_box.start_bump(self.moving_score_list)
                    if coin_box.contents == c.COIN:
                        self.game_info[c.COIN_TOTAL] += 1
                else:
                    coin_box.start_bump(self.moving_score_list)

            elif coin_box.state == c.OPENED:
                pass
            setup.SFX['bump'].play()
            self.sanda.y_vel = 7
            self.sanda.rect.y = coin_box.rect.bottom
            self.sanda.state = c.FALL
        else:
            self.sanda.y_vel = 0
            self.sanda.rect.bottom = coin_box.rect.top
            self.sanda.state = c.WALK


    def adjust_adnas_for_y_coin_box_collisions(self, coin_box):
        """Adnas collisions with coin boxes on the y-axis"""
        if self.adnas.rect.y > coin_box.rect.y:
            if coin_box.state == c.RESTING:
                if coin_box.contents == c.COIN:
                    self.game_info[c.SCORE] += 200
                    coin_box.start_bump(self.moving_score_list)
                    if coin_box.contents == c.COIN:
                        self.game_info[c.COIN_TOTAL] += 1
                else:
                    coin_box.start_bump(self.moving_score_list)

            elif coin_box.state == c.OPENED:
                pass
            setup.SFX['bump'].play()
            self.adnas.y_vel = 7
            self.adnas.rect.y = coin_box.rect.bottom
            self.adnas.state = c.FALL
        else:
            self.adnas.y_vel = 0
            self.adnas.rect.bottom = coin_box.rect.top
            self.adnas.state = c.WALK


    def adjust_sanda_for_y_brick_collisions(self, brick):
        """Sanda collisions with bricks on the y-axis"""
        if self.sanda.rect.y > brick.rect.y:
            if brick.state == c.RESTING:
                if self.sanda.invincible and brick.contents is None:
                    setup.SFX['brick_smash'].play()
                    self.check_if_enemy_on_brick(brick)
                    brick.kill()
                    self.brick_pieces_group.add(
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y - (brick.rect.height/2),
                                               -2, -12),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y - (brick.rect.height/2),
                                               2, -12),
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y,
                                               -2, -6),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y,
                                               2, -6))
                else:
                    setup.SFX['bump'].play()
                    if brick.coin_total > 0:
                        self.game_info[c.COIN_TOTAL] += 1
                        self.game_info[c.SCORE] += 200
                    self.check_if_enemy_on_brick(brick)
                    brick.start_bump(self.moving_score_list)
            elif brick.state == c.OPENED:
                setup.SFX['bump'].play()
            self.sanda.y_vel = 7
            self.sanda.rect.y = brick.rect.bottom
            self.sanda.state = c.FALL

        else:
            self.sanda.y_vel = 0
            self.sanda.rect.bottom = brick.rect.top
            self.sanda.state = c.WALK


    def adjust_adnas_for_y_brick_collisions(self, brick):
        """Adnas collisions with bricks on the y-axis"""
        if self.adnas.rect.y > brick.rect.y:
            if brick.state == c.RESTING:
                if self.adnas.invincible and brick.contents is None:
                    setup.SFX['brick_smash'].play()
                    self.check_if_enemy_on_brick(brick)
                    brick.kill()
                    self.brick_pieces_group.add(
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y - (brick.rect.height/2),
                                               -2, -12),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y - (brick.rect.height/2),
                                               2, -12),
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y,
                                               -2, -6),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y,
                                               2, -6))
                else:
                    setup.SFX['bump'].play()
                    if brick.coin_total > 0:
                        self.game_info[c.COIN_TOTAL] += 1
                        self.game_info[c.SCORE] += 200
                    self.check_if_enemy_on_brick(brick)
                    brick.start_bump(self.moving_score_list)
            elif brick.state == c.OPENED:
                setup.SFX['bump'].play()
            self.adnas.y_vel = 7
            self.adnas.rect.y = brick.rect.bottom
            self.adnas.state = c.FALL

        else:
            self.adnas.y_vel = 0
            self.adnas.rect.bottom = brick.rect.top
            self.adnas.state = c.WALK


    def check_if_enemy_on_brick(self, brick):
        """Kills enemy if on a bumped or broken brick"""
        brick.rect.y -= 5

        enemy = pg.sprite.spritecollideany(brick, self.enemy_group)

        if enemy:
            setup.SFX['kick'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y,
                            100))
            enemy.kill()
            self.sprites_about_to_die_group.add(enemy)
            if self.mario.rect.centerx > brick.rect.centerx:
                enemy.start_death_jump('right')
            else:
                enemy.start_death_jump('left')

        brick.rect.y += 5


    def adjust_sanda_for_y_ground_vaze_collisions(self, collider):
        """Sanda collisions with vazes on the y-axis"""
        if collider.rect.bottom > self.sanda.rect.bottom:
            self.sanda.y_vel = 0
            self.sanda.rect.bottom = collider.rect.top
            if self.sanda.state == c.END_OF_LEVEL_FALL:
                self.sanda.state = c.WALKING_TO_CASTLE
            else:
                self.sanda.state = c.WALK
        elif collider.rect.top < self.sanda.rect.top:
            self.sanda.y_vel = 7
            self.sanda.rect.top = collider.rect.bottom
            self.sanda.state = c.FALL


    def adjust_adnas_for_y_ground_vaze_collisions(self, collider):
        """Adnas collisions with vazes on the y-axis"""
        if collider.rect.bottom > self.adnas.rect.bottom:
            self.adnas.y_vel = 0
            self.adnas.rect.bottom = collider.rect.top
            if self.adnas.state == c.END_OF_LEVEL_FALL:
                self.adnas.state = c.WALKING_TO_CASTLE
            else:
                self.adnas.state = c.WALK
        elif collider.rect.top < self.adnas.rect.top:
            self.adnas.y_vel = 7
            self.adnas.rect.top = collider.rect.bottom
            self.adnas.state = c.FALL


    def test_if_sanda_is_falling(self):
        """Changes Sanda to a FALL state if more than a pixel above a pipe,
        ground, step or box"""
        self.sanda.rect.y += 1
        test_collide_group = pg.sprite.Group(self.ground_step_vaze_group,
                                                 self.brick_group,
                                                 self.coin_box_group)

        if pg.sprite.spritecollideany(self.sanda, test_collide_group) is None:
            if self.sanda.state != c.JUMP \
                and self.sanda.state != c.DEATH_JUMP \
                and self.sanda.state != c.SMALL_TO_BIG \
                and self.sanda.state != c.BIG_TO_FIRE \
                and self.sanda.state != c.BIG_TO_SMALL \
                and self.sanda.state != c.FLAGPOLE \
                and self.sanda.state != c.WALKING_TO_CASTLE \
                and self.sanda.state != c.END_OF_LEVEL_FALL:
                self.sanda.state = c.FALL
            elif self.sanda.state == c.WALKING_TO_CASTLE or \
                self.sanda.state == c.END_OF_LEVEL_FALL:
                self.sanda.state = c.END_OF_LEVEL_FALL

        self.sanda.rect.y -= 1


    def test_if_adnas_is_falling(self):
        """Changes Adnas to a FALL state if more than a pixel above a pipe,
        ground, step or box"""
        self.adnas.rect.y += 1
        test_collide_group = pg.sprite.Group(self.ground_step_vaze_group,
                                                 self.brick_group,
                                                 self.coin_box_group)

        if pg.sprite.spritecollideany(self.adnas, test_collide_group) is None:
            if self.adnas.state != c.JUMP \
                and self.adnas.state != c.DEATH_JUMP \
                and self.adnas.state != c.SMALL_TO_BIG \
                and self.adnas.state != c.BIG_TO_FIRE \
                and self.adnas.state != c.BIG_TO_SMALL \
                and self.adnas.state != c.FLAGPOLE \
                and self.adnas.state != c.WALKING_TO_CASTLE \
                and self.adnas.state != c.END_OF_LEVEL_FALL:
                self.adnas.state = c.FALL
            elif self.adnas.state == c.WALKING_TO_CASTLE or \
                self.adnas.state == c.END_OF_LEVEL_FALL:
                self.adnas.state = c.END_OF_LEVEL_FALL

        self.adnas.rect.y -= 1


    def adjust_sanda_for_y_enemy_collisions(self, enemy):
        """Sanda collisions with all enemies on the y-axis"""
        if self.sanda.y_vel > 0:
            setup.SFX['stomp'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.state = c.JUMPED_ON
            enemy.kill()
            if enemy.name == c.GOOMBA:
                enemy.death_timer = self.current_time
                self.sprites_about_to_die_group.add(enemy)
            elif enemy.name == c.KOOPA:
                self.shell_group.add(enemy)

            self.sanda.rect.bottom = enemy.rect.top
            self.sanda.state = c.JUMP
            self.sanda.y_vel = -7


    def adjust_adnas_for_y_enemy_collisions(self, enemy):
        """Adnas collisions with all enemies on the y-axis"""
        if self.adnas.y_vel > 0:
            setup.SFX['stomp'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.state = c.JUMPED_ON
            enemy.kill()
            if enemy.name == c.GOOMBA:
                enemy.death_timer = self.current_time
                self.sprites_about_to_die_group.add(enemy)
            elif enemy.name == c.KOOPA:
                self.shell_group.add(enemy)

            self.adnas.rect.bottom = enemy.rect.top
            self.adnas.state = c.JUMP
            self.adnas.y_vel = -7


    def adjust_sanda_for_y_shell_collisions(self, shell):
        """Sanda collisions with Koopas in their shells on the y axis"""
        if self.sanda.y_vel > 0:
            self.game_info[c.SCORE] += 400
            self.moving_score_list.append(
                score.Score(self.sanda.rect.centerx - self.viewport.x,
                            self.sanda.rect.y, 400))
            if shell.state == c.JUMPED_ON:
                setup.SFX['kick'].play()
                shell.state = c.SHELL_SLIDE
                if self.sanda.rect.centerx < shell.rect.centerx:
                    shell.direction = c.RIGHT
                    shell.rect.left = self.sanda.rect.right + 5
                else:
                    shell.direction = c.LEFT
                    shell.rect.right = self.sanda.rect.left - 5
            else:
                shell.state = c.JUMPED_ON


    def adjust_adnas_for_y_shell_collisions(self, shell):
        """Adnas collisions with Koopas in their shells on the y axis"""
        if self.adnas.y_vel > 0:
            self.game_info[c.SCORE] += 400
            self.moving_score_list.append(
                score.Score(self.adnas.rect.centerx - self.viewport.x,
                            self.adnas.rect.y, 400))
            if shell.state == c.JUMPED_ON:
                setup.SFX['kick'].play()
                shell.state = c.SHELL_SLIDE
                if self.adnas.rect.centerx < shell.rect.centerx:
                    shell.direction = c.RIGHT
                    shell.rect.left = self.adnas.rect.right + 5
                else:
                    shell.direction = c.LEFT
                    shell.rect.right = self.adnas.rect.left - 5
            else:
                shell.state = c.JUMPED_ON


    def adjust_enemy_position(self):
        """Moves all enemies along the x, y axes and check for collisions"""
        for enemy in self.enemy_group:
            enemy.rect.x += enemy.x_vel
            self.check_enemy_x_collisions(enemy)

            enemy.rect.y += enemy.y_vel
            self.check_enemy_y_collisions(enemy)
            self.delete_if_off_screen(enemy)


    def check_enemy_x_collisions(self, enemy):
        """Enemy collisions along the x axis.  Removes enemy from enemy group
        in order to check against all other enemies then adds it back."""
        enemy.kill()

        collider = pg.sprite.spritecollideany(enemy, self.ground_step_vaze_group)
        enemy_collider = pg.sprite.spritecollideany(enemy, self.enemy_group)

        if collider:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = collider.rect.left
                enemy.direction = c.LEFT
                enemy.x_vel = -2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = collider.rect.right
                enemy.direction = c.RIGHT
                enemy.x_vel = 2


        elif enemy_collider:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = enemy_collider.rect.left
                enemy.direction = c.LEFT
                enemy_collider.direction = c.RIGHT
                enemy.x_vel = -2
                enemy_collider.x_vel = 2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = enemy_collider.rect.right
                enemy.direction = c.RIGHT
                enemy_collider.direction = c.LEFT
                enemy.x_vel = 2
                enemy_collider.x_vel = -2

        self.enemy_group.add(enemy)
        self.mario_and_enemy_group.add(self.enemy_group)


    def check_enemy_y_collisions(self, enemy):
        """Enemy collisions on the y axis"""
        collider = pg.sprite.spritecollideany(enemy, self.ground_step_vaze_group)
        brick = pg.sprite.spritecollideany(enemy, self.brick_group)
        coin_box = pg.sprite.spritecollideany(enemy, self.coin_box_group)

        if collider:
            if enemy.rect.bottom > collider.rect.bottom:
                enemy.y_vel = 7
                enemy.rect.top = collider.rect.bottom
                enemy.state = c.FALL
            elif enemy.rect.bottom < collider.rect.bottom:

                enemy.y_vel = 0
                enemy.rect.bottom = collider.rect.top
                enemy.state = c.WALK

        elif brick:
            if brick.state == c.BUMPED:
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                if self.mario.rect.centerx > brick.rect.centerx:
                    enemy.start_death_jump('right')
                else:
                    enemy.start_death_jump('left')

            elif enemy.rect.x > brick.rect.x:
                enemy.y_vel = 7
                enemy.rect.top = brick.rect.bottom
                enemy.state = c.FALL
            else:
                enemy.y_vel = 0
                enemy.rect.bottom = brick.rect.top
                enemy.state = c.WALK

        elif coin_box:
            if coin_box.state == c.BUMPED:
                self.game_info[c.SCORE] += 100
                self.moving_score_list.append(
                    score.Score(enemy.rect.centerx - self.viewport.x,
                                enemy.rect.y, 100))
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                if self.mario.rect.centerx > coin_box.rect.centerx:
                    enemy.start_death_jump('right')
                else:
                    enemy.start_death_jump('left')

            elif enemy.rect.x > coin_box.rect.x:
                enemy.y_vel = 7
                enemy.rect.top = coin_box.rect.bottom
                enemy.state = c.FALL
            else:
                enemy.y_vel = 0
                enemy.rect.bottom = coin_box.rect.top
                enemy.state = c.WALK


        else:
            enemy.rect.y += 1
            test_group = pg.sprite.Group(self.ground_step_vaze_group,
                                         self.coin_box_group,
                                         self.brick_group)
            if pg.sprite.spritecollideany(enemy, test_group) is None:
                if enemy.state != c.JUMP:
                    enemy.state = c.FALL

            enemy.rect.y -= 1


    def adjust_shell_position(self):
        """Moves any koopa in a shell along the x, y axes and checks for
        collisions"""
        for shell in self.shell_group:
            shell.rect.x += shell.x_vel
            self.check_shell_x_collisions(shell)

            shell.rect.y += shell.y_vel
            self.check_shell_y_collisions(shell)
            self.delete_if_off_screen(shell)


    def check_shell_x_collisions(self, shell):
        """Shell collisions along the x axis"""
        collider = pg.sprite.spritecollideany(shell, self.ground_step_vaze_group)
        enemy = pg.sprite.spritecollideany(shell, self.enemy_group)

        if collider:
            setup.SFX['bump'].play()
            if shell.x_vel > 0:
                shell.direction = c.LEFT
                shell.rect.right = collider.rect.left
            else:
                shell.direction = c.RIGHT
                shell.rect.left = collider.rect.right

        if enemy:
            setup.SFX['kick'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.right - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.kill()
            self.sprites_about_to_die_group.add(enemy)
            enemy.start_death_jump(shell.direction)


    def check_shell_y_collisions(self, shell):
        """Shell collisions along the y axis"""
        collider = pg.sprite.spritecollideany(shell, self.ground_step_vaze_group)

        if collider:
            shell.y_vel = 0
            shell.rect.bottom = collider.rect.top
            shell.state = c.SHELL_SLIDE

        else:
            shell.rect.y += 1
            if pg.sprite.spritecollideany(shell, self.ground_step_vaze_group) is None:
                shell.state = c.FALL
            shell.rect.y -= 1


    def adjust_powerup_position(self):
        """Moves mushrooms, Scarab and fireballs along the x, y axes"""
        for powerup in self.powerup_group:
            if powerup.name == c.SCARAB:
                self.adjust_scarab_position(powerup)
            elif powerup.name == '1up_mushroom':
                self.adjust_mushroom_position(powerup)

    def adjust_mushroom_position(self, mushroom):
        """Moves mushroom along the x, y axes."""
        if mushroom.state != c.REVEAL:
            mushroom.rect.x += mushroom.x_vel
            self.check_mushroom_x_collisions(mushroom)

            mushroom.rect.y += mushroom.y_vel
            self.check_mushroom_y_collisions(mushroom)
            self.delete_if_off_screen(mushroom)

    def check_mushroom_x_collisions(self, mushroom):
        """Mushroom collisions along the x axis"""
        collider = pg.sprite.spritecollideany(mushroom, self.ground_step_vaze_group)
        brick = pg.sprite.spritecollideany(mushroom, self.brick_group)
        coin_box = pg.sprite.spritecollideany(mushroom, self.coin_box_group)

        if collider: self.adjust_mushroom_for_collision_x(mushroom, collider)
        elif brick: self.adjust_mushroom_for_collision_x(mushroom, brick)
        elif coin_box: self.adjust_mushroom_for_collision_x(mushroom, coin_box)


    def check_mushroom_y_collisions(self, mushroom):
        """Mushroom collisions along the y axis"""
        collider = pg.sprite.spritecollideany(mushroom, self.ground_step_vaze_group)
        brick = pg.sprite.spritecollideany(mushroom, self.brick_group)
        coin_box = pg.sprite.spritecollideany(mushroom, self.coin_box_group)

        if collider: self.adjust_mushroom_for_collision_y(mushroom, collider)
        elif brick: self.adjust_mushroom_for_collision_y(mushroom, brick)
        elif coin_box: self.adjust_mushroom_for_collision_y(mushroom, coin_box)
        else:
            self.check_if_falling(mushroom, self.ground_step_vaze_group)
            self.check_if_falling(mushroom, self.brick_group)
            self.check_if_falling(mushroom, self.coin_box_group)

    def adjust_mushroom_for_collision_x(self, item, collider):
        """Changes mushroom direction if collision along x axis"""
        if item.rect.x < collider.rect.x:
            item.rect.right = collider.rect.x
            item.direction = c.LEFT
        else:
            item.rect.x = collider.rect.right
            item.direction = c.RIGHT

    def adjust_mushroom_for_collision_y(self, item, collider):
        """Changes mushroom state to SLIDE after hitting ground from fall"""
        item.rect.bottom = collider.rect.y
        item.state = c.SLIDE
        item.y_vel = 0

    def adjust_scarab_position(self, Scarab):
        """Moves invincible Scarab along x, y axes and checks for collisions"""
        if Scarab.state == c.BOUNCE:
            Scarab.rect.x += Scarab.x_vel
            self.check_mushroom_x_collisions(Scarab)
            Scarab.rect.y += Scarab.y_vel
            self.check_Scarab_y_collisions(Scarab)
            Scarab.y_vel += Scarab.gravity
            self.delete_if_off_screen(Scarab)


    def check_Scarab_y_collisions(self, Scarab):
        """Invincible Scarab collisions along y axis"""
        collider = pg.sprite.spritecollideany(Scarab, self.ground_step_vaze_group)
        brick = pg.sprite.spritecollideany(Scarab, self.brick_group)
        coin_box = pg.sprite.spritecollideany(Scarab, self.coin_box_group)

        if collider: self.adjust_scarab_for_collision_y(Scarab, collider)
        elif brick: self.adjust_scarab_for_collision_y(Scarab, brick)
        elif coin_box: self.adjust_scarab_for_collision_y(Scarab, coin_box)


    def adjust_scarab_for_collision_y(self, Scarab, collider):
        """Allows for a Scarab bounce off the ground and on the bottom of a
        box"""
        if Scarab.rect.y > collider.rect.y:
            Scarab.rect.y = collider.rect.bottom
            Scarab.y_vel = 0
        else:
            Scarab.rect.bottom = collider.rect.top
            Scarab.start_bounce(-8)


    def check_if_falling(self, sprite, sprite_group):
        """Checks if sprite should enter a falling state"""
        sprite.rect.y += 1

        if pg.sprite.spritecollideany(sprite, sprite_group) is None:
            if sprite.state != c.JUMP:
                sprite.state = c.FALL

        sprite.rect.y -= 1


    def delete_if_off_screen(self, enemy):
        """Removes enemy from sprite groups if 500 pixels left off the screen,
         underneath the bottom of the screen, or right of the screen if shell"""
        if enemy.rect.x < (self.viewport.x - 300):
            enemy.kill()

        elif enemy.rect.y > (self.viewport.bottom):
            enemy.kill()

        elif enemy.state == c.SHELL_SLIDE:
            if enemy.rect.x > (self.viewport.right + 500):
                enemy.kill()


    def check_flag(self):
        """Adjusts mario's state when the flag is at the bottom"""
        if (self.flag.state == c.BOTTOM_OF_POLE
            and self.sanda.state == c.FLAGPOLE):
            self.sanda.set_state_to_bottom_of_pole()
        if self.game_mode() == c.PLAYER2:
            if (self.flag.state == c.BOTTOM_OF_POLE
            and self.adnas.state == c.FLAGPOLE):
                self.adnas.set_state_to_bottom_of_pole()


    def check_to_add_flag_score(self):
        """Adds flag score if at top"""
        if self.flag_score.y_vel == 0:
            self.game_info[c.SCORE] += self.flag_score_total
            self.flag_score_total = 0


    def check_for_sanda_death(self):
        """Restarts the level if Sanda is dead"""
        if self.sanda.rect.y > c.SCREEN_HEIGHT and not self.sanda.in_castle:
            self.sanda.dead = True
            self.sanda.x_vel = 0
            self.state = c.FROZEN
            self.game_info[c.SANDA_DEAD] = True

        if self.sanda.dead:
            self.play_death_song()

    def check_for_adnas_death(self):
        """Restarts the level if Adnas is dead"""
        if self.adnas.rect.y > c.SCREEN_HEIGHT and not self.adnas.in_castle:
            self.adnas.dead = True
            self.adnas.x_vel = 0
            self.state = c.FROZEN
            self.game_info[c.ADNAS_DEAD] = True

        if self.adnas.dead:
            self.play_death_song()


    def play_death_song(self):
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 3000:
            self.set_game_info_values()
            self.done = True


    def set_game_info_values(self):
        """sets the new game values after all player's death"""
        if self.sanda.dead:
            self.persist[c.SANDA_LIVES] -= 1
        if self.game_mode() == c.PLAYER2 and self.adnas.dead:
            self.persist[c.ADNAS_LIVES] -= 1

        if self.persist[c.SANDA_LIVES] == 0 or self.persist[c.ADNAS_LIVES] == 0:
            self.next = c.GAME_OVER
            self.game_info[c.CAMERA_START_X] = 0
        elif self.sanda.dead == False and not getattr(Level1, "self.adnas.dead", True):
            self.next = c.MAIN_MENU
            self.game_info[c.CAMERA_START_X] = 0
        elif self.overhead_info_display.time == 0:
            self.next = c.TIME_OUT
        else:
            if  (self.sanda.rect.x > 3670 and self.game_info[c.CAMERA_START_X]) == 0 or \
                (self.game_mode() == c.PLAYER2 and self.adnas.rect.x > 3670 and self.game_info[c.CAMERA_START_X]) == 0:
                self.game_info[c.CAMERA_START_X] = 3440
            self.next = c.LOAD_SCREEN


    def check_if_time_out(self):
        """Check if time has run down to 0"""
        if self.overhead_info_display.time <= 0 \
                and not self.sanda.dead \
                and not getattr(Level1, 'self.adnas.dead', True) \
                and not self.sanda.in_castle \
                and not self.adnas.in_castle:
            self.state = c.FROZEN
            self.mario.start_death_jump(self.game_info)


    def update_viewport(self):
        """Changes the view of the camera"""
        third = self.viewport.x + self.viewport.w//3
        sanda_center = self.sanda.rect.centerx
        sanda_right = self.sanda.rect.right

        if self.sanda.x_vel > 0 and sanda_center >= third:
            mult = 0.5 if sanda_right < self.viewport.centerx else 1
            new = self.viewport.x + mult * self.sanda.x_vel
            highest = self.level_rect.w - self.viewport.w
            self.viewport.x = min(highest, new)


    def update_while_in_castle(self):
        """Updates while Mario is in castle at the end of the level"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info)

        if self.overhead_info_display.state == c.END_OF_LEVEL:
            self.state = c.FLAG_AND_FIREWORKS
            self.flag_pole_group.add(castle_flag.Flag(8745, 322))


    def update_flag_and_fireworks(self):
        """Updates the level for the fireworks and castle flag"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info)
        self.flag_pole_group.update()

        self.end_game()


    def end_game(self):
        """End the game"""
        if self.flag_timer == 0:
            self.flag_timer = self.current_time
        elif (self.current_time - self.flag_timer) > 2000:
            self.set_game_info_values()
            self.next = c.GAME_OVER
            self.sound_manager.stop_music()
            self.done = True


    def blit_everything(self, surface):
        """Blit all sprites to the main surface"""
        self.level.blit(self.background, self.viewport, self.viewport)
        if self.flag_score:
            self.flag_score.draw(self.level)
        self.powerup_group.draw(self.level)
        self.coin_group.draw(self.level)
        self.brick_group.draw(self.level)
        self.coin_box_group.draw(self.level)
        self.sprites_about_to_die_group.draw(self.level)
        self.shell_group.draw(self.level)
        #self.check_point_group.draw(self.level)
        self.brick_pieces_group.draw(self.level)
        self.flag_pole_group.draw(self.level)
        self.mario_and_enemy_group.draw(self.level)

        surface.blit(self.level, (0,0), self.viewport)
        self.overhead_info_display.draw(surface)
        for score in self.moving_score_list:
            score.draw(surface)