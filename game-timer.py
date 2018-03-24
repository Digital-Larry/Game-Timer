import pygame, sys, os, datetime, settings, player, gradient, inputbox

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
      self.screen_width = 1024
      self.screen_height = 768
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
      self.appWarning = ""
      QuitWarning = 0
      CurrentPlayer = 0
      # =========================================================================================================
      # font = pygame.font.Font(None, 32)
      window = pygame.display.set_mode((self.screen_width, self.screen_height))
      pygame.display.set_caption('Video Game Timer')

      # initialize players
      self.Player1 = player.Player('Martin', "sounds/player-1.wav", self.screen, 1, 2, "1", self.settings)
      self.Player1.reset()

      self.Player2 = player.Player('Reed', "sounds/player-2.wav", self.screen, 2, 2, "2", self.settings)
      self.Player2.reset()

      self.clear_background()

   def clear_background(self):
      gradient.fill_gradient(self.screen, (250,250,250), (0,0,180))
      self.Player1.update()
      self.Player2.update()


   def input(self, events):
      global QuitWarning
      global ResetWarning
      global CurrentPlayer
      for event in events: 
         if event.type == QUIT:
            sys.exit(0) 
         if event.type == KEYDOWN:
            self.MenuTimeOut = 5
            self.clearAppWarning()
            if event.key == K_1:
               #print ("Key 1")
               CurrentPlayer = self.Player1
               self.Player2.clearMenu(self.screen)
               CurrentPlayer.AddPause(0)
               pygame.display.flip()
            elif event.key == K_2:
               #print ("Key 2")
               CurrentPlayer = self.Player2
               self.Player1.clearMenu(self.screen)
               CurrentPlayer.AddPause(0)
               pygame.display.flip()
            elif ((event.key == K_3)):
               print ("Key 3")
               self.Player1.AddTurn(10)
               self.Player2.AddTurn(10)
            # 3 and 6 set turns of 30 and 60 minutes
            elif ((event.key == K_4)):
               print ("Key 4")
               self.Player1.AddTurn(30)
               self.Player2.AddTurn(30)
            elif ((event.key == K_5)):
               print ("Key 5")
               self.Player1.AddTurn(45)
               self.Player2.AddTurn(45)
            elif (event.key == (K_6)):
               print ("Key 6")
               self.Player1.AddTurn(60)
               self.Player2.AddTurn(60)
            # 8 and 6 set breaks of 30 and 60 minutes
            elif ((event.key == K_7)):
               print ("Key 7")
               self.Player1.AddBreak(30)
               self.Player2.AddBreak(30)
            elif ((event.key == K_8)):
               print ("Key 8")
               self.Player1.AddBreak(60)
               self.Player2.AddBreak(60)
            elif (event.key == (K_9)):
               print ("Key 9")
               self.Player1.AddBreak(90)
               self.Player2.AddBreak(90)
            elif (event.key == (K_0)):
               print ("Key 0")
               self.Player1.AddBreak(120)
               self.Player2.AddBreak(120)
# handle "Y" key - modal response, wish I could figure out a better way to handle this!
            elif (event.key == K_y):
               #print ("Key Y")
               if (QuitWarning == 1):
                  sys.exit(0)
               if (ResetWarning == 1):
                  self.Player1.reset()
                  #
                  self.Player2.reset()
                  #
                  ResetWarning = 0
                  self.clearAppWarning()
            elif event.key == K_ESCAPE:
               self.setAppWarning("Quit? (Y/N)")
               CurrentPlayer = 0
               QuitWarning = 1
            elif event.key == K_PLUS:           
               fontIndex = fontIndex + 1
               self.font = fontList[fontIndex]
               print "plus", fontIndex, self.font
            elif event.key == K_r:
               self.setAppWarning( "Reset? (Y/N)")
               CurrentPlayer = 0
               ResetWarning = 1
               
            if CurrentPlayer != 0:
               CurrentPlayer.MenuKey(event.key)
               CurrentPlayer.showMenu(self.screen)
               pygame.display.flip()
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
   #      fg = (110, 210, 160)
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
      font = pygame.font.SysFont(self.settings.get_font(), 52)
      fg = (220, 250, 235)
      d = datetime.datetime.now()
      text = font.render(' {:>2}:{:0>2}:{:0>2} '.format((d.hour % 12),d.minute,d.second), 1, fg, (30, 30, 200))
      textpos = text.get_rect()
      textpos.centerx = self.screen_width/2
      textpos.centery = 40
      self.screen.blit(text, textpos)

   def run(self):
      CurrentPlayer = 0
      self.MenuTimeOut = 5

      while True:      
         self.input(pygame.event.get())
         timex = pygame.time.get_ticks()
# changed from using get_ticks() to datetime.now(), seems more accurate
#         while ((pygame.time.get_ticks() - timex) < (1000/SPEEDUP)):

         d = datetime.datetime.now().second    
         while (datetime.datetime.now().second == d):
            self.input(pygame.event.get())

         start = datetime.datetime.now()
         # time out of onscreen menu if no key activity for 5 seconds
         if self.MenuTimeOut > 0:
            self.MenuTimeOut -= 1
#            print self.MenuTimeOut
            
         else:
            self.Player1.MenuDepth = 0
            self.Player1.Menu.clearMenu(self.screen, self.Player1.menu_key)
            self.Player2.MenuDepth = 0
            self.Player2.Menu.clearMenu(self.screen, self.Player2.menu_key)
            
         self.Player1.dec()
         self.Player2.dec()
         self.showTime()
         self.showAppWarning()
         
         # print end - start        
         pygame.display.flip()
         end = datetime.datetime.now()

      pygame.exit()

# =========================== Create App and then run it!
app = App()
app.run()
