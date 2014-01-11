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
    'human torso': (14, 23, 18, 51),
    'human head': (15, 4, 16, 19),
    'human right arm': (5, 28, 9, 41),
    'human left arm': (32, 28, 9, 41),
    'human right leg': (11, 70, 10, 35),
    'human left leg': (25, 70, 10, 35),

    'alien torso': (65, 22, 20, 52),
    'alien head': (67, 4, 16, 19),
    'alien right arm': (57, 28, 9, 41),
    'alien left arm': (84, 28, 9, 41),
    'alien right leg': (63, 70, 10, 35),
    'alien left leg': (77, 70, 10, 35),
}

class DraggableSprite(pygame.sprite.Sprite):
    
    def __init__(self, name, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = image
        self.rect = rect

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
        self.sprites = []
        self.load_sprites()
        self.font = pygame.font.Font(os.path.join('..', 'data', 'emulogic.ttf'), 12)
        
    def load_background(self):
        """
        Load a background depending on the game state.
        
        """
        
        if self.model.state == STATE_BUILD:
            self.background = pygame.image.load(os.path.join('..', 'data', 'build-screen.png')).convert()

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

    def draw_hover_part_name(self):
        """
        Return the part name under the cursor.
        
        """
        
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
        
        # draw sprites
        for sprite in self.sprites:
            self.canvas.blit(sprite.image, sprite.rect)
        
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
    
#    def screenpos(self, xy

    def mouseDown(self):
        self.dragging_sprite = None
        if self.model.state == STATE_BUILD:
            
            #xy = pygame.mouse.get_pos()
            xy = self.translated_mousepos
            
            # sprite click
            for sprite in self.sprites:
                if sprite.rect.collidepoint(xy):
                    self.dragging_sprite = sprite
                    return

            # plant button click
            button = pygame.Rect(390, 165, 198, 29)
            if button.collidepoint(self.translated_mousepos):
                self.model.set_state(STATE_GUNFIGHT)

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
