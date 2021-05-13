import logging
import os
import hashlib
import time

class Event(object):

    def __init__(self, view, action, device, event_count):
        self.view = view
        self.action = action
        self.device = device
        self.text = "None"
        self.count=0
        self.event_count=event_count
    
    def set_device(self,device):
        self.device = device
    
    def set_text(self,text):
        self.text = text
    
    def set_count(self,count):
        self.count = count
    
    def print_event(self):
        print("Event start=============================")
        print("Event_count:"+str(self.event_count))
        if self.view is not None:
            print("View_text:"+self.view.line)
        print("Action:"+self.action)
        print("Device:"+self.device.device_serial)
        if self.text is not None:
            print("Text:"+self.text)
        print("Event end=============================")


    
