import json
import logging
import subprocess
import time
from device import Device
from app import App
import random
import uiautomator2 as u2
from event import Event
from utils import Utils
"""
The strategy of changing setting
"""
class Injector(object):

    def __init__(self,devices,app,strategy_list,emulator_path,android_system,root_path,resource_path,testcase_count,event_num,timeout,setting_random_denominator,rest_interval,choice):
        
        self.timeout = timeout
        self.app = app
        self.devices = devices
        self.emulator_path = emulator_path
        self.android_system = android_system
        self.root_path = root_path
        self.resource_path = resource_path
        self.strategy_list = strategy_list
        self.testcase_count = testcase_count
        self.event_num = event_num
        self.setting_random_denominator = setting_random_denominator
        self.rest_interval = rest_interval
        self.utils = Utils(devices=devices)
        self.choice = choice
    
    def change_setting_before_run(self,event_count,strategy):
        print("Change setting before run")
        if strategy == "network_immediate_1":
            self.network_immediate_1()
            event = Event(None,"network_immediate_1",self.devices[1],event_count)
        elif strategy == "network_lazy_1":
            self.network_lazy_1()
            event = Event(None,"network_lazy_1",self.devices[1],event_count)
        elif strategy == "network_lazy_2":
            self.network_lazy_2()
            event = Event(None,"network_lazy_2",self.devices[1],event_count)
        elif strategy == "location_lazy_1":
            self.location_lazy_1()
            event = Event(None,"location_lazy_1",self.devices[1],event_count)
        elif strategy == "location_lazy_2":
            self.location_lazy_2()
            event = Event(None,"location_lazy_2",self.devices[1],event_count)
        elif strategy == "sound_lazy_1":
            self.sound_lazy_1()
            event = Event(None,"sound_lazy_1",self.devices[1],event_count)
        elif strategy == "battery_lazy_1":
            self.battery_lazy_1()
            event = Event(None,"battery_lazy_1",self.devices[1],event_count)
        elif strategy == "battery_immediate_1":
            self.battery_immediate_1()
            event = Event(None,"battery_immediate_1",self.devices[1],event_count)
        elif strategy == "permssion_lazy_1":
            self.permssion_lazy_1()
            event = Event(None,"permssion_lazy_1",self.devices[1],event_count)
        elif strategy == "developer_lazy_1":
            self.developer_lazy_1()
            event = Event(None,"developer_lazy_1",self.devices[1],event_count)
        elif strategy == "language":
            self.language()
            event = Event(None,"language",self.devices[1],event_count)
        elif strategy == "time":
            self.time()
            event = Event(None,"time",self.devices[1],event_count)
        else:
            event = None
        return event

    def inject_setting_during_run(self,event_count,strategy,request_flag):
        event = None
        if strategy == "network_immediate_1":
            setting_or_not = random.randint(0,self.setting_random_denominator/10)
            if setting_or_not == 0:
                print("network_immediate_1")
                self.network_immediate_1()
                event = Event(None,"network_immediate_1",self.devices[1],event_count)
        elif strategy == "network_lazy_1":
            if self.devices[1].wifi_state == True:
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
                if setting_or_not == 0:
                    print("network_lazy_1")
                    self.network_lazy_1()
                    event = Event(None,"network_lazy_1",self.devices[1],event_count)
        elif strategy == "network_lazy_2":
            if self.devices[1].wifi_state == True:
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
                if setting_or_not == 0:
                    print("network_lazy_2")
                    self.network_lazy_2()
                    event = Event(None,"network_lazy_2",self.devices[1],event_count)
        elif strategy == "sound_lazy_1":
            if self.devices[1].sound_state == True:
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
                if setting_or_not == 0:
                    print("sound_lazy_1")
                    self.sound_lazy_1()
                    event = Event(None,"sound_lazy_1",self.devices[1],event_count)
        elif strategy == "location_lazy_1":
            if self.devices[1].gps_state == True:
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
                if setting_or_not == 0:
                    print("")
                    self.location_lazy_1()
                    event = Event(None,"location_lazy_1",self.devices[1],event_count)
        elif strategy == "location_lazy_2":
            if self.devices[1].gps_state == True:
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
                if setting_or_not == 0:
                    print("location_lazy_2")
                    self.location_lazy_2()
                    event = Event(None,"location_lazy_2",self.devices[1],event_count)
        elif strategy == "display_immediate_1":
            setting_or_not = random.randint(0,self.setting_random_denominator/10)
            if setting_or_not == 0:
                print("display_immediate_1")
                self.display_immediate_1()
                event = Event(None,"display_immediate_1",self.devices[1],event_count)
        elif strategy == "display_immediate_2":
            setting_or_not = random.randint(0,self.setting_random_denominator/10)
            if setting_or_not == 0:
                print("display_immediate_2")
                self.display_immediate_2()
                event = Event(None,"display_immediate_2",self.devices[1],event_count)
        elif strategy == "permssion_lazy_1":
            if request_flag ==1:
                setting_or_not = 0
            else:
                setting_or_not = random.randint(0,self.setting_random_denominator)
            if setting_or_not == 0 and self.devices[1].permission==True:
                print("permssion_lazy_1")
                self.permssion_lazy_1()
                event = Event(None,"permssion_lazy_1",self.devices[1],event_count)
        # elif strategy == "language" :
        #     if self.devices[1].language == "ch":
        #         setting_or_not = random.randint(0,self.setting_random_denominator)
        #     else:
        #         setting_or_not = random.randint(0,self.setting_random_denominator/10)
        #     print()
        #     if setting_or_not == 0:
        #         print("language")
        #         self.language()
        #         event = Event(None,"language",self.devices[1],event_count)
        else:
            event = None
        return event
    
    def change_setting_after_run(self,event_count,strategy):
        print("Change setting after run")
        if strategy == "network_immediate_1":
            self.network_immediate_1()
            event = Event(None,"network_immediate_1",self.devices[1],event_count)
        elif strategy == "network_lazy_1":
            self.network_lazy_1()
            event = Event(None,"network_lazy_1",self.devices[1],event_count)
        elif strategy == "network_lazy_2":
            self.network_lazy_2()
            event = Event(None,"network_lazy_2",self.devices[1],event_count)
        elif strategy == "location_lazy_1":
            self.location_lazy_1()
            event = Event(None,"location_lazy_1",self.devices[1],event_count)
        elif strategy == "location_lazy_2":
            self.location_lazy_2()
            event = Event(None,"location_lazy_2",self.devices[1],event_count)
        elif strategy == "sound_lazy_1":
            self.sound_lazy_1()
            event = Event(None,"sound_lazy_1",self.devices[1],event_count)
        elif strategy == "battery_immediate_1":
            self.battery_immediate_1()
            event = Event(None,"battery_immediate_1",self.devices[1],event_count)
        elif strategy == "battery_lazy_1":
            self.battery_lazy_1()
            event = Event(None,"battery_lazy_1",self.devices[1],event_count)
        elif strategy == "permssion_lazy_1":
            self.permssion_lazy_1()
            event = Event(None,"permssion_lazy_1",self.devices[1],event_count)
        elif strategy == "developer_lazy_1":
            self.developer_lazy_1()
            event = Event(None,"developer_lazy_1",self.devices[1],event_count)
        elif strategy == "language" and self.devices[1].language=="ch":
            self.language()
            event = Event(None,"language",self.devices[1],event_count)
        elif strategy == "time" and self.devices[1].hourformat=="24h":
            self.time()
            event = Event(None,"time",self.devices[1],event_count)
        else:
            event = None
        return event
    
    def replay_setting(self,event,strategy_list):
        print("Replay setting")
        if event.action == "network_immediate_1":
            self.network_immediate_1()
        elif event.action == "network_lazy_1":
            self.network_lazy_1()
        elif event.action == "network_lazy_2":
            self.network_lazy_2()
        elif event.action == "location_lazy_1":
            self.location_lazy_1()
        elif event.action == "location_lazy_2":
            self.location_lazy_2()
        elif event.action == "sound_lazy_1":
            self.sound_lazy_1()
        elif event.action == "battery_immediate_1":
            self.battery_immediate_1()
        elif event.action == "battery_lazy_1":
            self.battery_lazy_1()
        elif event.action == "display_immediate_1":
            self.display_immediate_1()
        elif event.action == "display_immediate_2":
            self.display_immediate_2()
        elif event.action == "permssion_lazy_1":
            self.permssion_lazy_1()
        elif event.action == "developer_lazy_1":
            self.developer_lazy_1()
        elif event.action == "language":
            self.language()
        elif event.action == "time":
            self.time()
        else:
            event = None
        return event
    
    def developer_lazy_1(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        while device0(text="Apps & notifications").count<0 or device1(text="Apps & notifications").count<0:
            time.sleep(self.rest_interval*1)
        print("System")
        device1(scrollable=True,instance = 0).scroll.to(text="System")
        device1(text="System").wait(timeout=3.0)
        device1(text="System").click()
        device1(text="About emulated device").wait(timeout=3.0)
        device1(text="About emulated device").click()
        i=0
        while i < 7:
            time.sleep(self.rest_interval*1)
            device1(text="Build number").click()
            i=i+1
        device1.press("back")
        device1(text="Developer options").wait(timeout=3.0)
        device1(text="Developer options").click()
        device1(scrollable=True,instance = 0).scroll.to(text="Don’t keep activities")
        device1(text="Don’t keep activities").wait(timeout=3.0)
        device1(text="Don’t keep activities").click()
        device0.press("back")
        time.sleep(self.rest_interval*1)
        backtime =0
        while backtime <3:
            backtime=backtime+1
            device1.press("back")
            time.sleep(self.rest_interval*1)

    def network_immediate_1(self):
        device = self.devices[1]
        device.use.open_quick_settings()
        self.devices[0].use.open_quick_settings()
        device.use(description="Airplane mode").wait()
        device.use(description="Airplane mode").click()
        time.sleep(self.rest_interval*1)
        device.use(description="Airplane mode").wait()
        device.use(description="Airplane mode").click()
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        self.devices[1].wifi_state = True
        time.sleep(self.rest_interval*1)

    def network_lazy_1(self):
        device = self.devices[1]
        device.use.open_quick_settings()
        self.devices[0].use.open_quick_settings()
        if self.devices[1].wifi_state == True:
            device.use(description="Airplane mode").wait()
            device.use(description="Airplane mode").click()
            self.devices[1].wifi_state = False
        elif self.devices[1].wifi_state == False:
            device.use(description="Airplane mode").wait()
            device.use(description="Airplane mode").click()
            self.devices[1].wifi_state = True
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)

    def network_lazy_2(self):
        device = self.devices[1]
        device.use.open_quick_settings()
        self.devices[0].use.open_quick_settings()
        if self.devices[1].wifi_state == True:
            device.use(description="Wi-Fi,Wifi signal full.,No internet.,AndroidWifi").wait()
            device.use(description="Wi-Fi,Wifi signal full.,No internet.,AndroidWifi").click()
            device.use(text="ON").wait()
            device.use(text="ON").click()
            device.use(text="DONE").wait()
            device.use(text="DONE").click()
            self.devices[1].wifi_state = False
        elif self.devices[1].wifi_state == False:
            device.use(description="Wi-Fi,").wait()
            device.use(description="Wi-Fi,").click()
            device.use(text="OFF").wait()
            device.use(text="OFF").click()
            device.use(text="DONE").wait()
            device.use(text="DONE").click()
            self.devices[1].wifi_state = True
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)

    def location_lazy_1(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        while device0(text="Apps & notifications").count<0 or device1(text="Apps & notifications").count<0:
            time.sleep(self.rest_interval*1)
        print("Security & Location")
        device1(scrollable=True,instance = 0).scroll.to(text="Security & Location")
        device1(text="Security & Location").click()
        device1(text="Location").wait(timeout=3.0)
        device1(text="Location").click()
        time.sleep(self.rest_interval*1)
        if self.devices[1].gps_state == True and device1(text="ON").count >0:
            device1(text="ON").click()
            self.devices[1].gps_state = False
        elif self.devices[1].gps_state == False and device1(text="OFF").count >0:
            device1(text="OFF").click()
            self.devices[1].gps_state = True
        print("End location change")
        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        backtime =0
        device1.press("back")
        time.sleep(self.rest_interval*1)
        device1.press("back")
        time.sleep(self.rest_interval*1)
        while backtime <2:
            backtime=backtime+1
            device0.press("back")
            device1.press("back")
            time.sleep(self.rest_interval*1)

    def location_lazy_2(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        while device0(text="Apps & notifications").count<0 or device1(text="Apps & notifications").count<0:
            time.sleep(self.rest_interval*1)
        print("Security & Location")
        device0(scrollable=True,instance = 0).scroll.to(text="Security & Location")
        device0(text="Security & Location").click()
        device0(text="Location").wait(timeout=3.0)
        device0(text="Location").click()
        device1(scrollable=True,instance = 0).scroll.to(text="Security & Location")
        device1(text="Security & Location").click()
        device1(text="Location").wait(timeout=3.0)
        device1(text="Location").click()
        device0(text="Mode").wait(timeout=3.0)
        device0(text="Mode").click()
        device1(text="Mode").wait(timeout=3.0)
        device1(text="Mode").click()
        if self.devices[1].gps_state == True:
            device0(text="High accuracy").wait(timeout=3.0)
            device0(text="High accuracy").click()
            device0(text="AGREE").wait(timeout=3.0)
            if device0(text="AGREE").count>0:
                device0(text="AGREE").click()
            device1(text="Device only").wait(timeout=3.0)
            device1(text="Device only").click()
            self.devices[1].gps_state = False
        elif self.devices[1].gps_state == False:
            device1(text="High accuracy").wait(timeout=3.0)
            device1(text="High accuracy").click()
            device1(text="AGREE").wait(timeout=3.0)
            if device1(text="AGREE").count>0:
                device1(text="AGREE").click()
            self.devices[1].gps_state = True
        time.sleep(self.rest_interval*1)
        print("End location change")
        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        backtime =0
        while backtime <4:
            backtime=backtime+1
            device0.press("back")
            device1.press("back")
            time.sleep(self.rest_interval*1)

    def sound_lazy_1(self):
        device = self.devices[1]
        device.use.open_quick_settings()
        self.devices[0].use.open_quick_settings()
        if self.devices[1].sound_state == True:
            device.use(description="Do not disturb.").wait()
            device.use(description="Do not disturb.").click()
            device.use(text="OFF").wait()
            device.use(text="OFF").click()
            device.use(text="DONE").wait()
            device.use(text="DONE").click()
            self.devices[1].sound_state = False
        elif self.devices[1].sound_state == False:
            device.use(text="Alarms only").wait()
            device.use(text="Alarms only").click()
            device.use(text="ON").wait()
            device.use(text="ON").click()
            device.use(text="DONE").wait()
            device.use(text="DONE").click()
            self.devices[1].sound_state = True
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)

    def battery_immediate_1(self):
        device = self.devices[1]
        device.use.open_quick_settings()
        self.devices[0].use.open_quick_settings()
        if self.devices[1].battery_state == False:
            device.use(description="Battery Saver").wait()
            device.use(description="Battery Saver").click()
            device.use(description="Battery Saver").wait()
            device.use(description="Battery Saver").long_click()
            device.use(description="More options").wait()
            device.use(description="More options").click()
            device.use(className="android.widget.RelativeLayout",instance=0).wait()
            device.use(className="android.widget.RelativeLayout",instance=0).click()
            device.use(text="Not optimized").wait()
            device.use(text="Not optimized").click()
            device.use(text="All apps").wait()
            device.use(text="All apps").click()
            device.use(scrollable=True,instance = 1).scroll.to(text=self.app.app_name)
            device.use(scrollable=True,instance = 1).scroll.to(text=self.app.app_name)
            device.use(text=self.app.app_name).click()
            device.use(text=self.app.app_name).click()
            device.use(text="Don’t optimize").wait()
            device.use(text="Don’t optimize").click()
            device.use(text="DONE").wait()
            device.use(text="DONE").click()
            self.devices[1].battery_state = True
        elif self.devices[1].battery_state == True:
            device.use(description="Battery Saver").wait()
            device.use(description="Battery Saver").click()
            device.use(description="Battery Saver").wait()
            device.use(description="Battery Saver").long_click()
            device.use(description="More options").wait()
            device.use(description="More options").click()
            device.use(className="android.widget.RelativeLayout",instance=0).wait()
            device.use(className="android.widget.RelativeLayout",instance=0).click()
            device.use(text="Not optimized").wait()
            device.use(text="Not optimized").click()
            device.use(text="All apps").wait()
            device.use(text="All apps").click()
            device.use(scrollable=True,instance = 1).scroll.to(text=self.app.app_name)
            device.use(scrollable=True,instance = 1).scroll.to(text=self.app.app_name)
            device.use(text=self.app.app_name).click()
            device.use(text=self.app.app_name).click()
            device.use(text="Optimize").wait()
            device.use(text="Optimize").click()
            device.use(text="DONE").wait()
            device.use(text="DONE").click()
            self.devices[1].battery_state = False
        
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)

    def battery_lazy_1(self):
        device = self.devices[1]
        device.use.open_quick_settings()
        self.devices[0].use.open_quick_settings()
        if self.devices[1].battery_state == True:
            device.use(description="Battery Saver").wait()
            device.use(description="Battery Saver").click()
            self.devices[1].battery_state = False
        elif self.devices[1].battery_state == False:
            device.use(description="Battery Saver").wait()
            device.use(description="Battery Saver").click()
            self.devices[1].battery_state = True
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
    
    def display_immediate_2(self):
        self.devices[1].use(resourceId="com.android.systemui:id/recent_apps").long_click()
        time.sleep(self.rest_interval*1)
        self.devices[1].use(resourceId="com.android.systemui:id/recent_apps").long_click()

    def display_immediate_1(self):
        device = self.devices[1]
        orientation1=self.devices[0].use.orientation
        device.use.set_orientation("n")
        device.use.set_orientation("l")
        device.use.set_orientation(orientation1)
        time.sleep(self.rest_interval*1)
    
    def permssion_lazy_1(self):
        last_activity = self.devices[1].use.app_current()['activity']
        
        if self.android_system == "emulator8":
            self.change_permission_emulator8()
        self.devices[1].permission=False

        applist=["com.dragon.read"]
        self.devices[1].use.wait_activity(last_activity, timeout=5)
        current_activity=self.devices[1].use.app_current()['activity']
        if self.app.package_name in applist or (self.choice != 2 and last_activity != current_activity):
            for device in self.devices:
                print("permission restart")
                device.stop_app(self.app)
    
    def change_permission_emulator8(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        while device0(text="Apps & notifications").count<0 or device1(text="Apps & notifications").count<0:
            time.sleep(self.rest_interval*1)
        print("Apps & notifications")
        device0(text="Apps & notifications").click()
        device1(text="Apps & notifications").click()
        device0(text="App info").wait(timeout=3.0)
        device1(text="App info").wait(timeout=3.0)
        device0(text="App info").click()
        device1(text="App info").click()
        device0(scrollable=True,instance = 1).scroll.to(text=self.app.app_name)
        device1(scrollable=True,instance = 1).scroll.to(text=self.app.app_name)
        device0(text=self.app.app_name).click()
        device1(text=self.app.app_name).click()
        device0(scrollable=True,instance = 0).scroll.to(text="Permissions")
        device1(scrollable=True,instance = 0).scroll.to(text="Permissions")
        device0(text="Permissions").click()
        device1(text="Permissions").click()
        time.sleep(self.rest_interval*1)
        while device0(text="OFF",className="android.widget.Switch").count>0:
            try:
                device0(text="OFF",className="android.widget.Switch").click()
            except:
                continue
        while device1(text="ON",className="android.widget.Switch").count>0:
            try:
                device1(text="ON",className="android.widget.Switch").click()
            except:
                continue
        print("End Permissions change")
        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        backtime = 0
        while backtime <5:
            backtime=backtime+1
            device0.press("back")
            device1.press("back")
            time.sleep(self.rest_interval*1)
    
    def language(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        if self.devices[1].language == "en":
            time.sleep(self.rest_interval*1)
            print("System")
            device1(scrollable=True,instance = 0).scroll.to(text="System")
            device1(text="System").click()
            device1(text="Gboard").wait(timeout=3.0)
            device1(text="Gboard").click()
            device1(text="Languages").wait(timeout=3.0)
            device1(text="Languages").click()
            device1(text="Add a language").wait()
            device1(text="Add a language").click()
            device1(scrollable=True,instance = 0).scroll.to(text="简体中文")
            device1(text="简体中文").wait(timeout=3.0)
            device1(text="简体中文").click()
            device1(text="中国").wait(timeout=3.0)
            device1(text="中国").click()
            device1(description="More options").wait(timeout=3.0)
            device1(description="More options").click()
            time.sleep(self.rest_interval*1)
            device1.click(796, 144)
            device1(text="English (United States)").wait(timeout=3.0)
            device1(text="English (United States)").click()
            device1(description="Remove").wait(timeout=3.0)
            device1(description="Remove").click()
            device1(text="OK").wait(timeout=3.0)
            device1(text="OK").click()
            self.devices[1].language = "ch"
        elif self.devices[1].language == "ch":
            device1(scrollable=True,instance = 0).scroll.to(text="系统")
            device1(text="系统").click()
            device1(text="语言和输入法").wait(timeout=3.0)
            device1(text="语言和输入法").click()
            device1(text="语言").wait(timeout=3.0)
            device1(text="语言").click()
            device1(text="添加语言").wait()
            device1(text="添加语言").click()
            device1(text="English (United States)").click()
            device1(description="更多选项").click()
            time.sleep(self.rest_interval*1)
            device1.click(796, 144)
            device1(text="简体中文（中国）").wait(timeout=3.0)
            device1(text="简体中文（中国）").click()
            device1(description="移除").wait(timeout=3.0)
            device1(description="移除").click()
            device1(text="确定").wait(timeout=3.0)
            device1(text="确定").click()
            self.devices[1].language = "en"
        time.sleep(self.rest_interval*1)
        device0.press("back")
        device0.press("back")
        time.sleep(self.rest_interval*1)
        backtime=0
        while backtime <4:
            backtime=backtime+1
            device1.press("back")
            time.sleep(self.rest_interval*1)

    def time(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")

        if self.devices[1].hourformat == "12h":
            time.sleep(self.rest_interval*1)
            print("System")
            device1(scrollable=True,instance = 0).scroll.to(text="System")
            device1(text="System").click()
            device1(text="Date & time").wait(timeout=3.0)
            device1(text="Date & time").click()
            device1(text="Use 24-hour format").wait(timeout=3.0)
            device1(text="Use 24-hour format").click()
            self.devices[1].hourformat = "24h"
        elif self.devices[1].hourformat == "24h":
            time.sleep(self.rest_interval*1)
            print("System")
            device1(scrollable=True,instance = 0).scroll.to(text="System")
            device1(text="System").click()
            device1(text="Date & time").wait(timeout=3.0)
            device1(text="Date & time").click()
            device1(text="Use 24-hour format").wait(timeout=3.0)
            device1(text="Use 24-hour format").click()
            self.devices[1].hourformat = "12h"

        device0.press("back")
        device1.press("back")
        time.sleep(self.rest_interval*1)
        backtime=0
        while backtime <2:
            backtime=backtime+1
            device1.press("back")
            time.sleep(self.rest_interval*1)

    def clear_and_start_setting(self,device0,device1):
        device0.set_orientation("n")
        device1.set_orientation("n")
        device0.app_clear("com.android.settings")
        device1.app_clear("com.android.settings")
        device0.app_start("com.android.settings")
        device1.app_start("com.android.settings")
    
    def init_setting(self):
        if self.android_system == "emulator8":
            self.init_setting_emulator8()
    
    def init_setting_emulator8(self):
        for device in self.devices:
            device.use.open_quick_settings()
            time.sleep(self.rest_interval*1)
            lines=device.use.dump_hierarchy().splitlines()
            for line in lines:
                if 'android.widget.Switch' in line and "content-desc=\"Airplane mode" in line and "text=\"On" in line:
                    device.use(description="Airplane mode").click()
                    time.sleep(self.rest_interval*1)
                elif 'android.widget.Switch' in line and "content-desc=\"Airplane mode" in line and "text=\"On" in line:
                    device.use(description="Airplane mode").click()
                    time.sleep(self.rest_interval*1)
                elif 'android.widget.Switch' in line and "content-desc=\"Battery Saver" in line and "text=\"On" in line:
                    device.use(description="Battery Saver").click()
                    time.sleep(self.rest_interval*1)
                elif 'android.widget.TextView' in line and "text=\"Alarms only" in line:
                    device.use(text="Alarms only").click()
                    device.use(text="ON").wait()
                    device.use(text="ON").click()
                    device.use(text="DONE").wait()
                    device.use(text="DONE").click()
                    time.sleep(self.rest_interval*1)
            device.use.press("home")

    
