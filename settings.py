# class to hold global settings to be used by various modules

class Settings(object):
    def __init__(self, font):
        self.font = font

    def set_font(self, font):
        self.font = font

    def get_font(self):
        return self.font
    
