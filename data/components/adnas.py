__author__ = 'justinarmstrong'

import pygame as pg
from .. import setup, tools
from .. import constants as c
from . import powerups

class Adnas(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprite_sheet = setup.GFX['characters']
        self.setup_timers()
        self.setup_state_booleans()
        self.setup_forces()
        self.setup_counters()
        self.load_images_from_sheet()
        self.state = c.WALK
        self.image = self.right_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.key_timer = 0

    def setup_timers(self):
        """Sets up timers for animations"""
        self.walking_timer = 0
        self.invincible_animation_timer = 0
        self.invincible_start_timer = 0
        self.fire_transition_timer = 0
        self.death_timer = 0
        self.transition_timer = 0
        self.last_fireball_time = 0
        self.hurt_invisible_timer = 0
        self.hurt_invisible_timer2 = 0
        self.flag_pole_timer = 0

    def setup_state_booleans(self):
        """Sets up booleans that affect Adnas's behavior"""
        self.facing_right = True
        self.allow_jump = True
        self.dead = False
        self.invincible = False
        self.big = True
        self.fire = False
        self.allow_fireball = True
        self.in_transition_state = False
        self.hurt_invincible = False
        self.in_castle = False
        self.crouching = False
        self.losing_invincibility = False

    def setup_forces(self):
        """Sets up forces that affect Adnas's velocity"""
        self.x_vel = 0
        self.y_vel = 0
        self.max_x_vel = c.MAX_WALK_SPEED
        self.max_y_vel = c.MAX_Y_VEL
        self.x_accel = c.WALK_ACCEL
        self.jump_vel = c.JUMP_VEL
        self.gravity = c.GRAVITY

    def setup_counters(self):
        """These keep track of various total for important values"""
        self.frame_index = 0
        self.invincible_index = 0
        self.fire_transition_index = 0
        self.flag_pole_right = 0

    def load_images_from_sheet(self):
        """Extracts Mario images from his sprite sheet and assigns
        them to appropriate lists"""
        self.right_frames = []
        self.left_frames = []
        self.right_small_normal_frames = []
        self.left_small_normal_frames = []
        self.right_big_normal_frames = []
        self.left_big_normal_frames = []

        #Images for normal small Sanda

        self.right_small_normal_frames.append(
            self.get_image(72, 1, 26, 31))    # Right [0]
        self.right_small_normal_frames.append(
            self.get_image(98, 1, 26, 31))    # Right walking 1 [1]
        self.right_small_normal_frames.append(
            self.get_image(124, 1, 26, 31))   # Right walking 2 [2]
        self.right_small_normal_frames.append(
            self.get_image(150, 1, 26, 31))   # Right walking 3 [3]
        self.right_small_normal_frames.append(
            self.get_image(124, 1, 26, 31))   # Right jump [4]
        self.right_small_normal_frames.append(
            self.get_image(72, 1, 26, 31))    # Right skid [5]
        self.right_small_normal_frames.append(
            self.get_image(22, 1, 24, 31))    # Death frame [6]
        self.right_small_normal_frames.append(
            self.get_image(46, 1, 26, 31))    # Flag pole slide [7]

        #Images for normal big Sanda

        self.right_big_normal_frames.append(
            self.get_image(72, 1, 26, 31))   # Right [0]
        self.right_big_normal_frames.append(
            self.get_image(98, 1, 26, 31))   # Right walking 1 [1]
        self.right_big_normal_frames.append(
            self.get_image(124, 1, 26, 31))  # Right walking 2 [2]
        self.right_big_normal_frames.append(
            self.get_image(150, 1, 26, 31))  # Right walking 3 [3]
        self.right_big_normal_frames.append(
            self.get_image(124, 1, 26, 31))  # Right jump [4]
        self.right_big_normal_frames.append(
            self.get_image(72, 1, 26, 31))   # Right skid [5]
        self.right_big_normal_frames.append(
            self.get_image(22, 1, 24, 31))   # Death frame [6]
        self.right_big_normal_frames.append(
            self.get_image(46, 1, 26, 31))   # Flag pole slide [7]

        #The left image frames are numbered the same as the right frames but are simply reversed.

        for frame in self.right_small_normal_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_small_normal_frames.append(new_image)

        for frame in self.right_big_normal_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_big_normal_frames.append(new_image)

        self.normal_small_frames = [self.right_small_normal_frames,
                              self.left_small_normal_frames]

        self.normal_big_frames = [self.right_big_normal_frames,
                                  self.left_big_normal_frames]

        self.all_images = [self.right_big_normal_frames,
                           self.right_small_normal_frames,
                           self.left_big_normal_frames,
                           self.left_small_normal_frames]


        self.right_frames = self.normal_small_frames[0]
        self.left_frames = self.normal_small_frames[1]


    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""	
        image = pg.Surface([width, height])
        rect = image.get_rect()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*c.MULTIPLIER),
                                    int(rect.height*c.MULTIPLIER)))
        return image


    def update(self, keys, game_info, fire_group):
        """Updates Mario's states and animations once per frame"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state(keys, fire_group)
        self.check_for_special_state()
        self.animation()


    def handle_state(self, keys, fire_group):
        """Determines Adnas's behavior based on his state"""
        if self.state == c.STAND:
            self.standing(keys, fire_group)
        elif self.state == c.WALK:
            self.walking(keys, fire_group)
        elif self.state == c.JUMP:
            self.jumping(keys, fire_group)
        elif self.state == c.FALL:
            self.falling(keys, fire_group)
        elif self.state == c.DEATH_JUMP:
            self.jumping_to_death()
        elif self.state == c.SMALL_TO_BIG:
            self.changing_to_big()
        elif self.state == c.BIG_TO_FIRE:
            self.changing_to_fire()
        elif self.state == c.BIG_TO_SMALL:
            self.jumping_to_death()
        elif self.state == c.FLAGPOLE:
            self.flag_pole_sliding()
        elif self.state == c.BOTTOM_OF_POLE:
            self.sitting_at_bottom_of_pole()
        elif self.state == c.WALKING_TO_CASTLE:
            self.walking_to_castle()
        elif self.state == c.END_OF_LEVEL_FALL:
            self.falling_at_end_of_level()


    def standing(self, keys, fire_group):
        """This function is called if Mario is standing still"""
        self.check_to_allow_jump(keys)

        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0

        if keys[tools.keybinding['left_o']]:
            self.facing_right = False
            self.get_out_of_crouch()
            self.state = c.WALK
        elif keys[tools.keybinding['right_o']]:
            self.facing_right = True
            self.get_out_of_crouch()
            self.state = c.WALK
        elif keys[tools.keybinding['jump_o']]:
            if self.allow_jump:
                if self.big: setup.SFX['big_jump'].play()
                else: setup.SFX['small_jump'].play()
                self.state = c.JUMP
                self.y_vel = c.JUMP_VEL
        else: self.state = c.STAND

        if not keys[tools.keybinding['down_o']]:
            self.get_out_of_crouch()

    def get_out_of_crouch(self):
        """Get out of crouch"""
        bottom = self.rect.bottom
        left = self.rect.x
        if self.facing_right:
            self.image = self.right_frames[0]
        else:
            self.image = self.left_frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = left
        self.crouching = False


    def check_to_allow_jump(self, keys):
        """Check to allow Mario to jump"""
        if not keys[tools.keybinding['jump_o']]:
            self.allow_jump = True

    def walking(self, keys, fire_group):
        """This function is called when Sanda is in a walking state
        It changes the frame, checks for holding down the run button,
        checks for a jump, then adjusts the state if necessary"""

        self.check_to_allow_jump(keys)

        if self.frame_index == 0:
            self.frame_index += 1
            self.walking_timer = self.current_time
        else:
            if (self.current_time - self.walking_timer >
                    self.calculate_animation_speed()):
                if self.frame_index < 3: self.frame_index += 1
                else:                    self.frame_index = 1

                self.walking_timer = self.current_time

        if keys[tools.keybinding['action_a']]:
            self.max_x_vel = c.MAX_RUN_SPEED
            self.x_accel = c.RUN_ACCEL
        else:
            self.max_x_vel = c.MAX_WALK_SPEED
            self.x_accel = c.WALK_ACCEL

        if keys[tools.keybinding['jump_o']]:
            if self.allow_jump:
                if self.big: setup.SFX['big_jump'].play()
                else: setup.SFX['small_jump'].play()
                self.state = c.JUMP
                if self.x_vel > 4.5 or self.x_vel < -4.5:
                    self.y_vel = c.JUMP_VEL - .5
                else: self.y_vel = c.JUMP_VEL


        if keys[tools.keybinding['left_o']]:
            self.get_out_of_crouch()
            self.facing_right = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = c.SMALL_TURNAROUND
            else:
                self.x_accel = c.WALK_ACCEL

            if self.x_vel > (self.max_x_vel * -1):
                self.x_vel -= self.x_accel
                if self.x_vel > -0.5:
                    self.x_vel = -0.5
            elif self.x_vel < (self.max_x_vel * -1):
                self.x_vel += self.x_accel

        elif keys[tools.keybinding['right_o']]:
            self.get_out_of_crouch()
            self.facing_right = True
            if self.x_vel < 0:
                self.frame_index = 5
                self.x_accel = c.SMALL_TURNAROUND
            else:
                self.x_accel = c.WALK_ACCEL

            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accel
                if self.x_vel < 0.5:
                    self.x_vel = 0.5
            elif self.x_vel > self.max_x_vel:
                self.x_vel -= self.x_accel

        else:
            if self.facing_right:
                if self.x_vel > 0:
                    self.x_vel -= self.x_accel
                else:
                    self.x_vel = 0
                    self.state = c.STAND
            else:
                if self.x_vel < 0:
                    self.x_vel += self.x_accel
                else:
                    self.x_vel = 0
                    self.state = c.STAND


    def calculate_animation_speed(self):
        """Used to make walking animation speed be in relation to
        Mario's x-vel"""
        if self.x_vel == 0:
            animation_speed = 130
        elif self.x_vel > 0:
            animation_speed = 130 - (self.x_vel * (13))
        else:
            animation_speed = 130 - (self.x_vel * (13) * -1)

        return animation_speed


    def jumping(self, keys, fire_group):
        """Called when Mario is in a JUMP state."""
        self.allow_jump = False
        self.frame_index = 4
        self.gravity = c.JUMP_GRAVITY
        self.y_vel += self.gravity

        if self.y_vel >= 0 and self.y_vel < self.max_y_vel:
            self.gravity = c.GRAVITY
            self.state = c.FALL

        if keys[tools.keybinding['left_o']]:
            if self.x_vel > (self.max_x_vel * - 1):
                self.x_vel -= self.x_accel

        elif keys[tools.keybinding['right_o']]:
            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accel

        if not keys[tools.keybinding['jump_o']]:
            self.gravity = c.GRAVITY
            self.state = c.FALL

        if keys[tools.keybinding['action_o']]:
            if self.fire and self.allow_fireball:
                self.shoot_fireball(fire_group)


    def falling(self, keys, fire_group):
        """Called when Mario is in a FALL state"""
        if self.y_vel < c.MAX_Y_VEL:
            self.y_vel += self.gravity

        if keys[tools.keybinding['left_o']]:
            if self.x_vel > (self.max_x_vel * - 1):
                self.x_vel -= self.x_accel

        elif keys[tools.keybinding['right_o']]:
            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accel

        if keys[tools.keybinding['action_o']]:
            if self.fire and self.allow_fireball:
                self.shoot_fireball(fire_group)


    def jumping_to_death(self):
        """Called when Adnas is in a DEATH_JUMP state"""
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 500:
            self.rect.y += self.y_vel
            self.y_vel += self.gravity


    def start_death_jump(self, game_info):
        """Used to put Adnas in a DEATH_JUMP state"""
        self.dead = True
        game_info[c.ADNAS_DEAD] = True
        self.y_vel = -11
        self.gravity = .5
        self.frame_index = 6
        self.image = self.right_frames[self.frame_index]
        self.state = c.DEATH_JUMP
        self.in_transition_state = True

    def timer_between_these_two_times(self,start_time, end_time):
        """Checks if the timer is at the right time for the action. Reduces
        the ugly code."""
        if (self.current_time - self.transition_timer) >= start_time\
            and (self.current_time - self.transition_timer) < end_time:
            return True

    def adjust_rect(self):
        """Makes sure new Rect has the same bottom and left
        location as previous Rect"""
        x = self.rect.x
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = bottom

    def flag_pole_sliding(self):
        """State where Mario is sliding down the flag pole"""
        self.state = c.FLAGPOLE
        self.in_transition_state = True
        self.x_vel = 0
        self.y_vel = 0

        if self.flag_pole_timer == 0:
            self.flag_pole_timer = self.current_time
        elif self.rect.bottom < 493:
            if (self.current_time - self.flag_pole_timer) < 65:
                self.image = self.right_frames[7]
            elif (self.current_time - self.flag_pole_timer) >= 130: self.flag_pole_timer = self.current_time

            self.rect.right = self.flag_pole_right
            self.y_vel = 5
            self.rect.y += self.y_vel

            if self.rect.bottom >= 488:
                self.flag_pole_timer = self.current_time

        elif self.rect.bottom >= 493:
            self.image = self.right_frames[7]


    def sitting_at_bottom_of_pole(self):
        """State when mario is at the bottom of the flag pole"""
        if self.flag_pole_timer == 0:
            self.flag_pole_timer = self.current_time
            self.image = self.left_frames[7]
        elif (self.current_time - self.flag_pole_timer) < 210:
            self.image = self.left_frames[7]
        else:
            self.in_transition_state = False
            if self.rect.bottom < 485:
                self.state = c.END_OF_LEVEL_FALL
            else:
                self.state = c.WALKING_TO_CASTLE


    def set_state_to_bottom_of_pole(self):
        """Sets Mario to the BOTTOM_OF_POLE state"""
        self.image = self.left_frames[7]
        right = self.rect.right
        #self.rect.bottom = 493
        self.rect.x = right
        if self.big: self.rect.x -= 10
        self.flag_pole_timer = 0
        self.state = c.BOTTOM_OF_POLE


    def walking_to_castle(self):
        """State when Adnas walks to the castle to end the level"""
        self.max_x_vel = 5
        self.x_accel = c.WALK_ACCEL

        if self.x_vel < self.max_x_vel:
            self.x_vel += self.x_accel

        if (self.walking_timer == 0 or (self.current_time - self.walking_timer) > 200):
            self.walking_timer = self.current_time

        elif (self.current_time - self.walking_timer) > \
                self.calculate_animation_speed():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time


    def falling_at_end_of_level(self, *args):
        """State when Adnas is falling from the flag pole base"""
        self.y_vel += c.GRAVITY

    def check_for_special_state(self):
        """Determines if Mario is invincible, Fire Mario or recently hurt"""
        self.check_if_invincible()
        self.check_if_hurt_invincible()
        self.check_if_crouching()

    def check_if_invincible(self):
        if self.invincible:
            if ((self.current_time - self.invincible_start_timer) < 10000):
                self.losing_invincibility = False
            elif ((self.current_time - self.invincible_start_timer) < 12000):
                self.losing_invincibility = True
            else:
                self.losing_invincibility = False
                self.invincible = False


    def check_if_hurt_invincible(self):
        """Check if Adnas is still temporarily invincible after getting hurt"""
        if self.hurt_invincible and self.state != c.BIG_TO_SMALL:
            if self.hurt_invisible_timer2 == 0:
                self.hurt_invisible_timer2 = self.current_time
            elif (self.current_time - self.hurt_invisible_timer2) < 2000:
                self.hurt_invincible_check()
            else:
                self.hurt_invincible = False
                self.hurt_invisible_timer = 0
                self.hurt_invisible_timer2 = 0
                for frames in self.all_images:
                    for image in frames:
                        image.set_alpha(255)


    def hurt_invincible_check(self):
        """Makes Mario invincible on a fixed interval"""
        if self.hurt_invisible_timer == 0:
            self.hurt_invisible_timer = self.current_time
        elif (self.current_time - self.hurt_invisible_timer) < 35:
            self.image.set_alpha(0)
        elif (self.current_time - self.hurt_invisible_timer) < 70:
            self.image.set_alpha(255)
            self.hurt_invisible_timer = self.current_time


    def check_if_crouching(self):
        """Checks if mario is crouching"""
        if self.crouching and self.big:
            bottom = self.rect.bottom
            left = self.rect.x
            if self.facing_right:
                self.image = self.right_frames[7]
            else:
                self.image = self.left_frames[7]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = left


    def animation(self):
        """Adjusts Mario's image for animation"""
        if self.state == c.DEATH_JUMP \
            or self.state == c.SMALL_TO_BIG \
            or self.state == c.BIG_TO_FIRE \
            or self.state == c.BIG_TO_SMALL \
            or self.state == c.FLAGPOLE \
            or self.state == c.BOTTOM_OF_POLE \
            or self.crouching:
            pass
        elif self.facing_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]
