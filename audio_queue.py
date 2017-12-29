import pygame, sys, os
from pygame.locals import *
   
class qSound:
   def __init__(self, sound, waitloop):
      Channels = pygame.mixer.get_num_channels()
      # print "Channels =", Channels
      self.SoundChannel = pygame.mixer.Channel(0)
      self.waitloop = waitloop
      self.sownd = sound
      
   def PlayIt(self):
      i = 0
      # print self.sownd
      s = self.SoundChannel.get_queue()
      while s <> None:
            # print s
            s = self.SoundChannel.get_queue()
            i += 1
            # print "waiting..."   
            # self.waitloop(pygame.event.get()) 
            # print "return from waiting..."   
      print i, "Queueing sound: ", s
      x = self.SoundChannel.queue(self.sownd)
      # print x

# =============================================================================================      
class SoundQueue:
   def __init__(self, waitloop):
      self.queue = []      # used to hold queue of sounds to be played
      self.playing = 0
      Channels = pygame.mixer.get_num_channels()
      print "Channels =", Channels
      self.SoundChannel = pygame.mixer.Channel(0)
      self.waitloop = waitloop
      
   def AddSound(self, sound):
      # input sound list is tuple of ("Sound name", "file name")
      # what gets added to the list is the Sound Name and the handle to the sound file
      print sound
      self.queue.append(sound)

   def PlayAll(self):
      i = 0
      print "Queue length = ", len(self.queue)
      for x in self.queue:
         while self.SoundChannel.get_queue() <> None:
            i += 1
            self.waitloop(pygame.event.get()) 
            # print "waiting..."   
         print i, "Queueing sound: "
         self.SoundChannel.queue(x)    


# ==== start of actual code initialization
if __name__ == '__main__':

   def input(events):
      for event in events: 
         if event.type == QUIT:
            sys.exit(0) 
         if event.type == KEYDOWN:
            # print " (input)key = ", event.key
            if event.key == K_F2:
               print ("F2")
               Queue.PlayAll()
               return event.key
            if event.key == K_F3:
               print ("F3")
               Number.PlayAll()
               return event.key
            if event.key == K_ESCAPE:
               #print ("Escape")
               sys.exit(0)
         else:
            # print event
            return

   #=========================================================================
   SoundList = (("One", "one.wav"), ("Two", "two.wav"), ("Three", "three.wav"), ("Four", "four.wav"), ("Five", "five.wav"))
   PhoneNumber = (("3", "three.wav"), ("5", "five.wav"), ("3", "three.wav"), ("5", "five.wav"), ("0", "ten.wav"), ("3", "three.wav"), ("5", "five.wav"))

   # Screen init and setup
   pygame.init()
   window = pygame.display.set_mode((320, 240))
   pygame.display.set_caption('Audio Queue Test')

   # Sound init
   Queue = SoundQueue(input)

   for x in SoundList:
      # print x
      Queue.AddSound(pygame.mixer.Sound(x[1]))

   Number = SoundQueue(input)

   for x in PhoneNumber:
      Number.AddSound(pygame.mixer.Sound(x[1]))                                                                                                                                                                             

   while True:
      key = input(pygame.event.get())
      # if key <> "None": print key
      
   pygame.exit()
   print "All done!"
