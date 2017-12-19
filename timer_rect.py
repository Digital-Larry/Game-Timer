import pygame, sys,os, math, gradient
from pygame.locals import *

TIMEBACKGROUND = (0, 0, 60)
SCREENTOPCOLOR = (250,250,250)
SCREENBOTTOMCOLOR = (0,0,200)


# displayed rectangle class definitions
class TimerRect:
   """Representing the onscreen rectangles"""
   def __init__(self, name, left, width, height, top, slot, settings):
      # maximum, is available time per day, currently 3 hours
      # rect is the rectangle (upper left corner, width and height)
      # mapped to this screen area
      self.maximum = top
      # print height, top
      self.rect = (left + (width/20) * (slot * 3 + 1), height/3, width/7, height)
      self.name = name
      self.font = settings.get_font()
      # print self.name, self.rect

   def timeFormat(self, time_value, mode=0):
      hours = time_value/3600
      minutes = (time_value % 3600)/60
      seconds = time_value % 60
      if(mode > 0):
         if(hours > 0):
            time_string = ' {}h {:0>2}m '.format(hours, minutes)
         else:
            time_string = '  {:0>2}m  '.format(minutes)
      else:
         if(hours > 0):
            time_string = ' {}:{:0>2}:{:0>2} '.format(hours, minutes, seconds)
         else:
            time_string = '  {:0>2}:{:0>2}  '.format(minutes, seconds)

      return time_string

# redefined drawIt to just draw colored rectangles in certain places
# as the functionality of Total, Turn, and Break rects is different
# top and bottom should be # of minutes

   def drawit(self, screen, top, bottom, color):
      
      y1 = top * (self.rect[3])/self.maximum
      y2 = bottom * (self.rect[3])/self.maximum
      draw_box = Rect(self.rect[0], self.rect[1] + self.rect[3] - y2, self.rect[2], y2 - y1)
         
      gradient.fill_gradient(screen, color, (0.66 * color[0],0.66 * color[1], 0.66 * color[2]), draw_box, False, True)

   # draw outline in dark green
   def drawOutline(self, screen):
      color = (0, 150, 150)
      pygame.draw.rect(screen, color, self.rect, 4)


# now draw the time markers - helps if maximum is a nice increment of 6
   def drawTimes(self, screen):

      time = self.maximum/6
      font = pygame.font.SysFont(self.font, 28)
      v_increment = self.rect[3]/6
      
      for i in (0, 1, 2, 3, 4, 5):
         text = font.render(self.timeFormat(time, 1), 1, (230, 230, 235))
         textpos = text.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3] - v_increment - v_increment * i))
         screen.fill(TIMEBACKGROUND, textpos)
         screen.blit(text, textpos)
         time = time + self.maximum/6

#      Total time detail readout, seems unnecessary         
#      text = font.render(self.timeFormat(self.time, 0), 1, (220, 250, 235))
#      textpos = text.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3] + 65))
#      screen.fill(TIMEBACKGROUND, textpos)
#      screen.blit(text, textpos)

      font = pygame.font.SysFont(self.font, 28)
      text = font.render(self.name, 1, (220, 250, 235))
      textpos = text.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3] + 25))
      screen.blit(text, textpos)



#----- TimerRect Class end of definition ----------------------------------------------------------------------
