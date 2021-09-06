import os, sys
import pygame
from pygame import *

import src.modules.app as app

pygame.init()
pygame.mixer.init()


class Body:
    def __init__(self, pos=Vector2(0,0), vel=Vector2(0,0), ignore_paused=False):
        app.children.append(self)
        
        self.pos = pos
        self.vel = vel
        self.ignore_paused = ignore_paused
        

class Paddle(Body):
    def __init__(self, pos=Vector2(0,0), vel=Vector2(0,0), keys=[pygame.K_w, pygame.K_s], size=Vector2(25, 120), ignore_paused=False):
        #Properties
        self.color = [255,255,255]
        self.keys = keys
        self.size = size
        
        #Graphics
        self.model = pygame.Surface(self.size)
        self.rect = self.model.get_rect()
        
        super().__init__(pos, vel, ignore_paused)
        
    def draw(self):
        self.model.fill(self.color)
        app.screen.blit(self.model, self.rect)

        
    def update(self):
        if not app.paused:
            keys=pygame.key.get_pressed()
            
            #Getting key to controll
            self.vel.y = keys[self.keys[0]] * -5 or keys[self.keys[1]] * 5
            self.pos += self.vel
            self.rect.center = self.pos
            
        self.draw()
        
class Ball(Body):
    def __init__(self, pos=Vector2(0,0), vel=Vector2(0,0), ignore_paused=False, render=True):
        #Properties
        self.color = [255,255,255]
        self.radius = 13
        self.render = render
        
        #Sound
        cFolder = os.path.dirname(os.path.realpath(sys.argv[0])) #Thanks Stack Overflow
        full_path = os.path.join(cFolder, "src\\assets\\sfx\\Wall_Hit.ogg")
        self.wallHit = pygame.mixer.Sound(full_path)
        self.wallHit.set_volume(.1)
        
        full_path = os.path.join(cFolder, "src\\assets\\sfx\\Paddle_Hit.ogg")
        self.paddleHit = pygame.mixer.Sound(full_path)
        self.paddleHit.set_volume(.1)
        
        #Graphics
        self.model = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
        self.rect = self.model.get_rect()
        
        
        super().__init__(pos, vel, ignore_paused)
        
    def on_right(self):
        pass
        
    def on_left(self):
        pass
        
    def check_collision(self):
        # Rectangle collision
        collided = False
        for child in app.children:
            if hasattr(child, 'rect') and child != self:
                if self.rect.colliderect(child.rect):
                    self.paddleHit.play()
                    if self.vel.magnitude() < 25: self.vel *= 1.05
                    if child.pos.x < app.screen.get_size()[0]/2:
                        self.pos.x = child.pos.x + child.model.get_size()[0]/2 + self.radius
                    else:
                        self.pos.x = child.pos.x - child.model.get_size()[0]/2 - self.radius
                    
                    self.vel.x *= -1
                    
        # Wall collision
        initPosition = Vector2(app.screen.get_size()[0]/2, app.screen.get_size()[1]/2)
        
        if self.pos.y - self.radius < 0: self.vel.y *= -1; self.wallHit.play()
        if self.pos.y + self.radius > app.screen.get_size()[1]: self.vel.y*=-1; self.wallHit.play()
        
        if self.pos.x + self.radius < 0: self.pos = initPosition; self.on_left()
        if self.pos.x - self.radius > app.screen.get_size()[0]: self.pos = initPosition; self.on_right()
    
    def draw(self):
        pygame.draw.circle(self.model, self.color, Vector2(self.radius, self.radius), self.radius)
        app.screen.blit(self.model, self.rect)
        
    def update(self):
        if not app.paused:
        
            self.check_collision()
            
            # Movement
            self.pos += self.vel
            self.rect.center = self.pos
        if self.render: self.draw()
        
        
class Net:
    def __init__(self, ignore_paused=False):
        self.children = []
        self.ignore_paused = ignore_paused
        app.children.append(self)
        
        for i in range(0,5):
            child = pygame.Surface([15,55])
            child.fill([255,255,255])
            rect = child.get_rect()
            rect.centerx = 450
            rect.y = 120*i+ 25
            self.children.append([child, rect])
        
    def update(self):
        for child in self.children:
            app.screen.blit(child[0], child[1])