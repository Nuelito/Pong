import pygame
from pygame import*

import src.modules.app as app

pygame.init()
pygame.font.init()

class Label:
    def __init__(self, text="Hello World", render=True, pos=Vector2(0,0), fontName="Arial Black", fontSize=50, ignore_paused=False):
        app.children.append(self)
        
        #Properties
        self.pos = pos
        self.text = text
        self.render = render
        self.ignore_paused = ignore_paused
        
        self.font = pygame.font.SysFont(fontName, fontSize)
    
    def update(self):
        if self.render == True:
            surf = self.font.render(self.text, True, [255,255,255])
            rect = surf.get_rect()
            
            rect.center = self.pos
            app.screen.blit(surf, rect)

class Entry:
    def __init__(self, text="", render=True, size=Vector2(180, 32), pos=Vector2(0,0), fontName="Arial Black", fontSize=30, ignore_paused=False):
        app.children.append(self)

        #Properties
        self.pos = pos
        self.size = size
        self.text = text
        self.fontSize = fontSize
        self.render = render
        self.ignore_paused = ignore_paused

        #Colors
        self.active = False
        self.active_color = [255,255,255]
        self.inactive_color = [175, 175, 175]

        self.font = pygame.font.SysFont(fontName, fontSize)

    def on_unactivate(self):
        pass

    def update(self):
        color = self.inactive_color
        if self.active: color = self.active_color
        surf = self.font.render(self.text, True, color)

        input_rect = pygame.Rect(200, 200, self.size.x, self.size.y)
        input_rect.center = self.pos

        # Mouse detection
        if pygame.mouse.get_pressed()[0]:
            if input_rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False

        if self.active == True:
            app.typing = True
            for keyEvent in app.keyList:
                if keyEvent.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                elif keyEvent.key == pygame.K_RETURN or keyEvent.key == pygame.K_ESCAPE:
                    self.active = False
                    app.typing = False
                    self.on_unactivate()
                else:
                    self.text += keyEvent.unicode
                    if surf.get_rect().w + self.fontSize/1.5 > input_rect.w:
                        self.text = self.text[:-1]
                        self.active = False
                        app.typing = False
                        self.on_unactivate()

        pygame.draw.rect(app.screen, color, input_rect, 1)
        app.screen.blit(surf, (input_rect.x + 5, input_rect.y - 5))


class CheckBox:
    def __init__(self, pos=Vector2(0,0), size=30, active=False, checked=True):
        app.children.append(self)

        #Properties
        self.pos = pos
        self.size = size

        #Other
        self.active = active
        self.checked = checked

        self.active_color = [255,255,255]
        self.inactive_color = [175, 175, 175]

        self.__vertices = [
            Vector2(-.5, -.2),
            Vector2(0, .3),
            Vector2(.7, -.7),
            Vector2(0, 0)
        ]

    def on_deactivate(self):
        pass

    def on_activate(self):
        pass

    def update(self):
        vertices = []
        color = self.inactive_color
        if self.active: color = self.active_color

        for vertex in self.__vertices:
            vertex = vertex*self.size + self.pos

            vertices.append(vertex)

        input_rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        input_rect.center = self.pos
        pygame.draw.rect(app.screen, color, input_rect, 2)

        for mouseEvent in app.mouseList:
            if mouseEvent.button == 1:
                if input_rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = True
                    self.checked = not self.checked
                    if self.active == True:
                        self.on_activate()
                    else:
                        self.on_deactivate()
                else:
                    self.active = False

        if self.checked == True:
            pygame.draw.polygon(app.screen, color, vertices)

class InputSaver:
    def __init__(self, input=110, pos=Vector2(450, 300), fontName="Arial Black", fontSize = 25):
        app.children.append(self)

        #Properties
        self.input = input
        self.pos = pos

        self.inactive_color = [200,200,200]
        self.active_color = [255,255,255]
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.active = False

    def on_deactivate(self):
        pass

    def update(self):
        color = self.inactive_color
        if self.active: color = self.active_color
        surf = self.font.render(pygame.key.name(int(self.input)), True, color)
        rect = surf.get_rect()
        rect.center = self.pos

        for mouseEvent in app.mouseList:
            if mouseEvent.button == 1:
                if rect.collidepoint(mouse.get_pos()):self.active = True; app.typing = True
                else: self.active = False; app.typing = False

        #Getting key
        if self.active:
            for keyEvent in app.keyList:
                if keyEvent.key != pygame.K_ESCAPE:
                    self.input = str(keyEvent.key)
                self.on_deactivate()
                self.active = False
                app.typing = False

        app.screen.blit(surf, rect)