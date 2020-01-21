import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *

FPS = 30
ANIMATION_SPEED = 0.4 #hitrost animacije (stebri na daljših intervalih)  
BACKGROUND_WIDTH = 800   
BACKGROUND_HEIGHT = 450
POV_ozadja = pygame.display.set_mode((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
pygame.display.set_caption('Hiker ptic') #ime
clock = pygame.time.Clock() #objekt, ki meri čas v igri in pomaga pri določenih drugih funkcijah

class ptic(pygame.sprite.Sprite):
#kreiranje ptička
    WIDTH = 44
    HEIGHT = 32 #piksli = velikost slike v mapi
    SINK_SPEED = 0.25 #hitrost padanja
    CLIMB_SPEED = 0.3 #hitrost dviganja
    CLIMB_DURATION = 333.3 #trajanje dviganja

    def __init__(self, x, y, msek_dviganje, images):

        super(ptic, self).__init__()
        self.x, self.y = x, y  #položaj ptica
        self.msek_dviganje = msek_dviganje #milisekunde dviganja
        self.ptic = images #uporabljena slika ptiča
        images = load_images()

    def update(self, delta_frames=1): #položaj in hitrosti ptiča sproti - ne spreminjaj!!
        if self.msek_dviganje > 0:
            frac_climb_done = 1 - self.msek_dviganje/ptic.CLIMB_DURATION
            self.y -= (ptic.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msek_dviganje -= frames_to_msec(delta_frames)
        else:
            self.y += ptic.SINK_SPEED * frames_to_msec(delta_frames)

    @property 
    def image(self): #definicija ptiča
            return self.ptic
      
    @property
    def rect(self):
        return Rect(self.x, self.y, ptic.WIDTH, ptic.HEIGHT)

#generiranje ovir
class ovira(pygame.sprite.Sprite):

    WIDTH = 68
    vis_ovire = 10
    INTERVAL = 1500  #razdalija med ovirami

    def __init__(self, pipe_img): 
       
        self.x = float(BACKGROUND_WIDTH)

        self.image = pygame.Surface((ovira.WIDTH, BACKGROUND_HEIGHT))
        vse_ovire = int(
            (BACKGROUND_HEIGHT -                  
             3 * ptic.HEIGHT -             # prostor med ovirama
             6 * ovira.vis_ovire) /  
            ovira.vis_ovire          
        )
        self.spodnji_deli = randint(1, vse_ovire)
        self.zgornji_deli = vse_ovire - self.spodnji_deli

        # bottom pipe
        for i in range(1, self.spodnji_deli):
            polozaj = (0, BACKGROUND_HEIGHT - i*ovira.vis_ovire)
            self.image.blit(pipe_img, polozaj)
        # top pipe
        for i in range(self.zgornji_deli):
            self.image.blit(pipe_img, (0, i * ovira.vis_ovire))

    @property
    def rect(self):
        return Rect(self.x, 0, ovira.WIDTH, ovira.vis_ovire)

    def update(self, delta_frames=1):
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

def load_images():#Nalaganje slik brez problema - obvezno tako!!
    def load_image(img_file_name):
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        return img

    return {'background': load_image('background.png'),
            'pipe': load_image('pipe.jpg'),
            'ptic': load_image('ptic.jpg')}

def frames_to_msec(frames, fps=FPS):
    return 1000.0 * frames / fps

def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0

def main():
    pygame.init()

    images = load_images()

    Ikona = ptic(30, int(BACKGROUND_HEIGHT/2 - ptic.HEIGHT/2), 2,
                (images['ptic']))  

    pipes = deque()

    frame_clock = 0  
    done = paused = False
    while not done:
        clock.tick(FPS)

        if frame_clock == 40:
            pp = ovira(images['pipe']) 
            pipes.append(pp)
            frame_clock=0

        for e in pygame.event.get():
            if e.type == QUIT and e.key==K_ESCAPE:   
                done = True
                break
            elif e.type == KEYUP and e.key in (K_UP, K_SPACE):
                Ikona.msek_dviganje = ptic.CLIMB_DURATION

        #da se slike ne 'mažejo'
        for x in (0, BACKGROUND_WIDTH / 2):
            POV_ozadja.blit(images['background'], (x, 0))

        #da se prikazujejo stebri in ptič
        for p in pipes:
            p.update()
            POV_ozadja.blit(p.image, p.rect)

        Ikona.update() #da se ptič spoti prikazuje!!
        POV_ozadja.blit(Ikona.image, Ikona.rect)

        pygame.display.flip()
        frame_clock += 1
    pygame.quit()

#vedno na koncu v približno taki obliki
if __name__ == '__main__':
    main()
