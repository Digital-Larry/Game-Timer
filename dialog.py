#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, settings, sys

DIALOGCOLOR = (2,210,10)
TEXTCOLOR = (250, 250, 255)

# blit(source, dest, area=None, special_flags = 0) -> Rect
# Draws a source Surface onto this Surface. The draw can be positioned with
# the dest argument. Dest can be a pair of coordinates representing the
# upper left corner of the source. A Rect can also be passed as the
# destination and the topleft corner of the rectangle will be used as the
# position for the blit. The size of the destination rectangle does not
# affect the blit.

# An optional area rectangle can be passed as well. This represents a smaller
# portion of the source Surface to draw.

class Dialog(object):
    def __init__(self, text, question, settings):
       self.font = pygame.font.SysFont(settings.get_font(), 32)
       string = '{:^3}:{:^1}'.format(text, question)
       self.text = self.font.render(string, 1, TEXTCOLOR, DIALOGCOLOR)
       textpos = self.text.get_rect()
       self.textsize = self.font.size(string)
       
       # create a dialog box with some padding around the edges
       dialogx = self.textsize[0] + self.font.size("    ")[0]
       dialogy = self.textsize[1] * 3
       print "Dialog x = ", dialogx, "Dialog y = ", dialogy
       self.dialog = pygame.Surface((dialogx, dialogy))
       self.dialog.fill(DIALOGCOLOR);
       # dialogcenter = (self.dialog.get_size()[0]/2, self.dialog.get_size()[1]/2)
       textpos.centerx = self.dialog.get_rect().centerx
       textpos.centery = self.dialog.get_rect().centery
       self.dialog.blit(self.text, textpos)
       
       # print self.text, "self.textsize: ", self.textsize
       self.dialogpos = self.dialog.get_rect()
       print "self.dialogpos: ", self.dialogpos
       self.saveScreen = pygame.Surface((self.dialogpos[2], self.dialogpos[3]))

    def setTextCenter(self, screen):
       self.dialogpos.centerx = screen.get_size()[0]/2
       self.dialogpos.centery = screen.get_size()[1]/2
       # print "self.textpos: ", self.textpos

    def show(self, screen):
       print "Show"
       print screen.blit(self.dialog, self.dialogpos)
       pygame.display.flip()
       
    def saveBackground(self, screen):
       print "save self.dialogpos: ", self.dialogpos
       print self.saveScreen.blit(screen, (0, 0), self.dialogpos)
       pygame.display.flip()
       
    def restoreBackground(self, screen):
       print "restore self.dialogpos: ", self.dialogpos
       print screen.blit(self.saveScreen, self.dialogpos)
       pygame.display.flip()
     
import time, gradient

def main():
   pygame.init()
   screen = pygame.display.set_mode((480,240))
   gradient.fill_gradient(screen, (250,0,20), (0,0,250))

   if not pygame.font:
      print 'Warning, fonts disabled'

   appSettings = settings.Settings("freesans")

   dialog1 = Dialog("Quit? (y/n)", "Y", appSettings)

   dialog1.setTextCenter(screen)
   dialog1.saveBackground(screen)
   time.sleep(2)
   dialog1.show(screen)
   time.sleep(3)

   dialog1.restoreBackground(screen)
   time.sleep(2)

   sys.exit()

if __name__ == '__main__': main()
