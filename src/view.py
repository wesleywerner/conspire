import os
import textwrap
import random
import pygame
from pygame.locals import *
from const import *

FRAMERATE = 30
CANVAS_SIZE = (600, 600)
TEXT = (124, 164, 128)
BORDER = (64, 80, 116)
TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
PURPLE = (220, 0, 220)

# parts definition for source image rect
PARTS_RECT = {
    'human torso': (16,35,39,104),
    'human head': (20,0,32,37),
    'human right arm': (0,47,18,81),
    'human left arm': (53,47,18,81),
    'human right leg': (12,130,20,69),
    'human left leg': (39,130,20,69),

    'alien torso': (92,35,39,102),
    'alien head': (96,0,32,37),
    'alien right arm': (76,47,18,81),
    'alien left arm': (129,47,18,81),
    'alien right leg': (88,130,20,69),
    'alien left leg': (115,130,20,69),
    
    'trex torso': (242,51,92,117),
    'trex head': (174,123,56,72),
    'trex tail': (160,0,131,46),
    'trex legs': (168,53,66,63),
}

UFO_RECT = (6,6,88,88)
FIGHTER_RECT = (113,12,74,75)
LIGHTFIGHTER_RECT = (313,12,74,75)
MISSILE_RECT = (194,12,4,28)
RADAR_RECT = (210,10,80,80)
RADAR_HOSTILE_RECT = (245,3,4,4)
RADAR_GOAL_RECT = (250,3,4,4)


class DraggableSprite(pygame.sprite.Sprite):
    
    def __init__(self, name, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = image
        self.rect = rect

class AFOSprite(pygame.sprite.Sprite):
    """
    Player controller Air Force One sprite.
    
    """
    
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'AFO'
        self.original_image = image
        self.image = image
        self.rect = image.get_rect()
        self.fly_region = 0
        self.speed = [0, 0]
        self.autopilot = True
        self.health = 10
        
    def _accelerate(self, x, y):
        self.speed = [self.speed[0] + x, self.speed[1] + y]
        if self.speed[0] < -10:
            self.speed[0] = -10
        if self.speed[1] < -10:
            self.speed[1] = -10
        if self.speed[0] > 10:
            self.speed[0] = 10
        if self.speed[1] > 10:
            self.speed[1] = 10

    def _clamp(self):
        if self.rect.left < 10:
            self.rect.left = 10 
        if self.rect.top < 10:
            self.rect.top = 10 
        if self.rect.right > CANVAS_SIZE[0] - 10:
            self.rect.right = CANVAS_SIZE[0] - 10 
        if self.rect.top > self.fly_region:
            self.rect.top = self.fly_region

    def update(self):
        """
        Player controller craft.
        
        """
        
        # auto move the UFO forward until we are in the top half of the screen
        if self.rect.top > self.fly_region:
            self.rect.top -= 6
            if self.rect.top < self.fly_region:
                self.autopilot = False
        
        pressed = pygame.key.get_pressed()
        lose_acceleration = True
        
        if not self.autopilot and self.health > 0:
            if pressed[K_LEFT] or pressed[K_a]:
                self._accelerate(-1, 0)
                lose_acceleration = False

            if pressed[K_RIGHT] or pressed[K_d]:
                self._accelerate(1, 0)
                lose_acceleration = False
            
            if pressed[K_UP] or pressed[K_w]:
                self._accelerate(0, -1)
                lose_acceleration = False
            
            if pressed[K_DOWN] or pressed[K_s]:
                self._accelerate(0, 1)
                lose_acceleration = False
                
            if pressed[K_F10]:
                self.health = 0
            
            self._clamp()

        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]
        
        if lose_acceleration:
            if self.speed[0] > 0:
                self.speed[0] -= 1
            elif self.speed[0] < 0:
                self.speed[0] += 1
            if self.speed[1] > 0:
                self.speed[1] -= 1
            elif self.speed[1] < 0:
                self.speed[1] += 1
        
    def take_damage(self):
        self.health -= random.randint(1, 3)
        if self.health < 0:
            self.health = 0


class UFOSprite(AFOSprite):
    """
    Behaves like the base sprite and adds rotation.
    
    """
    
    def __init__(self, image):
        AFOSprite.__init__(self, image)
        self.angle = 0
        
    def update(self):
        AFOSprite.update(self)
        self.angle = (self.angle + 10) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class FighterJetSprite(pygame.sprite.Sprite):
    
    def __init__(self, image, target):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'Fighter Jet'
        self.image = image
        self.rect = image.get_rect()
        self.target = target
        self.reload_time = 0
        self.movement = 0
        self.fly_region = CANVAS_SIZE[1] / 1.5
        self.movement_speed = random.randint(10.0, 30.0)
        self.autopilot = True
        self.exitpilot = False
        self._firing = False
    
    def _clamp(self):
        if self.rect.left < 10:
            self.rect.left = 10 
        if self.rect.top > CANVAS_SIZE[1] - 100:
            self.rect.top = CANVAS_SIZE[1] - 100
        if self.rect.right > CANVAS_SIZE[0] - 10:
            self.rect.right = CANVAS_SIZE[0] - 10 
        if self.rect.top < self.fly_region:
            self.rect.top = self.fly_region

    def update(self):
        
        if self.autopilot:
            self.rect.top -= 4
            if self.rect.bottom < CANVAS_SIZE[1] - 100:
                self.autopilot = False
        elif self.exitpilot:
            if self.rect.top < CANVAS_SIZE[1]:
                self.rect.left += 2
                self.rect.top += 4
        else:
        
            # move inline with target and fire when ready and able.
            diff = self.target.rect.left - self.rect.left
            
            if abs(diff) > self.movement_speed:
                self.rect.left += diff / self.movement_speed
            
            if self.reload_time > 0:
                self.reload_time -= 1
            elif abs(diff) < 100:
                print('Fire!')
                self._firing = True
                self.reload_time = 45
            
            if random.randint(1, 100) < 5:
                self.movement = -1
            elif random.randint(1, 100) < 5:
                self.movement = 1
            elif random.randint(1, 100) < 5:
                self.movement = 0
            self.rect.top += self.movement * 4
            self._clamp()
            
            self.exitpilot = self.target.health == 0

    @property
    def is_firing(self):
        if self._firing:
            self._firing = False
            return True
        else:
            return False


class MissileSprite(pygame.sprite.Sprite):
    
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'Missile'
        self.image = image
        self.rect = image.get_rect()
        self.destroy = False
    
    def update(self):
        self.rect.top -= 10
        if self.rect.bottom < 0:
            self.destroy = True


class ExplosionSprite(pygame.sprite.Sprite):
    
    small_size = (57, 57)
    large_size = (89, 89)
    small_rects = (
        (1,185),(61,185),(121,185),(181,185),(241,185),
        (1,245),(61,245),(121,245),(181,245),(241,245),
        )
    large_rects = (
        (1,01),(93,01),(185,01),(277,01),(369,01),
        (1,93),(93,93),(185,93),(277,93),(369,93),
        )
    
    def __init__(self, sprites, is_small=True):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.animation_index = 0
        self.destroy = False
        self.image = None
        self.is_small = is_small
        self._set_sprite()
        self.rect = self.image.get_rect()
    
    def _set_sprite(self):
        if self.is_small:
            self.image = self.sprites.subsurface(self.small_rects[self.animation_index], self.small_size)
        else:
            self.image = self.sprites.subsurface(self.large_rects[self.animation_index], self.large_size)

    def update(self):
        
        self._set_sprite()
        self.animation_index += 1
        self.destroy = self.animation_index >= 10


class View(object):
    
    def __init__(self, pixel_width, pixel_height, model):

        # we may observe the model
        self.model = model

        # listen for model events
        model.register_listener(self.model_event)

        # calculate each block size, and set our viewport size.
        self.screen_size = (pixel_width, pixel_height)

        # init pygame
        pygame.init()
        pygame.display.set_caption('Conspiracy-101')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        # draw game sprites to a surface of a fixed size
        # which we can rescale when blitting to the screen
        self.canvas = pygame.Surface(CANVAS_SIZE).convert()
        self.canvas.set_colorkey(TRANSPARENT)
        
        # calculate the scale size by the canvas/screen height ratio.
        # since canvas is square the width+height always equal
        # but we calculate anyway to be good citizens.
        self.scale_ratio = self.screen_size[1] / float(CANVAS_SIZE[1])
        print('scale ratio is %s' % (self.scale_ratio,))
        
        self.scale_size = (
            int(CANVAS_SIZE[0] * self.scale_ratio), self.screen_size[1])
            
        self.scale_center = ((self.screen_size[0] - self.scale_size[0]) / 2,
            (self.screen_size[1] - self.scale_size[1]) / 2)
        print('scale center is %s' % (self.scale_center,))
        
        # background image storage
        self.background = self.canvas.copy()
        self.load_background()
        self.scrolling_background_yoffset = 0
        
        # scenario description
        self.brief_offset = 0
        self.brief_sprite = None
        self.results_sprite = None
        self.tactical_info_sprite = None

        # sprite sheets
        self.parts_sprite_sheet = pygame.image.load(os.path.join('..', 'data', 'parts.png')).convert()
        self.parts_sprite_sheet.set_colorkey(TRANSPARENT)
        self.player_craft_sheet = pygame.image.load(os.path.join('..', 'data', 'ufo-sprites.png')).convert()
        self.player_craft_sheet.set_colorkey(TRANSPARENT)
        self.explosion_sprite_sheet = pygame.image.load(os.path.join('..', 'data', 'explosion3.png')).convert()
        self.explosion_sprite_sheet.set_colorkey(TRANSPARENT)
        
        # sprite storage
        self.dragging_sprite = None
        self.sprites = []
        
        # font storage
        self.font = pygame.font.Font(os.path.join('..', 'data', 'emulogic.ttf'), 12)
        self.smallfont = pygame.font.Font(os.path.join('..', 'data', 'emulogic.ttf'), 10)
        
        # confirm dialog
        self.confirm_image = pygame.image.load(os.path.join('..', 'data', 'confirm-dialog.png')).convert()
        self.confirm_action = None
        
        # agent images
        self.agent_image = pygame.image.load(os.path.join('..', 'data', 'agent.png')).convert()
        
        # player objects
        self.player_craft = None
        
        # delay exit state
        self.exit_counter = None
        
        
    def load_background(self):
        """
        Load a background depending on the game state.
        
        """
        
        if self.model.state == STATE_MENU:
            self.background = pygame.image.load(os.path.join('..', 'data', 'menu-screen.png')).convert()
        if self.model.state == STATE_BUILD:
            self.background = pygame.image.load(os.path.join('..', 'data', 'build-screen.png')).convert()
        if self.model.state in (STATE_UFO, STATE_FLIGHT):
            self.background = pygame.image.load(os.path.join('..', 'data', 'ufo-screen.png')).convert()
        if self.model.state == STATE_RESULTS:
            self.background = pygame.image.load(os.path.join('..', 'data', 'results-screen.png')).convert()

    def load_build_sprites(self):
        """
        Load sprites depending on the game state.
        
        """
        
        self.sprites = []
        parts = self.model.builder.get_level_parts()
        print('level %s parts are %s' % (self.model.level, parts))
        for part in parts:
            rect = pygame.Rect(PARTS_RECT.get(part, None))
            if rect:
                image = self.parts_sprite_sheet.subsurface(rect)
                rect.center = (random.randint(30, 570), random.randint(230, 370))
                if self.model.builder.part_used(part):
                    rect.center = (random.randint(30, 570), random.randint(430, 570))
                sprite = DraggableSprite(part, image, rect)
                self.sprites.append(sprite)
            else:
                print('warning: part "%s" has no image rect definition' % (part,))
        
    def load_player_craft_sprites(self):
            
        self.sprites = []
        
        # player craft
        player = None
        
        # start off at the bottom center of the screen
        if self.model.state == STATE_UFO:
            player = UFOSprite(self.player_craft_sheet.subsurface(UFO_RECT))

        elif self.model.state == STATE_FLIGHT:
            player = AFOSprite(self.player_craft_sheet.subsurface(LIGHTFIGHTER_RECT))

        if player:
            player.fly_region = CANVAS_SIZE[1] / 2
            player.rect.center = (CANVAS_SIZE[0] / 2, CANVAS_SIZE[1])
            self.sprites.append(player)
            self.player_craft = player

    def add_fighter_jet(self):
        """
        Add a fighter jet to the play field.
        
        """
        
        if self.player_craft:
            jet = FighterJetSprite(
                self.player_craft_sheet.subsurface(FIGHTER_RECT),
                self.player_craft)
            jet.rect.top = CANVAS_SIZE[1]
            jet.rect.left = random.randint(100, 400)
            self.sprites.append(jet)

    def fire_jet_missile(self, jet):
        """
        Fire a missile from a jet.

        """
        
        missile = MissileSprite(
            self.player_craft_sheet.subsurface(MISSILE_RECT))
        missile.rect.center = jet.rect.center
        missile.rect.left += (26 * random.randint(-1, 1))
        self.sprites.append(missile)
    
    def create_explosion(self, target, is_small=True):
        """
        Creat an explosion near target (a sprite object).
        
        """
        
        explosion = ExplosionSprite(self.explosion_sprite_sheet, is_small)
        explosion.rect.center = target.rect.center
        self.sprites.append(explosion)
        
    def draw_hover_part_name(self):
        """
        Return the part name under the cursor.
        
        """
        
        if not self.confirm_action:
            xy = self.translated_mousepos
            for sprite in self.sprites:
                if sprite.rect.collidepoint(xy):
                    part_name = self.font.render(
                        sprite.name, False, TEXT, TRANSPARENT)
                    part_name.set_colorkey(TRANSPARENT)
                    if part_name:
                        self.canvas.blit(part_name, (13, 370))
                        return

    def draw_body_accuracy(self):
        """
        Return the part name under the cursor.
        
        """
        
        part_name = self.font.render(
            'accuracy: %s %%' % (self.model.builder.accuracy, ),
            False, TEXT, TRANSPARENT)
        part_name.set_colorkey(TRANSPARENT)
        if part_name:
            self.canvas.blit(part_name, (13, 420))

    def blit(self):
        """
        Draw the model state to our game canvas, and finally blit it
        to the screen after we rescale it.
        """

        garbage_sprites = []
        self.canvas.blit(self.background, (0, 0))
        
        if self.model.state != STATE_MENU and self.exit_counter > 0:
            self.exit_counter -= 1
        
        if self.model.state == STATE_BUILD:
        
            # dragging a sprite
            if self.dragging_sprite:
                self.dragging_sprite.rect.center =  self.translated_mousepos
            
            # briefing words
            if self.brief_sprite:
                self.canvas.blit(self.brief_sprite.image, 
                    (14, 22), 
                    self.brief_sprite.rect.move(0, self.brief_offset))
            
            self.draw_hover_part_name()
            self.draw_body_accuracy()
        
            # draw sprites
            for sprite in self.sprites:
                sprite.update()
                self.canvas.blit(sprite.image, sprite.rect)

        elif self.model.state in (STATE_UFO, STATE_FLIGHT):
            
            bh = self.background.get_height()
            self.scrolling_background_yoffset += 15
            if self.scrolling_background_yoffset > bh:
                self.scrolling_background_yoffset = 0
            self.canvas.blit(self.background, (0, self.scrolling_background_yoffset))
            self.canvas.blit(self.background, (0, self.scrolling_background_yoffset - bh))
            
            # radar
            self.draw_tactical_radar()
            
            # health bar
            self.draw_ufo_healthbar()
                
            # help words
            self.draw_ufo_help()
            
            # exit
            if self.exit_counter == 0:
                self.model.mission_success = self.model.ufotactical.distance_from_goal < 10
                self.model.set_state(STATE_RESULTS)

            # draw sprites
            for sprite in self.sprites:
                sprite.update()
                self.canvas.blit(sprite.image, sprite.rect)
                
                if isinstance(sprite, FighterJetSprite):
                    if sprite.is_firing:
                        self.fire_jet_missile(sprite)
                        
                elif isinstance(sprite, MissileSprite):
                    if self.player_craft.health > 0:
                        if self.player_craft.rect.colliderect(sprite.rect):
                            # TODO hit sound and explosion
                            garbage_sprites.append(sprite)
                            self.player_craft.take_damage()
                            if self.player_craft.health > 0:
                                self.create_explosion(sprite, is_small=True)
                            else:
                                self.create_explosion(sprite, is_small=False)
                                
                elif isinstance(sprite, AFOSprite):
                    if self.player_craft.health == 0 and not self.exit_counter:
                        self.exit_counter = 100
                        garbage_sprites.append(sprite)
                        
                elif isinstance(sprite, ExplosionSprite):
                    if sprite.destroy:
                        garbage_sprites.append(sprite)

        elif self.model.state == STATE_RESULTS:
            
            # report!
            if self.results_sprite:
                self.canvas.blit(self.results_sprite, (111, 100))
        
        if self.model.state != STATE_MENU:
            
            # garbage
            for g in garbage_sprites:
                if g in self.sprites:
                    self.sprites.remove(g)
            
            # confirm
            if self.confirm_action:
                csize = self.canvas.get_size()
                size = pygame.Rect((0, 0), self.confirm_image.get_size())
                size.center = (csize[0] / 2, csize[1] / 2)
                self.canvas.blit(self.confirm_image, size)
            
        # rescale
        if self.scale_ratio > 1.0:
            self.screen.blit(
                pygame.transform.scale(self.canvas, self.scale_size),
                self.scale_center)
        else:
            self.screen.blit(self.canvas, (0, 0))
        
        # flip and tick
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    def draw_tactical_radar(self):
        
        # base image
        self.canvas.blit(
            self.player_craft_sheet.subsurface(RADAR_RECT),
            (10, 10))
        
        # enemy fighters
        incoming_jets = self.model.ufotactical.jet_distances
        for enemy in incoming_jets:
            # draw a dot for it's distance.
            epos = (
                50,
                50 + ((enemy / 500.0) * 40)
                )
            self.canvas.blit(
                self.player_craft_sheet.subsurface(RADAR_HOSTILE_RECT),
                epos)

        # dot for goal distance
        epos = (
            50 + (RADAR_GOAL_RECT[3] / 2), 
            50 - ((self.model.ufotactical.distance_from_goal / 2000.0) * 40)
            )
        self.canvas.blit(
            self.player_craft_sheet.subsurface(RADAR_GOAL_RECT),
            epos)

    def draw_ufo_help(self):
        
        if self.model.state in (STATE_UFO, STATE_FLIGHT):
            # for the first few ticks
            if self.model.ufotactical.clock  < 250: #250
                # draw the agent picture
                self.canvas.blit(self.agent_image, (10, 10))
                # and show some helpful words of wisdom
                if self.tactical_info_sprite:
                    self.canvas.blit(self.tactical_info_sprite, (220, 40))
            
    def draw_ufo_healthbar(self):
        hp = self.player_craft.health * 8 + 1
        fullrect = pygame.Rect(10, 100, 80, 10)
        rect = pygame.Rect(10, 100, hp, 10)
        pygame.draw.rect(self.canvas, RED, fullrect, 0)
        pygame.draw.rect(self.canvas, GREEN, rect, 0)
        pygame.draw.rect(self.canvas, BLACK, fullrect, 2)
    
    def print_wrapped_text(self, sentence, maxlength, font, color):
        """
        Creates an image with the given words wrapped.
        
        """

        lines = []
        paragraphs = sentence.split('\n')
        for p in paragraphs:
            lines.extend(textwrap.wrap(p, maxlength))
            lines.append(' ')
        surfii = []
        max_width = 0
        total_height = 0
        for line in lines:
            surfii.append(font.render(line, False, color, TRANSPARENT))
            print_size = surfii[-1].get_size()
            if print_size[0] > max_width:
                max_width = print_size[0]
            total_height += print_size[1]
        
        combined = pygame.Surface((max_width, total_height))
        combined.fill(TRANSPARENT)
        print_position = 0
        for print_surface in surfii:
            combined.blit(print_surface, (0, print_position))
            print_position += print_surface.get_height()
        
        combined.set_colorkey(TRANSPARENT)
        return combined
    
    def draw_briefing_words(self):
        """
        Redraw the briefing wording.
        
        """
        
        if self.model.state == STATE_BUILD:

            BRIEF_TEXT_HEIGHT = 150

            brief_text = LEVEL_SCENARIOS[self.model.level - 1]
            if self.model.level > 1:
                if self.model.mission_success:
                    brief_text = 'My commendations on your last ' \
                        'mission, what a success!\n' + brief_text
                else:
                    brief_text = 'Failure like your last mission will ' \
                        'not be tolerated. Let us hope your next ' \
                        'mission goes better...\n' + brief_text
                    
            sprite = pygame.sprite.Sprite()

            image = self.print_wrapped_text(
                brief_text, 
                30,
                self.font,
                TEXT
                )
            sprite.image = image
            sprite.rect = pygame.Rect((0, 0), (image.get_width(), BRIEF_TEXT_HEIGHT))
            self.brief_sprite = sprite
        
        elif self.model.state in (STATE_UFO, STATE_FLIGHT):
            
            self.tactical_info_sprite = self.print_wrapped_text(
                'Avoid gunfire until you reach the target zone. ' \
                'Once in the zone, you must get shot down on purpose. ' \
                'Timing is critical, good luck Agent!',
                30,
                self.font,
                TEXT
                )
        
        elif self.model.state == STATE_RESULTS:
            
            self.results_sprite = self.print_wrapped_text(
                self.model.results, 35, self.smallfont, BLACK)

    def scroll_brief(self, offset):
        if self.model.state == STATE_BUILD:
            self.brief_offset += offset
            max_size = self.brief_sprite.rect.height * 2
            if self.brief_offset > max_size:
                self.brief_offset = max_size
            if self.brief_offset < 0:
                self.brief_offset = 0
    
    def model_event(self, event_name, data):
        
        print('view event "%s" => %s' % (event_name, data))
        
        if event_name == 'levelup':
            self.player_craft = None
            
        elif event_name == 'state':
            self.load_background()
            
            if self.model.is_new_level:
                self.draw_briefing_words()
                self.exit_counter = None
                self.load_build_sprites()
            
            if self.model.state in (STATE_UFO, STATE_FLIGHT) and not self.player_craft:
                self.draw_briefing_words()
                self.load_player_craft_sprites()
                
            if self.model.state == STATE_RESULTS:
                self.draw_briefing_words()
        
        elif event_name == 'deploy fighter jet':
            self.add_fighter_jet()

    @property
    def translated_mousepos(self):
        """
        Get the mouse position as translated to to screen size ratio.
        
        """
        
        xy = pygame.mouse.get_pos()
        scaled_xoffset = (self.scale_center[0] / self.scale_ratio)
        scaled_yoffset = (self.scale_center[1] / self.scale_ratio)
        xy = (
            xy[0] / self.scale_ratio - scaled_xoffset, 
            xy[1] / self.scale_ratio - scaled_yoffset)
        return xy
    
    def mouseDown(self):
        
        if self.model.state == STATE_MENU:
            return
            
        self.dragging_sprite = None
        xy = self.translated_mousepos

        # affirmative and negatory buttons
        if self.confirm_action:

            affirm = pygame.Rect(204, 287, 191, 25)
            if affirm.collidepoint(xy):
                
                if self.confirm_action == 'plant':
                    print('level is', self.model.level)
                    print('tactical mode is', TACTICAL_TYPE[self.model.level])
                    self.model.set_state(TACTICAL_TYPE[self.model.level])
                
                self.confirm_action = None
                
            negate = pygame.Rect(204, 337, 191, 25)
            if negate.collidepoint(xy):
                self.confirm_action = None
                
            return

        if self.model.state == STATE_BUILD:

            # sprite click
            for sprite in self.sprites:
                if sprite.rect.collidepoint(xy):
                    self.dragging_sprite = sprite
                    # place dragging sprite on top
                    self.sprites.remove(self.dragging_sprite)
                    self.sprites.append(self.dragging_sprite)
                    return

            # plant button click
            button = pygame.Rect(390, 165, 198, 29)
            if button.collidepoint(xy):
                self.confirm_action = 'plant'
            
    def mouseUp(self):
        if self.dragging_sprite:
            part = self.dragging_sprite.name
            self.dragging_sprite = None
            x,y = self.translated_mousepos
            if y < 400:
                self.model.builder.remove_part(part)
            else:
                self.model.builder.add_part(part)

    def mouseWheelUp(self):
        self.scroll_brief(-16)

    def mouseWheelDown(self):
        self.scroll_brief(16)

    def keyDown(self, key):
        if key == K_DOWN:
            self.scroll_brief(16)
        if key == K_UP:
            self.scroll_brief(-16)
