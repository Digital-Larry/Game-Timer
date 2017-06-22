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
      self.time = 0
      self.time_left = 0
      self.reminder = 0
      self.font = settings.get_font()
      # print self.name, self.rect

   def decrement(self, inc):
      self.time_left = max(0, self.time_left - inc)
      
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

   def drawit(self, screen):
      # draw and fill outline in blue
      pygame.draw.rect(screen, (30,30,170), self.rect, 0)

      # box = Rect(self.rect)
      # this gradient fill appears to take too long, slowing the timer down
      # gradient.fill_gradient(screen, (50,50, 250), (150,150,2520), box, False, True)

      # print self.time, self.time_left
      
      if (self.time > 0):
      # draw remaining time in green
         color = (0, 255, 0)
         y1 = ((self.maximum - self.time) * self.rect[3])/self.maximum
         y2 = ((self.maximum - self.time_left) * self.rect[3])/self.maximum

         draw_green = Rect(self.rect[0], self.rect[1] + y2, self.rect[2], self.rect[3] - y2)
         
         # print "y1 =", y1, "y2 = ", y2
         # print "Draw green:", draw_green 
#     replace this line with a gradient call
#         pygame.draw.rect(screen, color, draw_green, 0)
         gradient.fill_gradient(screen, color, (0,123,0), draw_green, False, True)

#        bgd = pygame.Surface(screen.get_size())
#        bgd.blit( gradients.vertical(bgd.get_size(), (227, 200, 53, 255), (157, 116, 2, 255)),(0,0))
#        bgd.fill((128,)*3)

         if self.time != self.time_left:
         # draw from top down in red to represent used time
            color = (255, 0, 0)
            draw_red = Rect(self.rect[0], self.rect[1] + y1, self.rect[2], (y2 - y1) + 1)
            gradient.fill_gradient(screen, color, (225,120,120), draw_red, False, True)
  #          pygame.draw.rect(screen, color, draw_red, 0)
            # print "Draw red:", draw_red

     # draw outline in dark green
      color = (0, 150, 10)
      pygame.draw.rect(screen, color, self.rect, 3)


# now draw the time markers - helps if maximum is a nice increment of 6

      time = self.maximum/6
      font = pygame.font.SysFont(self.font, 28)
      v_increment = self.rect[3]/6
      
      for i in (0, 1, 2, 3, 4, 5):
         text = font.render(self.timeFormat(time, 1), 1, (230, 230, 235))
         textpos = text.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3] - v_increment - v_increment * i))
         screen.fill(TIMEBACKGROUND, textpos)
         screen.blit(text, textpos)
         time = time + self.maximum/6
       

      font = pygame.font.SysFont(self.font, 32)
      text = font.render(self.timeFormat(self.time_left, 0), 1, (220, 250, 235))
      textpos = text.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3] + 65))
      screen.fill(TIMEBACKGROUND, textpos)
      screen.blit(text, textpos)

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
