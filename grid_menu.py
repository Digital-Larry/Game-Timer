import pygame, sys,os, math, audio_queue, timer_rect
from pygame.locals import *
MENUFONTSIZE = 16


# menu class for settings adjustment
class GridMenu:
   def __init__(self, x, y, waitloop, settings):
      self.waitloop = waitloop
      self.lineList = []
      self.MenuDepth = 0
      self.menu_level = 0
      self.MenuSelection = 0
      self.left = x
      self.top = y
      self.font = settings.get_font()

   # adjust is the function, values is a list of params to send to the function
   def AddLine(self, name, adjust, values):
      self.lineList.append((name, adjust, values))
      
   def MenuKey(self, key):
      # print "Key = ", key, "Menu_depth = ", self.MenuDepth, "Menu_level = ", self.menu_level, "MenuSelection = ", self.MenuSelection
      if key == K_1:
         if self.MenuDepth == 0:
            self.MenuSelection = 0
            self.MenuDepth = 1
      if key == K_2:
         if self.MenuDepth == 0:
            self.MenuSelection = 0
            self.MenuDepth = 1
      if key == K_RETURN:
         if self.MenuDepth == 0:
            self.MenuSelection = 0
            self.MenuDepth = 1
         elif self.MenuDepth == 1:
            # print self.Menu[self.menu_level].values
            self.lineList[self.menu_level][1](self.lineList[self.menu_level][2][self.MenuSelection])
            return
      if key == K_UP:
         if(self.menu_level > 0):
            self.MenuSelection = 0
            self.menu_level -= 1;
      if key == K_DOWN:
         if self.menu_level < (len(self.lineList[self.menu_level])):
            self.MenuSelection = 0
            self.menu_level += 1;
      if key == K_RIGHT:
         if(self.MenuSelection < len(self.lineList[self.menu_level][2]) - 1):
            self.MenuSelection += 1
      if key == K_LEFT:
         if self.MenuSelection > 0:
            self.MenuSelection -= 1

   def drawMenuLine(self, screen, textcolor, bgcolor):
      font = pygame.font.SysFont(self.font, MENUFONTSIZE)
      i = 0      
      for x in self.lineList:
         if i == self.menu_level:
            background = bgcolor
         else:
            background = (0, 0, 0)
         # x[0] is the menu line name   
         text = font.render(x[0], 1, textcolor, background)
         textpos = text.get_rect(center=(self.left - 12, self.top + (18 * i) + 118))
         screen.blit(text, textpos)
         ii = 0
         for y in self.lineList[i][2]:
            # print ii, self.MenuSelection
            # skip zero, it is not used
            if self.lineList[i][2][ii] <> 0:
               if (i == self.menu_level) & (ii == self.MenuSelection):
                  background = bgcolor
               else:
                  background = (0, 0, 0)
               text = font.render(' {} '.format(y), 1, textcolor, background)
               textpos = text.get_rect(center=(self.left + 55 + ii * 36, self.top + (18 * i) + 118))
               screen.fill((40, 40, 120), textpos)
               screen.blit(text, textpos)
            ii = ii + 1
         i = i + 1

   def showMenu(self, screen):
      # print self.left,self.top
      self.drawMenuLine(screen, (250,250,250), (0, 0, 180))
      
   def clearMenu(self, screen, key_string):
      screen.fill((20,0,0), (0, self.top + 100, 1024, 100))
#      font = pygame.font.Font(None, 24)
      background = (0, 0, 0)
         # x[0] is the menu line name   
      # text = font.render('{:^50}'.format(""), 1, message_fg, message_bg)
      font = pygame.font.SysFont(self.font, MENUFONTSIZE)
      text = font.render("Press {0} to pause/edit".format(key_string), 1, (240,240,240), background)
      textpos = text.get_rect(midleft=(self.left + 15, self.top + 118))
      screen.blit(text, textpos)

      text = font.render("4/5/6: 30/45/60 minute turn, both players", 1, (240,240,240), background)
      textpos = text.get_rect(midleft=(self.left + 15, self.top + 136))
      screen.blit(text, textpos)

      text = font.render("7/8/9/0: 30/60/90/120 minute break, both players", 1, (240,240,240), background)
      textpos = text.get_rect(midleft=(self.left + 15, self.top + 154))
      screen.blit(text, textpos)

# ========= Menu class end
