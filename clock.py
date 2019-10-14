import pygame, sys, os, datetime, settings, gradient, inputbox

from pygame.locals import *

RED = (220,0,0)
DRK_RED = (180,0,0)
PURPLE = (180,0,180)
BLUE = (0,0,180)
LT_BLUE = (70,100,180)
GREEN = (0,200,0)
DRK_GREEN = (0,100,0)
YELLOW = (0,200,180)

STATUS_YPOS = 95

# speedup factor for testing (which doesn't work)
SPEEDUP = 10

global QuitWarning
global ResetWarning
global CurrentPlayer
# global MenuTimeOut

#=========================================================================
# Screen init and setup
class App():
   def __init__(self):
      global CurrentPlayer
      global QuitWarning
      
      pygame.init()
      list = pygame.display.list_modes()
#      print list
      
#      index = list.index((1824, 984))
#      print list, index, list[index]
      self.screen_width = 600
      self.screen_height = 200
      self.appWarning = ""
#      self.screen_width = 800
#      self.screen_height = 600
      error = pygame.display.set_mode((self.screen_width, self.screen_height))
      # print error
      # print

      if not pygame.font:
         print 'Warning, fonts disabled'
      else:
         fontList = pygame.font.get_fonts()
#         print fontList
         fontIndex = 5
         self.font = fontList[fontIndex]

      self.settings = settings.Settings("dejavusans")
      self.screen = pygame.display.get_surface() 

      # =========================================================================================================
      # font = pygame.font.Font(None, 32)
      window = pygame.display.set_mode((self.screen_width, self.screen_height))
      pygame.display.set_caption('Clock')

      self.clear_background()

   def clear_background(self):
      gradient.fill_gradient(self.screen, (250,250,250), (0,0,180))


   def input(self, events):
      global QuitWarning
      global ResetWarning
      global CurrentPlayer
      for event in events: 
         if event.type == QUIT:
            sys.exit(0) 
         if event.type == KEYDOWN:
            self.clearAppWarning()

            if event.key == K_ESCAPE:
               self.setAppWarning("Quit? (Y/N)")
               CurrentPlayer = 0
               QuitWarning = 1
            elif event.key == K_PLUS:           
               fontIndex = fontIndex + 1
               self.font = fontList[fontIndex]
               print "plus", fontIndex, self.font
            elif event.key == K_r:
               self.setAppWarning( "Reset? (Y/N)")
               ResetWarning = 1
               
            else:
            # print event
               # QuitWarning = 0
               return
            
# appWarning currently has 3 desired possibilities
# Quit? (Y/N)
# Reset? (Y/N)
# Password: **** (asterisks show up as password is entered)
# Quit? and Reset?  return "1" is "Y" is typed in, "0" otherwise
# They return immediately after the key is typed.
# Should be case insensitive
# Password waits for the user to enter the exact password
# with each key, an asterisk is printed out
# Returns when length of supplied password is reached
# so, the parameters should be:
# string (to show)
# response (match to return 1, 0 otherwise)
# case (whether it's case sensitive)
# mask (might be needed later, but all responses defined so far are masked) 

# blit(source, dest, area=None, special_flags = 0) -> Rect
# Draws a source Surface onto this Surface. The draw can be positioned with the dest argument.
# Dest can either be pair of coordinates representing the upper left corner of the source.
# A Rect can also be passed as the destination and the topleft corner of the rectangle will be
# used as the position for the blit. The size of the destination rectangle does not effect the blit.

   def setAppWarning(self, string):
      self.appWarning = string

   def showAppWarning(self):
      if(self.appWarning != ""):
         font = pygame.font.SysFont(self.settings.get_font(), 32)
         fg = (220, 250, 235)
         text = font.render('{:^16}'.format(self.appWarning), 1, fg, (235,10,10))
         textpos = text.get_rect()
         # print self.name, textpos, textpos.centerx
         textpos.centerx = self.screen_width/2
         textpos.centery = self.screen_height/2
         # print self.name, textpos, textpos.centerx, textpos.centery
         self.screen.blit(text, textpos)  

   def clearAppWarning(self):
      self.appWarning = ""
      self.clear_background()
      
   def showTime(self):
      font = pygame.font.SysFont(self.settings.get_font(), 144)
      fg = (220, 250, 235)
      d = datetime.datetime.now()
      text = font.render(' {:>2}:{:0>2}:{:0>2} '.format((d.hour % 12),d.minute,d.second), 1, fg, (30, 30, 200))
      textpos = text.get_rect()
      textpos.centerx = self.screen_width/2
      textpos.centery = 120
      self.screen.blit(text, textpos)

   def run(self):

      while True:      
         self.input(pygame.event.get())
         timex = pygame.time.get_ticks()
# changed from using get_ticks() to datetime.now(), seems more accurate
#         while ((pygame.time.get_ticks() - timex) < (1000/SPEEDUP)):

         d = datetime.datetime.now().second    
         while (datetime.datetime.now().second == d):
            self.input(pygame.event.get())

         start = datetime.datetime.now()

         self.showTime()
         self.showAppWarning()
         
         # print end - start        
         pygame.display.flip()
         end = datetime.datetime.now()

      pygame.exit()

# =========================== Create App and then run it!
app = App()
app.run()
