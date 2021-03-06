import pygame, sys, os, audio_queue, datetime, timer_rect, grid_menu, settings

from pygame.locals import *

# of minutes for each type of timer rectangle per player
MAXTOTAL = 360
MAXTURN = 60
MAXBREAK = 180
# number of seconds for total above which it is shown as red
TOTALWARNINGLEVEL = 120 * 60
# use of reminder deemed controversial, annoying
REMINDER_INTERVAL = 60
# add penalty counter - idea: add 5x reminder time to break
PENALTY_MULTIPLIER = 5

RED = (220,0,0)
DRK_RED = (180,0,0)
PURPLE = (180,0,180)
BLUE = (0,0,180)
LT_BLUE = (70,100,180)
GREEN = (0,200,0)
DRK_GREEN = (0,100,0)
YELLOW = (0,200,180)
WHITE = (255, 255, 255)
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
      self.statusString = ""
      self.statusBG = GREEN
      self.statusFG = (200, 200, 200)
      # print self.width, rect_height, self.left

      self.font = settings.get_font()
      
      self.menu_key = menu_key   # this is the string representing the key you press to call up the menu
      
      self.TotalRect = timer_rect.TimerRect("Total", self.left, self.width, rect_height, MAXTOTAL * 60, 0, settings)
      self.TurnRect = timer_rect.TimerRect("Turn", self.left, self.width, rect_height, MAXTURN * 60, 1, settings)
      self.BreakRect = timer_rect.TimerRect("Break", self.left, self.width, rect_height, MAXBREAK * 60, 2, settings)

# initialize times - these will be part of player rather than timer_rect
      self.reset()
      
      self.Menu = grid_menu.GridMenu(self.left + self.width/10, rect_height + 140, input, settings)
#      self.Menu.AddLine("Add to Total", self.AddTotal, [60, 30, 15, 10, 5]) 
      self.Menu.AddLine("Stop At", self.StopAt, [60, 45, 30, 15] )
      self.Menu.AddLine("Set Turn", self.AddTurn, [60, 45, 30, 15, 10, 5, 1] )
      self.Menu.AddLine("Set Break", self.AddBreak, [180, 150, 120, 90, 60, 45, 30, 1] )
      self.Menu.AddLine("Start/Pause", self.AddPause, [0])   

      self.name_sound = audio_queue.qSound(pygame.mixer.Sound(name_wave), input)
      self.turn_over_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/your-turn-is-over.wav"), input)
      self.reminder_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/reminder.wav"), input)
      self.break_over_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/break-over.wav"), input)
      self.ten_minute_warning_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/ten-minute-warning.wav"), input)
      self.ten_minute_message_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/ten-minutes-remaining.wav"), input)
      self.five_minute_warning_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/five-minute-warning.wav"), input)
      self.five_minute_message_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/five-minutes-until-break.wav"), input)
      self.two_minute_warning_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/two-minute-warning.wav"), input)
      self.two_minute_message_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/two-minutes-until-break.wav"), input)
      self.penalty_warning_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/in-two-minutes-your-break-will-be-extended.wav"), input)
      self.penalty_message_sound = audio_queue.qSound(pygame.mixer.Sound("sounds/your-break-has-been-extended.wav"), input)

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
      self.setStatus("Ready", WHITE, BLUE)
      
   # reset clears all counters
   def reset(self):
      self.increment = 0
      self.reminder = -1
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

   def setStatus(self, string, fg, bg):
      self.statusString = string
      self.statusFG = fg
      self.statusBG= bg

   def showStatus(self):
#      print "Status colors: ", self.statusFG, self.statusBG
      font = pygame.font.SysFont(self.font, 32)
      text = font.render('{:^30}'.format(self.statusString), 1, self.statusFG, self.statusBG)
      textpos = text.get_rect()
      # print self.name, textpos, textpos.centerx
      textpos.centerx = self.left + self.width/4
      textpos.centery = STATUS_YPOS
      # print self.name, textpos, textpos.centerx, textpos.centery
      self.surface.blit(text, textpos)

   def showReminders(self):
      fg = (252, 252, 235)
      bg = (200, 15, 15)
      if self.breakTimePenalty > 0:
         self.setStatus('Penalty: {:^}:00'.format(self.breakTimePenalty / 60), fg, bg)
      
   def update(self):
      self.updateTotal()
      self.updateTurn()
      self.updateBreak()
      self.showName(BLUE)
      self.showStatus()
#

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
          self.TotalRect.drawit(self.surface, TOTALWARNINGLEVEL, min(MAXTOTAL * 60, self.totalTime), (250,0,0))
      else:
          self.TotalRect.drawit(self.surface, 0, self.totalTime, (0,250,0))

      if (self.totalTime > MAXTOTAL * 60):
          self.status("Time to stop!!!!")

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
      self.BreakRect.drawit(self.surface, self.BreakRect.maximum, self.breakTime + self.breakTimePenalty, (0,0,215))

      if(self.breakTime == 0 and self.breakTimePenalty > 0):
#         print "breakTime, breakTimePenalty:"
#         print self.breakTime, self.breakTimePenalty
         
         self.BreakRect.drawit(self.surface, self.breakTimePenalty, 0, (215,0,215))
         
      if(self.breakTimeLeft > self.breakTimePenalty):
      # we need to draw a rectangle
#         print "breakTime, breakTimePenalty, breakTimeLeft:"
#         print self.breakTime, self.breakTimePenalty, self.breakTimeLeft
         
         self.BreakRect.drawit(self.surface, self.breakTime, self.breakTimeLeft, (0,215,0))
         self.BreakRect.drawit(self.surface, self.breakTimeLeft, self.breakTimePenalty, (215,0,0))
         self.BreakRect.drawit(self.surface, self.breakTimePenalty, 0, (215,0,215))
      else:
         self.BreakRect.drawit(self.surface, self.breakTime, self.breakTimeLeft, (0,215,0))
         self.BreakRect.drawit(self.surface, self.breakTimeLeft, 0, (215,0,0))
         
      self.BreakRect.drawOutline(self.surface)
      self.BreakRect.drawTimes(self.surface)
      self.showTime(self.BreakRect, self.breakTimeLeft)
      return
        
   def StopAt(self, minutes):
      d = datetime.datetime.now()
      minuet = d.minute
      seconds = d.second
#      print d, "Minutes: ", minuet, "Seconds: ", seconds
      
      if minuet > minutes:
         turn = (60 - minuet) + minutes
      else:
         turn = minutes - minuet

      tsec = 60 - seconds

#      adjust for case where seconds not = 0, have to subtrat 1 from minutes  
      if seconds > 0:
         turn = turn -1
         
      m = turn * 60 + tsec

#      print "Turn =", m
      self.AddTurnSec(m)

   def AddTurn(self, minutes):
      self.AddTurnSec(minutes * 60)

   def AddTurnSec(self, seconds):
      fg = (200, 200, 200)
      bg = (20, 225, 20)
      if self.breakTimeLeft > 0:
         self.setStatus("Wait until break is over!", fg, bg)
         return
      else:
#     TimeStarted not currently used
#         self.TimeStarted = datetime.datetime.now()
#         d = datetime.datetime.now()
#         print d
         self.turnTime = seconds
         self.turnTimeLeft = self.turnTime
         self.reminder = -1      # set to -1 so we can determine that turn just ended, vs. in reminder loop
         self.reminders = 0
         self.breakTimePenalty = 0
         self.increment = 1
         if self.increment > 0:
            fg = (200, 200, 200)
            bg = (20, 20, 225)
            self.setStatus(" Taking turn! ", fg, bg)
            self.showName(BLUE)
      self.update()
      
   def AddBreak(self, minutes):
      print "Add break:", minutes, self.breakTimePenalty
      self.breakTime = minutes * 60 + self.breakTimePenalty
      self.breakTimeLeft = minutes * 60 + self.breakTimePenalty
      print "Break time:", self.breakTime
      print "Break time Left:", self.breakTimeLeft
      self.reminders = 0
      self.increment = 0
      self.BreakIncrement = 1
      if minutes > 0:
         fg = BLUE
         bg = (220, 20, 225)
         self.setStatus(" Taking a break! ", fg, bg)
         self.showName((250,0,0))
      self.update()
      
   def AddPause(self, minutes):
      if self.breakTimeLeft > 0:
         fg = (200, 200, 200)
         bg = (220, 20, 225)
         self.setStatus("Wait until break is over! ", fg, bg)
         return
      if self.increment == 0:
         if self.turnTimeLeft > 0:
            self.reminders = 0
            self.AddBreak(0)
            self.showName(BLUE)
            fg = (20, 20, 20)
            bg = (20, 220, 20)
            self.setStatus(" Taking turn! ", fg, bg)
            self.increment = 1
         else:
             self.showReminders()
      else:
         self.increment = 0
         fg = (20, 20, 20)
         bg = (120, 20, 220)
         self.setStatus(" Paused! ", fg, bg)
         self.showName(DRK_GREEN)
      return

   # this is where we keep track of global time relationships within the game timer
   # such as the relationship between total time and turn time and break time
   # 
   def dec(self):
      if(self.reminder > 0):
         self.totalTime += self.increment         
      if(self.turnTimeLeft > 0):
         self.totalTime += self.increment
#      print "Total time = " + str(self.totalTime)     
         self.turnTimeLeft -= self.increment
#      print "Turn time left = " + str(self.turnTimeLeft)
      
      if (self.turnTimeLeft == 599):
            print self.name, "Ten minute warning!"
            self.name_sound.PlayIt()
            self.ten_minute_warning_sound.PlayIt()
            self.ten_minute_message_sound.PlayIt()
            self.showName(GREEN)

      if (self.turnTimeLeft == 299):
            print self.name, "Five minute warning!"
            self.name_sound.PlayIt()
            self.five_minute_warning_sound.PlayIt()
            self.five_minute_message_sound.PlayIt()
            self.showName(GREEN)
        
      if (self.turnTimeLeft == 119):
            print self.name, "Two minute warning!"
            self.name_sound.PlayIt()
            self.two_minute_warning_sound.PlayIt()
            self.two_minute_message_sound.PlayIt()
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
               self.two_minute_warning_sound.PlayIt()
               self.name_sound.PlayIt()
               self.turn_over_sound.PlayIt()
               fg = (200, 200, 200)
               bg = (220, 20, 20)
               self.setStatus("Turn over!", fg, bg)
               self.showName(RED)
               self.reminder = REMINDER_INTERVAL * SPEEDUP  # turn over reminder every 120 seconds
            elif(self.reminder == 0): # now we're counting down reminders, just play a reminder sound less annoying y'know 8^)
               self.reminder = REMINDER_INTERVAL * SPEEDUP  # turn over reminder every 120 seconds
               self.reminders += 1
               self.breakTimePenalty += PENALTY_MULTIPLIER * 60

               if (self.reminders % 10 == 0):
                     if( self.breakTimePenalty <= (MAXBREAK - (10 * PENALTY_MULTIPLIER)) * 60):
                        self.name_sound.PlayIt()
                        self.penalty_message_sound.PlayIt()
                        self.breakTimePenalty += 22 * 60
                        print "Adding 22 minutes"
                     else:
                        self.name_sound.PlayIt()
                        self.reminder_sound.PlayIt()
                        fg = (220, 220, 220)
                        bg = (250, 20, 20)
                        self.setStatus(" Break time already!!!", fg, bg)            
                     # print "break penalty for ", self.name, " is ", self.breakTimePenalty
                     
               self.showReminders()
               # print self.name, "reminders:", self.reminders
            else:
               self.reminder -= 1            
               # print self.name, "reminder countdown:", self.reminder
# process break time
# break over announcement will not repeat, currently
# break reminder is not used
      if self.breakTimeLeft > 0:
         self.breakTimeLeft -= self.BreakIncrement
         # announce break over ONLY if it just ended, not continuously
         if (self.breakTimeLeft == 0):
            print self.name, "Break over!"
            self.name_sound.PlayIt()
#	Don't play break over sounds, maybe they won't notice
#            self.break_over_sound.PlayIt()   
            fg = (220, 220, 220)
            bg = (20, 250, 20)
            self.setStatus(" Break over! ", fg, bg)
            self.showName(BLUE)
            self.BreakIncrement = 0
            self.breakTime = 0    # clear the break rect, since break is over
            self.breakTimePenalty = 0
#            self.BreakRect.reminder = 30 * SPEEDUP
#         else:
#            self.setStatus("Break over!")
#            self.BreakRect.reminder -= 1

      self.update()

# ================ end of Player class definition
