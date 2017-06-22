import pygame, sys,os, math, audio_queue, timer_rect, grid_menu, time
from pygame.locals import *

#=========================================================================
# Screen init and setup
pygame.init()

# time speedup factor for testing
speedup = 1

def input(events):
   for event in events: 
      if event.type == QUIT:
         sys.exit(0) 
      if event.type == KEYDOWN:
         if event.key == K_1:
            print ("Key 1")
         if event.key == K_2:
            print ("Key 2")
         if event.key == K_ESCAPE:
            print ("Escape")
            sys.exit(0)
         else:
         # print event
            return   

# =========================================================================================================
nsecs = 0

while True:
   input(pygame.event.get())
   timex = pygame.time.get_ticks()
   time_t = time.time()
   pygame.time.wait(250)
#   pygame.time.wait(1000/speedup)
   while ((pygame.time.get_ticks() - timex) < (1000/speedup)):
      input(pygame.event.get())
   print nsecs, "time(): ", time.time() - time_t
   print "get_ticks", pygame.time.get_ticks() - timex
   nsecs += 1

pygame.exit()
