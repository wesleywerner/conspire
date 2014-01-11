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
        
        # confirm dialog
        self.confirm_image = pygame.image.load(os.path.join('..', 'data', 'confirm-dialog.png')).convert()
        self.confirm_action = None
        
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
        
        # draw sprites
        for sprite in self.sprites:
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
