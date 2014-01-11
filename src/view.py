import os
import textwrap
import random
import pygame
from pygame.locals import *
from model import *
import model_builder

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
}

UFO_RECT = (6,6,88,88)
FIGHTER_RECT = (113,12,74,75)
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


class UFOSprite(pygame.sprite.Sprite):
    
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'UFO'
        self.image = image
        self.rect = image.get_rect()
        self.fly_region = 0
        self.speed = [0, 0]
        self.autopilot = True
        
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
        
        if not self.autopilot:
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


class FighterJetSprite(pygame.sprite.Sprite):
    
    def __init__(self, image, target):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'Fighter Jet'
        self.image = image
        self.rect = image.get_rect()
        self.target = target
        self.reload_time = 0
        self.movement = 0
        self.fly_region = CANVAS_SIZE[1] / 2
        self.movement_speed = random.randint(10.0, 30.0)
        self.autopilot = True
    
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
        else:
        
            # move inline with target and fire when ready and able.
            diff = self.target.rect.left - self.rect.left
            
            if abs(diff) > self.movement_speed:
                self.rect.left += diff / self.movement_speed
            else:
                if self.reload_time > 0:
                    self.reload_time -= 1
                else:
                    print('Fire!')
                    self.reload_time = 30
            
            if random.randint(1, 100) < 5:
                self.movement = -1
            elif random.randint(1, 100) < 5:
                self.movement = 1
            elif random.randint(1, 100) < 5:
                self.movement = 0
            self.rect.top += self.movement * 4
            self._clamp()


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
        
        # scenario description
        self.brief_offset = 0
        self.brief_sprite = None
        
        # sprite storage
        self.dragging_sprite = None
        self.parts_sprite_sheet = pygame.image.load(os.path.join('..', 'data', 'parts.png')).convert()
        self.parts_sprite_sheet.set_colorkey(TRANSPARENT)
        self.ufo_sprite_sheet = pygame.image.load(os.path.join('..', 'data', 'ufo-sprites.png')).convert()
        self.ufo_sprite_sheet.set_colorkey(TRANSPARENT)
        self.sprites = []
        self.load_sprites()
        self.font = pygame.font.Font(os.path.join('..', 'data', 'emulogic.ttf'), 12)
        
        # confirm dialog
        self.confirm_image = pygame.image.load(os.path.join('..', 'data', 'confirm-dialog.png')).convert()
        self.confirm_action = None
        
        # player objects
        self.ufo_sprite = None
        
    def load_background(self):
        """
        Load a background depending on the game state.
        
        """
        
        if self.model.state == STATE_BUILD:
            self.background = pygame.image.load(os.path.join('..', 'data', 'build-screen.png')).convert()
        if self.model.state == STATE_UFO:
            self.background = pygame.image.load(os.path.join('..', 'data', 'ufo-screen.png')).convert()

    def load_sprites(self):
        """
        Load sprites depending on the game state.
        
        """
        
        self.sprites = []

        if self.model.state == STATE_BUILD:
        
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
        
        if self.model.state == STATE_UFO:
            
            # player ufo craft
            # start off at the bottom center of the screen
            self.ufo_sprite = UFOSprite(self.ufo_sprite_sheet.subsurface(UFO_RECT))
            self.ufo_sprite.fly_region = CANVAS_SIZE[1] / 2
            self.ufo_sprite.rect.center = (CANVAS_SIZE[0] / 2, CANVAS_SIZE[1])
            self.sprites.append(self.ufo_sprite)

    def add_fighter_jet(self):
        # add some jets
        jet = FighterJetSprite(
            self.ufo_sprite_sheet.subsurface(FIGHTER_RECT),
            self.sprites[0])
        jet.rect.top = CANVAS_SIZE[1]
        jet.rect.left = random.randint(100, 400)
        self.sprites.append(jet)

    def draw_hover_part_name(self):
        """
        Return the part name under the cursor.
        
        """
        
        if not self.confirm_action:
            xy = self.translated_mousepos
            for sprite in self.sprites:
                if sprite.rect.collidepoint(xy):
                    part_name = self.font.render(
                        sprite.name, False, BORDER, TRANSPARENT)
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
            False, BORDER, TRANSPARENT)
        part_name.set_colorkey(TRANSPARENT)
        if part_name:
            self.canvas.blit(part_name, (13, 420))

    def blit(self):
        """
        Draw the model state to our game canvas, and finally blit it
        to the screen after we rescale it.
        """

        self.canvas.blit(self.background, (0, 0))
        
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
        
        elif self.model.state == STATE_UFO:
            
            # radar
            self.draw_tactical_radar()
        
        # draw sprites
        for sprite in self.sprites:
            sprite.update()
            self.canvas.blit(sprite.image, sprite.rect)
        
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
        
        if not self.ufo_sprite.autopilot:

            # base image
            self.canvas.blit(
                self.ufo_sprite_sheet.subsurface(RADAR_RECT),
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
                    self.ufo_sprite_sheet.subsurface(RADAR_HOSTILE_RECT),
                    epos)

            # dot for goal distance
            epos = (
                50 + (RADAR_GOAL_RECT[3] / 2), 
                50 - ((self.model.ufotactical.distance_from_goal / 2000.0) * 40)
                )
            self.canvas.blit(
                self.ufo_sprite_sheet.subsurface(RADAR_GOAL_RECT),
                epos)

    def print_wrapped_text(self, sentence, maxlength):
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
            surfii.append(self.font.render(line, False, TEXT, TRANSPARENT))
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
        
        BRIEF_TEXT_HEIGHT = 150
        sprite = pygame.sprite.Sprite()
        image = self.print_wrapped_text(
            model_builder.LEVEL_SCENARIOS[self.model.level - 1], 30)
        sprite.image = image
        sprite.rect = pygame.Rect((0, 0), (image.get_width(), BRIEF_TEXT_HEIGHT))
        self.brief_sprite = sprite

    def scroll_brief(self, offset):
        self.brief_offset += offset
        max_size = self.brief_sprite.rect.height * 2
        if self.brief_offset > max_size:
            self.brief_offset = max_size
        if self.brief_offset < 0:
            self.brief_offset = 0
    
    def model_event(self, event_name, data):
        
        print('view received event %s => %s' % (event_name, data))
        
        if event_name == 'levelup' or event_name == 'state':
            self.load_background()
            self.load_sprites()
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
        self.dragging_sprite = None
        xy = self.translated_mousepos

        # affirmative and negatory buttons
        if self.confirm_action:

            affirm = pygame.Rect(204, 287, 191, 25)
            if affirm.collidepoint(xy):
                
                if self.confirm_action == 'plant':
                    self.model.set_state(STATE_UFO)
                
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
