import pygame, sys, os
from pygame.locals import *
   
# =============================================================================================      
class SoundQueue:
   def __init__(self):
      self.queue = []      # used to hold queue of sounds to be played
      self.playing = 0
      Channels = pygame.mixer.get_num_channels()
      print "Channels =", Channels
      self.SoundChannel = pygame.mixer.Channel(0)
      
   def AddSound(self, sound):
      # input sound list is tuple of ("Sound name", "file name")
      # what gets added to the list is the Sound Name and the handle to the sound file
      print sound
      self.queue.append(pygame.mixer.Sound(sound))

   def PlayAll(self):
      for x in self.queue:
         while self.SoundChannel.get_queue() <> None:
            print "waiting..."   
         print "Queueing sound: ", x
         self.SoundChannel.queue(x)    

#=========================================================================
SoundList = (("One", "one.wav"), ("Two", "two.wav"), ("Three", "three.wav"), ("Four", "four.wav"), ("Five", "five.wav"))
PhoneNumber = (("3", "three.wav"), ("5", "five.wav"), ("3", "three.wav"), ("5", "five.wav"), ("0", "ten.wav"), ("3", "three.wav"), ("5", "five.wav"))

# Screen init and setup
pygame.init()
window = pygame.display.set_mode((320, 240))
pygame.display.set_caption('Audio Queue Test')

# Sound init


Queue = SoundQueue()

for x in SoundList:
   # print x
   Queue.AddSound(x[1])

Number = SoundQueue()

for x in PhoneNumber:
   Number.AddSound(x[1])                                                                                                                                                                             

# ==== start of actual code initialization

def input(events):
   for event in events: 
      if event.type == QUIT:
         sys.exit(0) 
      if event.type == KEYDOWN:
         # print " (input)key = ", event.key
         if event.key == K_LEFT:
            #print ("Key Left")
            return event.key
         if event.key == K_RIGHT:
            #print ("Key Right")
            return event.key
         if event.key == K_UP:
            #print ("Key Up")
            return event.key
         if event.key == K_DOWN:
            #print ("Key Down")
            return event.key
         if event.key == K_F2:
            print ("F2")
            Queue.PlayAll()
            return event.key
         if event.key == K_F3:
            print ("F3")
            Number.PlayAll()
            return event.key
         if event.key == K_F4:
            print ("F4")
            Number.PlayAll()
            Queue.PlayAll()
            return event.key
         if event.key == K_ESCAPE:
            #print ("Escape")
            sys.exit(0)
      else:
         # print event
         return

while True:
      key = input(pygame.event.get())
      # if key <> "None": print key
      
pygame.exit()
print "All done!"
