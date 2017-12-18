import pygame, sys, os, audio_queue, timer_rect, grid_menu, settings

from pygame.locals import *

# of minutes for each type of timer rectangle per player
MAXTOTAL = 360
MAXTURN = 60
MAXBREAK = 180
# number of seconds for total above which it is shown as red
TOTALWARNINGLEVEL = 120 * 60
# use of reminder deemed controversial, annoying
REMINDER_INTERVAL = 120
# add penalty counter - idea: add 2x reminder time to break
PENALTY_MULTIPLIER = 2

RED = (220,0,0)
DRK_RED = (180,0,0)
PURPLE = (180,0,180)
BLUE = (0,0,180)
LT_BLUE = (70,100,180)
GREEN = (0,200,0)
DRK_GREEN = (0,100,0)
YELLOW = (0,200,180)
TIMEBACKGROUND = (0, 0, 60)


NAME_YPOS = 40
STATUS_YPOS = 95

# speedup factor for testing (which doesn't work)
SPEEDUP = 1

#------------------------------------------------------------------------------------------------------
# Player class routines
class Player(object):
   def __init__(self, name, name_wave, surface, slot, totalSlots, menu_key, settings):
      self.surface = surface
      # print "Width = ", surface.get_width()
      self.width = surface.get_width()
      rect_height = (surface.get_height() * 4)/7  # height of the rectangles
      self.screen_height = surface.get_height()   # height of the screen1
      self.name = name
      self.left = self.width * (slot - 1)/totalSlots
      # print self.width, rect_height, self.left

      self.font = settings.get_font()
      
      self.menu_key = menu_key   # this is the string representing the key you press to call up the menu
      
      self.TotalRect = timer_rect.TimerRect("Total", self.left, self.width, rect_height, MAXTOTAL * 60, 0, settings)
      self.TurnRect = timer_rect.TimerRect("Turn", self.left, self.width, rect_height, MAXTURN * 60, 1, settings)
      self.BreakRect = timer_rect.TimerRect("Break", self.left, self.width, rect_height, MAXBREAK * 60, 2, settings)

      self.showName(BLUE)

# initialize times - these will be part of player rather than timer_rect
      self.reset()
      
      self.Menu = grid_menu.GridMenu(self.left + self.width/10, rect_height + 140, input, settings)
#      self.Menu.AddLine("Add to Total", self.AddTotal, [60, 30, 15, 10, 5]) 
      self.Menu.AddLine("Set Turn", self.AddTurn, [60, 45, 30, 15, 1] )
      self.Menu.AddLine("Set Break", self.AddBreak, [180, 150, 120, 90, 60, 30, 1] )
      self.Menu.AddLine("Start/Pause", self.AddPause, [0])   

      self.name_sound = audio_queue.qSound(pygame.mixer.Sound(name_wave), input)
      self.turn_over_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/turn-over.wav"), input)
      self.bing_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/bing.wav"), input)
      self.time_up_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/time-up.wav"), input)
      self.break_over_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/break-over.wav"), input)
      self.five_minute_warning_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/five-minute-warning.wav"), input)
      self.two_minute_warning_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/two-minute-warning.wav"), input)
      self.bing_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/bing.wav"), input)

   def showName(self, background):
      font = pygame.font.SysFont(self.font, 52)
      name_fg = (220, 250, 235)
      text = font.render('{:^20}'.format(self.name), 1, name_fg, background)
      textpos = text.get_rect()
      # print self.name, textpos, textpos.centerx
      textpos.centerx = self.left + self.width/4
      textpos.centery = NAME_YPOS
      # print self.name, textpos, textpos.centerx, textpos.centery
      self.surface.blit(text, textpos)

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

   def MenuKey(self, key):
      self.Menu.MenuKey(key)

   def clearMenu(self, screen):
      self.Menu.clearMenu(screen, self.menu_key)

   def showMenu(self, screen):
      self.Menu.showMenu(screen)
   
   def clearStatus(self):
      status_fg = (0,0,0)
      status_bg = (0, 0, 0)
      font = pygame.font.SysFont(self.font, 32)
      text = font.render('{:^44}'.format(""), 1, status_fg, status_bg)
      textpos = text.get_rect()
      textpos.centerx = self.left + self.width/4
      textpos.centery = STATUS_YPOS
      self.surface.blit(text, textpos)

   # reset clears all counters
   def reset(self):
      self.increment = 0
      self.BreakIncrement = 0
      self.reminders = 0            # how many times the reminder has gone off
      self.totalTime = 0
      self.turnTime = 0
      self.turnTimeLeft = 0
      self.breakTime = 0
      self.breakTimeLeft = 0
      self.breakTimePenalty = 0

      self.clearStatus()
      self.showName(BLUE)

   def status(self, string):
      status_fg = (252, 252, 235)
      status_bg = (0, 175, 75)
      font = pygame.font.SysFont(self.font, 32)
      text = font.render('{:^30}'.format(string), 1, status_fg, status_bg)
      textpos = text.get_rect()
      # print self.name, textpos, textpos.centerx
      textpos.centerx = self.left + self.width/4
      textpos.centery = STATUS_YPOS
      # print self.name, textpos, textpos.centerx, textpos.centery
      self.surface.blit(text, textpos)

   def showReminders(self):
      self.status('Reminder # {:^}'.format(self.reminders))
      
   def update(self):
      self.updateTotal()
      self.updateTurn()
      self.updateBreak()

   def showTime(self, rectToShow, timeToShow):
      # now draw time value below the rectangle
      font = pygame.font.SysFont(self.font, 32)
      text = font.render(self.timeFormat(timeToShow, 0), 1, (220, 250, 235))
      textpos = text.get_rect(center=(rectToShow.rect[0] + rectToShow.rect[2]/2, rectToShow.rect[1] + rectToShow.rect[3] + 65))
      self.surface.fill(TIMEBACKGROUND, textpos)
      self.surface.blit(text, textpos)
      
      
   def updateTotal(self):
#      print "TotalRect max and Player total time:"
#      print self.TotalRect.maximum, self.totalTime
      self.TotalRect.drawit(self.surface, self.TotalRect.maximum, self.totalTime, (0,0,250))
      if (self.totalTime > TOTALWARNINGLEVEL):
          self.TotalRect.drawit(self.surface, 0, TOTALWARNINGLEVEL, (0,250,0))
          self.TotalRect.drawit(self.surface, TOTALWARNINGLEVEL, self.totalTime, (250,0,0))
      else:
          self.TotalRect.drawit(self.surface, 0, self.totalTime, (0,250,0))

      self.TotalRect.drawOutline(self.surface)
      self.TotalRect.drawTimes(self.surface)
      self.showTime(self.TotalRect, self.totalTime)

     
   def updateTurn(self):
#      print "TurnRect max and Player turn time, turn time left:"
#      print self.TurnRect.maximum, self.turnTime, self.turnTimeLeft
#      self.TurnRect.drawit(self.surface, self.TurnRect.maximum, self.turnTimeLeft, (0,0,250))
      self.TurnRect.drawit(self.surface, self.TurnRect.maximum, self.turnTime, (0,0,250))
      self.TurnRect.drawit(self.surface, self.turnTime, self.turnTimeLeft, (250,0,0))
      self.TurnRect.drawit(self.surface, self.turnTimeLeft, 0, (0,250,0))
      self.TurnRect.drawOutline(self.surface)
      self.TurnRect.drawTimes(self.surface)
      self.showTime(self.TurnRect, self.turnTimeLeft)
         
   def updateBreak(self):
      self.BreakRect.drawit(self.surface, self.BreakRect.maximum, self.breakTime, (0,0,215))
      self.BreakRect.drawit(self.surface, self.breakTime, self.breakTimeLeft, (0,215,0))
      self.BreakRect.drawit(self.surface, self.breakTimeLeft, 0, (215,0,0))
      self.BreakRect.drawOutline(self.surface)
      self.BreakRect.drawTimes(self.surface)
      self.showTime(self.BreakRect, self.breakTimeLeft)
      return
        
   def AddTurn(self, minutes):
      if self.breakTimeLeft > 0:
         self.status("Wait until break is over!")
         return
      else:
#     TimeStarted not currently used
#         self.TimeStarted = datetime.datetime.now()
         self.turnTime = minutes * 60
         self.turnTimeLeft = self.turnTime
         self.reminder = -1      # set to -1 so we can determine that turn just ended, vs. in reminder loop
         self.increment = 1
         if self.increment > 0:
            self.status(" Taking turn! ")
            self.showName(BLUE)
      self.update()
      
   def AddBreak(self, minutes):
      self.breakTime = minutes * 60
      self.breakTimeLeft = minutes *60
      self.increment = 0
      self.BreakIncrement = 1
      if minutes > 0:
         self.status(" Taking a break! ")
         self.showName((250,0,0))
      self.update()
      
   def AddPause(self, minutes):
      self.reminders = 0
      if self.breakTimeLeft > 0:
         self.status("Wait until break is over! ")
         return
      if self.increment == 0:
         if self.turnTimeLeft > 0:
            self.AddBreak(0)
            self.showName(BLUE)
            self.status(" Taking turn! ")
            self.increment = 1
         else:
             self.status(" No turn defined! ")
      else:
         self.increment = 0
         self.status(" Paused! ")
         self.showName(DRK_GREEN)
      return

   # this is where we keep track of global time relationships within the game timer
   # such as the relationship between total time and turn time and break time
   # 
   def dec(self):
      self.totalTime += self.increment
#      print "Total time = " + str(self.totalTime)
      
      self.turnTimeLeft -= self.increment
#      print "Turn time left = " + str(self.turnTimeLeft)
      
      if (self.turnTimeLeft == 299):
            print self.name, "Five minute warning!"
            self.name_sound.PlayIt()
            self.five_minute_warning_sound.PlayIt()
            self.showName(GREEN)
        
      if (self.turnTimeLeft == 119):
            print self.name, "Two minute warning!"
            self.name_sound.PlayIt()
            self.two_minute_warning_sound.PlayIt()
            self.showName(YELLOW)
        
      elif self.turnTimeLeft == 0:
         # print self.reminder unless in pause mode
         if(self.increment > 0):
            # flash name
            if ((self.reminder % 2) == 0):
               self.showName(RED)
            else:
               self.showName(BLUE)
            # manage reminder beep                  
            if(self.reminder == -1):   # it's set to -1 when turn starts, so turn just ended: say name + "turn over"
               print self.name, "Turn over!"
               self.name_sound.PlayIt()
               self.turn_over_sound.PlayIt()
               self.status("Turn over!")
               self.showName(RED)
               self.reminder = REMINDER_INTERVAL * SPEEDUP  # turn over reminder every 120 seconds
            elif(self.reminder == 0): # now we're counting down reminders, just play a bing sound less annoying y'know 8^)
               self.bing_sound.PlayIt()
               self.reminder = REMINDER_INTERVAL * SPEEDUP  # turn over reminder every 120 seconds
               self.reminders += 1
               self.showReminders()
            else:
               self.reminder -= 1            
# process break time
# break over announcement will not repeat, currently
# break reminder is not used
      if self.breakTimeLeft > 0:
         self.breakTimeLeft -= self.BreakIncrement
         # announce break over ONLY if it just ended, not continuously
         if (self.breakTimeLeft == 0):
            print self.name, "Break over!"
            self.name_sound.PlayIt()
#	Don't play braek over sounds, maybe they won't notice
#            self.break_over_sound.PlayIt()   
            self.status("Break over!")
            self.showName(BLUE)
            self.BreakIncrement = 0
            self.breakTime = 0    # clear the break rect, since break is over
#            self.BreakRect.reminder = 30 * SPEEDUP
#         else:
#            self.status("Break over!")
#            self.BreakRect.reminder -= 1

      self.update()

# ================ end of Player class definition
