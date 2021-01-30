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
        if strategy == "permission":
            self.change_permission()
            event = Event(None,"setting_change_permission",self.devices[1],event_count)
        elif strategy == "network":
            self.change_network()
            event = Event(None,"setting_network",self.devices[1],event_count)
        elif strategy == "language" and self.devices[1].language == "en":
            self.change_language()
            event = Event(None,"setting_change_language",self.devices[1],event_count)
        elif strategy == "gps_off":
            self.change_gps()
            event = Event(None,"setting_change_gps",self.devices[1],event_count)
        elif strategy == "gps_mode":
            self.change_gps()
            event = Event(None,"setting_change_gps_mode",self.devices[1],event_count)
        elif strategy == "battery":
            self.change_battery()
            event = Event(None,"setting_change_battery",self.devices[1],event_count)
        elif strategy == "wifi_data":
            self.change_wifi_data()
            event = Event(None,"setting_wifi_data",self.devices[1],event_count)
        elif strategy == "battery":
            self.change_battery()
            event = Event(None,"setting_battery",self.devices[1],event_count)
        else:
            event = None
        
        return event

    def inject_setting_during_run(self,event_count,strategy,request_flag):
        event = None
        for device in self.devices:
            if device.use(text="Close app").count>0:
                device.use(text="Close app").click()
        if strategy == "screen":
            setting_or_not = random.randint(0,self.setting_random_denominator/10)
            if setting_or_not == 0:
                print("Inject screen")
                self.change_orientation(self.devices[1])
                event = Event(None,"setting_change_orientation",self.devices[1],event_count)
        elif strategy == "permission":
            if request_flag ==1:
                setting_or_not = 0
            else:
                setting_or_not = random.randint(0,self.setting_random_denominator)
            if setting_or_not == 0 and self.devices[1].permission==True:
                print("Inject permission")
                self.change_permission()
                event = Event(None,"setting_change_permission",self.devices[1],event_count)
        elif strategy == "network":
            setting_or_not = random.randint(0,self.setting_random_denominator/5)
            if setting_or_not == 0:
                print("Inject network")
                self.change_network()
                event = Event(None,"setting_network",self.devices[1],event_count)
        elif strategy == "wifi_off":
            if self.devices[1].wifi_state == True:
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
                if setting_or_not == 0:
                    print("Inject wifi off")
                    self.turn_off_wifi()
                    event = Event(None,"setting_turn_off_wifi",self.devices[1],event_count)
        elif strategy == "wifi_data":
            setting_or_not = random.randint(0,self.setting_random_denominator)
            if setting_or_not == 0:
                print("Inject wifi tp data")
                self.change_wifi_data()
                event = Event(None,"setting_wifi_data",self.devices[1],event_count)
        elif strategy == "language" :
            if self.devices[1].language == "ch":
                setting_or_not = random.randint(0,self.setting_random_denominator/10)
            else:
                setting_or_not = random.randint(0,self.setting_random_denominator)
            print()
            if setting_or_not == 0:
                print("Inject language")
                self.change_language()
                event = Event(None,"setting_change_language",self.devices[1],event_count)
        else:
            event = None
        return event
    
    def change_setting_after_run(self,event_count,strategy):
        print("Change setting after run")
        if strategy == "language" and self.devices[1].language == "ch":
            self.change_language()
            event = Event(None,"setting_change_language",self.devices[1],event_count)
        elif strategy == "wifi_off" and self.devices[1].wifi_state == False:
            self.turn_on_wifi()
            event = Event(None,"setting_turn_off_wifi",self.devices[1],event_count)
        elif self.devices[1].gps_state==False:
            self.change_gps()
            event = Event(None,"setting_change_gps",self.devices[1],event_count)
        elif self.devices[1].battery_state==True:
            self.change_battery()
            event = Event(None,"setting_change_battery",self.devices[1],event_count)
        else:
            print("strategy:"+strategy)
            print("Device(B) language:"+self.devices[1].language)
            event = None
        
        return event
    
    def replay_setting(self,event,strategy_list):
        print("Replay setting")
        if event.action == "setting_change_orientation":
            self.change_orientation(event.device)
        elif event.action == "setting_change_permission":
            self.change_permission()
        elif event.action == "setting_network":
            self.change_network()
        elif event.action == "setting_turn_off_wifi":
            self.turn_off_wifi()
        elif event.action == "setting_change_language":
            self.change_language()
    
    def clear_and_start_setting(self,device0,device1):
        device0.set_orientation("n")
        device1.set_orientation("n")
        device0.app_clear("com.android.settings")
        device1.app_clear("com.android.settings")
        device0.app_start("com.android.settings")
        device1.app_start("com.android.settings")

    def change_language(self):
        print("Change language")
        last_activity=self.devices[1].use.app_current()['activity']
        if self.android_system == "11.0":
            self.change_language_11()
        elif self.android_system == "a6s":
            self.change_language_a6s()
        elif self.android_system == "cc9e":
            self.change_language_cc9e()
        if self.choice != 2 and last_activity != self.devices[1].use.app_current()['activity']:
            for device in self.devices:
                print("language restart")
                device.stop_app(self.app)
        time.sleep(self.rest_interval*5)
    def change_language_cc9e(self):
        print("change_language_cc9e")

    def change_language_11(self):
        print("change_language_11")

    def change_language_a6s(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        if self.devices[1].language == "en":
            while device1(text="Apps").count<0:
                time.sleep(self.rest_interval*1)
            print("General management")
            device1(scrollable=True,instance = 0).scroll.to(text="General management")
            device1(text="General management").wait(timeout=3.0)
            device1(text="General management").click()
            device1(text="Language and input").wait(timeout=3.0)
            device1(text="Language and input").click()
            device1(text="Languages").wait(timeout=3.0)
            device1(text="Languages").click()
            device1(text="Add language").wait(timeout=3.0)
            device1(text="Add language").click()
            device1(text="简体中文").wait(timeout=3.0)
            device1(text="简体中文").click()
            device1(text="SET AS DEFAULT").wait(timeout=3.0)
            device1(text="SET AS DEFAULT").click()
            device1(text="删除").wait(timeout=3.0)
            device1(text="删除").click()
            device1(text="English (United States)").wait(timeout=3.0)
            device1(text="English (United States)").click()
            device1(text="删除").wait(timeout=3.0)
            device1(text="删除").click()
            device1(text="确定").wait(timeout=3.0)
            device1(text="确定").click()
        elif self.devices[1].language == "ch":
            while device1(text="应用程序").count<0:
                time.sleep(self.rest_interval*1)
            print("常规管理")
            device1(scrollable=True,instance = 0).scroll.to(text="常规管理")
            device1(text="常规管理").wait(timeout=3.0)
            device1(text="常规管理").click()
            device1(text="语言和输入").wait(timeout=3.0)
            device1(text="语言和输入").click()
            device1(text="语言").wait(timeout=3.0)
            device1(text="语言").click()
            device1(text="添加语言").wait(timeout=3.0)
            device1(text="添加语言").click()
            device1(text="English").wait(timeout=3.0)
            device1(text="English").click()
            device1(text="设为默认").wait(timeout=3.0)
            device1(text="设为默认").click()
            device1(text="DELETE").wait(timeout=3.0)
            device1(text="DELETE").click()
            device1(text="简体中文（中国）").wait(timeout=3.0)
            device1(text="简体中文（中国）").click()
            device1(text="DELETE").wait(timeout=3.0)
            device1(text="DELETE").click()
            device1(text="OK").wait(timeout=3.0)
            device1(text="OK").click()
        
        print("end language change")
        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        backtime = 0
        while backtime <4:
            backtime=backtime+1
            time.sleep(self.rest_interval*1)
            device1.press("back")
        device0.press("back")
        time.sleep(self.rest_interval*2)
        
        if self.devices[1].language == "en":
            self.devices[1].language = "ch"
        else:
            self.devices[1].language = "en"

    def change_orientation(self,device):
        # for device in self.devices:
        #     device.close_keyboard()
        orientation1=self.devices[0].use.orientation
        device.use.set_orientation("n")
        device.use.set_orientation("l")
        device.use.set_orientation(orientation1)
        time.sleep(self.rest_interval*1)

    def change_wifi_data(self):
        if self.android_system == "8.0":
            self.change_wifi_data_8()
    def change_wifi_data_8(self):
        print("change_wifi_data_8")
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(1)
        if device.use(description="Wi-Fi,Wifi signal full.,No internet.,AndroidWifi").count>0:
            device.use(description="Wi-Fi,Wifi signal full.,No internet.,AndroidWifi").click()
            device.use(text="ON").wait(timeout=3.0)
            device.use(text="ON").click()
            device.use(text="DONE").wait(timeout=3.0)
            device.use(text="DONE").click()
        elif device.use(description="Wi-Fi,").count>0:
            device.use(description="Wi-Fi,").click()
            device.use(text="OFF").wait(timeout=3.0)
            device.use(text="OFF").click()
            device.use(text="DONE").wait(timeout=3.0)
            device.use(text="DONE").click()
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")

        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)

    def turn_on_wifi(self):
        print("Turn on wifi")
        if self.android_system == "8.0":
            self.turn_on_wifi_8()
        elif self.android_system == "a6s":
            self.turn_on_wifi_a6s()
        elif self.android_system == "honor":
            self.turn_on_wifi_honor()
    
    def turn_on_wifi_honor(self):
        print("turn_on_wifi_honor")
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(self.rest_interval*1)
        device.use(description="Airplane mode").click()
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        self.devices[1].wifi_state = True

    def turn_on_wifi_8(self):
        print("turn_off_wifi_8")
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(1)
        if device.use(description="Airplane mode").count>0:
            device.use(description="Airplane mode").click()
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")

        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        self.devices[1].wifi_state = True
        return
    
    def turn_on_wifi_a6s(self):
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(self.rest_interval*1)
        lines=device.use.dump_hierarchy().splitlines()
        for line in lines:
            if 'android.widget.LinearLayout' in line and "com.android.systemui" in line and "content-desc=\"WLAN,Off." in line:
                device.use(className="android.widget.Button").click()
                device.use(text="OFF").wait(timeout=3.0)
                device.use(text="OFF").click()
                device.use(text="DONE").wait(timeout=3.0)
                device.use(text="DONE").click()
                time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        self.devices[1].wifi_state = True
        time.sleep(self.rest_interval*1)
    
    def turn_off_wifi(self):
        print("Turn off wifi")
        if self.android_system == "8.0":
            self.turn_off_wifi_8()
        elif self.android_system == "a6s":
            self.turn_off_wifi_a6s()
        elif self.android_system == "honor":
            self.turn_off_wifi_honor()
    
    def turn_off_wifi_honor(self):
        print("turn_off_wifi_honor")
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        device.use(description="Airplane mode").wait(timeout=3.0)
        device.use(description="Airplane mode").click()
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        self.devices[1].wifi_state = False
    
    def turn_off_wifi_8(self):
        print("turn_off_wifi_8")
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(1)
        if device.use(description="Airplane mode").count>0:
            device.use(description="Airplane mode").click()
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")

        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        self.devices[1].wifi_state = False
        return
    
    def turn_off_wifi_a6s(self):
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(self.rest_interval*1)
        lines=device.use.dump_hierarchy().splitlines()
        for line in lines:
            if 'android.widget.LinearLayout' in line and "com.android.systemui" in line and "content-desc=\"WLAN,On." in line:
                device.use(className="android.widget.Button").click()
                device.use(text="ON").wait(timeout=3.0)
                device.use(text="ON").click()
                device.use(text="DONE").wait(timeout=3.0)
                device.use(text="DONE").click()
                time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        self.devices[1].wifi_state = False

    def change_network(self):
        if self.android_system == "8.0":
            self.change_network_8()
        elif self.android_system == "a6s":
            self.change_network_a6s()

    def change_network_8(self):
        print("change_network_8")
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(1)
        if device.use(description="Airplane mode").count>0:
            device.use(description="Airplane mode").click()
            time.sleep(1)
            device.use(description="Airplane mode").click()
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")

        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        return

    def change_network_a6s(self):
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(self.rest_interval*1)
        lines=device.use.dump_hierarchy().splitlines()
        for line in lines:
            if 'android.widget.LinearLayout' in line and "com.android.systemui" in line and "content-desc=\"WLAN,On." in line:
                device.use(className="android.widget.Button").click()
                device.use(text="ON").wait(timeout=3.0)
                device.use(text="ON").click()
                device.use(text="DONE").wait(timeout=3.0)
                device.use(text="DONE").click()
                time.sleep(self.rest_interval*1)
                device.use(className="android.widget.Button").wait(timeout=3.0)
                device.use(className="android.widget.Button").click()
                device.use(text="OFF").wait(timeout=3.0)
                device.use(text="OFF").click()
                device.use(text="DONE").wait(timeout=3.0)
                device.use(text="DONE").click()
                time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
    
    def change_battery(self):
        print("Change battery")
        if self.android_system == "8.0":
            self.change_battery_8()
        elif self.android_system == "a6s":
            self.change_battery_a6s()
    
    def change_battery_8(self):
        print("change_battery_8")
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        device0.set_orientation("n")
        device1.set_orientation("n")
        
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(1)
        if device.use(description="Battery Saver").count>0:
            device.use(description="Battery Saver").click()
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")

        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        self.devices[1].wifi_state = True
        return
    
    def change_battery_a6s(self):
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(self.rest_interval*1)
        device.use(text="Power saving").click()
        if self.devices[1].battery_state == False:
            device.use(text="MID").wait(timeout=3.0)
            device.use(text="MID").click()
            device.use(text="APPLY").wait(timeout=3.0)
            device.use(text="APPLY").click()
        else:
            device.use(text="OFF").wait(timeout=3.0)
            device.use(text="OFF").click()
        time.sleep(self.rest_interval*5)
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        if self.devices[1].battery_state == True:
            self.devices[1].battery_state = False
        else:
            self.devices[1].battery_state = True
        return

    def change_gps(self):
        print("Change GPS")
        if self.android_system == "11.0":
            self.change_gps_11()
        elif self.android_system == "a6s":
            self.change_gps_a6s()
    
    def change_gps_11(self):
        print("change_gps_11")
        return
    
    def change_gps_a6s(self):
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(self.rest_interval*1)
        device.use(text="GPS").click()
        if self.devices[1].gps_state == True:
            device.use(text="ON").wait(timeout=3.0)
            device.use(text="ON").click()
        else:
            device.use(text="OFF").wait(timeout=3.0)
            device.use(text="OFF").click()
        device.use(text="DONE").wait(timeout=3.0)
        device.use(text="DONE").click()
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        time.sleep(self.rest_interval*1)
        device.use.press("back")
        self.devices[0].use.press("back")
        if self.devices[1].gps_state == True:
            self.devices[1].gps_state = False
        else:
            self.devices[1].gps_state = True
        return
    
    def change_permission(self):
        last_activity = self.devices[1].use.app_current()['activity']
        
        if self.android_system == "11.0":
            self.change_permission_11()
        elif self.android_system == "a6s":
            self.change_permission_a6s()
        elif self.android_system == "cc9e":
            self.change_permission_cc9e()
        self.devices[1].permission=False

        applist=["com.dragon.read"]
        self.devices[1].use.wait_activity(last_activity, timeout=5)
        current_activity=self.devices[1].use.app_current()['activity']
        if self.app.package_name in applist or (self.choice != 2 and last_activity != current_activity):
            for device in self.devices:
                print("permission restart")
                device.stop_app(self.app)
                device.start_app(self.app)
            time.sleep(1)
            if self.app.package_name=="hk.alipay.wallet" and self.devices[1].use(text="Next").count>0:
                self.devices[1].use(text="Next").wait(timeout=10.0)
                self.devices[1].use(text="Next",instance=0).click()
                self.devices[1].use(text="DENY").wait(timeout=10.0)
                self.devices[1].use(text="DENY").click()
                self.devices[1].use(text="DENY").wait(timeout=10.0)
                self.devices[1].use(text="DENY").click()
                self.devices[1].use(text="DENY").wait(timeout=10.0)
                self.devices[1].use(text="DENY").click()


    
    def change_permission_cc9e(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        while device0(text="My device").count<0 or device1(text="My device").count<0:
            time.sleep(self.rest_interval*1)
        device0(scrollable=True,instance = 0).scroll.to(text="Apps")
        device0(text="Apps").wait(timeout=3.0)
        device0(text="Apps").click()
        device1(scrollable=True,instance = 0).scroll.to(text="Apps")
        device0(text="Apps").wait(timeout=3.0)
        device1(text="Apps").click()
        device0(resourceId="Manage apps").wait(timeout=3.0)
        device0(text="Manage apps").click()
        device1(resourceId="Manage apps").wait(timeout=3.0)
        device1(text="Manage apps").click()
        device0(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
        device0(text=self.app.app_name).click()
        device1(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
        device1(text=self.app.app_name).click()
        device0(scrollable=True,instance = 0).scroll.to(text="Permissions")
        device1(scrollable=True,instance = 0).scroll.to(text="Permissions")
        device0(text="Permissions").click()
        device1(text="Permissions").click()
        time.sleep(self.rest_interval*1)
        while device0(description="Notify",resourceId="com.miui.securitycenter:id/action").count>0:
            device0(description="Notify",resourceId="com.miui.securitycenter:id/action").click()
            device0(text="Accept").wait(timeout=3.0)
            if device0(text="Accept").count>0:
                device0(text="Accept").click()
        while device1(description="Notify",resourceId="com.miui.securitycenter:id/action").count>0:
            device1(description="Notify",resourceId="com.miui.securitycenter:id/action").click()
            device1(text="Deny").wait(timeout=3.0)
            if device1(text="Deny").count>0:
                device1(text="Deny").click()
        print("End Permissions change")
        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
        backtime = 0
        while backtime < 5:
            backtime=backtime+1
            device0.press("back")
            device1.press("back")
            time.sleep(self.rest_interval*1)
    
    def change_permission_a6s(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        device0.set_orientation("n")
        device1.set_orientation("n")
        while device0(text="Apps").count<0 or device1(text="Apps").count<0:
            time.sleep(self.rest_interval*1)
        print("Apps")
        device0(text="Apps").click()
        device1(text="Apps").click()
        device0(resourceId="com.android.settings:id/action_bar").wait(timeout=3.0)
        device1(resourceId="com.android.settings:id/action_bar").wait(timeout=3.0)
        device0(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
        device1(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
        device0(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
        device1(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
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
        while backtime <4:
            backtime=backtime+1
            device0.press("back")
            device1.press("back")
            time.sleep(self.rest_interval*1)
          
    def change_permission_11(self):
        device0=self.devices[0].use
        device1=self.devices[1].use
        orientation1=device0.orientation
        orientation2=device1.orientation
        self.clear_and_start_setting(device0,device1)
        
        for device in self.devices:
            while device.use(text="Apps & notifications").count<0:
                time.sleep(self.rest_interval*1)
            device.use(text="Apps & notifications").click()
            device0(className="android.widget.Button").wait(timeout=3.0)
            if device.use(className="android.widget.Button").count>0:
                print("android.widget.Button")
                device.use(className="android.widget.Button", instance = 0).click()
            else:
                print("android:id/title")
                device.use(resourceId="android:id/title", instance = 0).click()
            time.sleep(self.rest_interval*1)
            device.use(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
            time.sleep(self.rest_interval*1)
            print("d1"+self.app.app_name)
            device.use(text=self.app.app_name).click()
            device.use(text="Permissions").click()
            
        time.sleep(self.rest_interval*1)
        lines = device0.dump_hierarchy().splitlines()
        print("allow all")
        denyfalg = 0
        for line in lines:
            if "text=\"DENIED\"" in line:
                denyfalg=1
            elif "No permissions denied" not in line and denyfalg==1 and "class=\"android.widget.TextView\" package=\"com.google.android.permissioncontroller\"" in line:	
                textnum = line.find('text=')
                text = line[textnum+6:]
                textnum = text.find('\"')
                text = text[:textnum]
                try:
                    device0(text=text).click()
                    time.sleep(self.rest_interval*1)
                    if device0(className="android.widget.RadioButton").count<1:
                        device0(resourceId="android:id/title").click()
                        time.sleep(self.rest_interval*1)
                        device0(className="android.widget.RadioButton", instance = 0).click()
                        device0.press("back")
                        device0.press("back")
                        time.sleep(self.rest_interval*1)
                    else:
                        device0(className="android.widget.RadioButton", instance = 0).click()
                        device0.press("back")
                        time.sleep(self.rest_interval*1)
                except:
                    print("false")
        lines2 = device1.dump_hierarchy().splitlines()
        print("deny all")
        denyfalg = 0
        for line in lines2:
            if "text=\"ALLOWED\"" in line:
                denyfalg=1
            elif "text=\"DENIED\"" in line:
                denyfalg=2
            elif "No permissions allowed" not in line and denyfalg==1 and "android:id/title\" class=\"android.widget.TextView\" package=\"com.google.android.permissioncontroller\"" in line:
                textnum = line.find('text=')
                text = line[textnum+6:]
                textnum = text.find('\"')
                text = text[:textnum]
                device1(text=text).click()
                time.sleep(self.rest_interval*1)
                if device1(className="android.widget.RadioButton").count<1:
                    device1(resourceId="android:id/title").click()
                    time.sleep(self.rest_interval*1)
                    device1(resourceId="com.android.permissioncontroller:id/deny_radio_button").click()
                    time.sleep(self.rest_interval*1)
                    if device1(text="Deny anyway").count>0:
                        device1(text="Deny anyway").click()
                    time.sleep(self.rest_interval*1)
                    device1.press("back")
                    device1.press("back")
                else:
                    device1(resourceId="com.android.permissioncontroller:id/deny_radio_button").click()
                    time.sleep(self.rest_interval*1)
                    if device1(text="Deny anyway").count>0:
                        device1(text="Deny anyway").click()
                    time.sleep(self.rest_interval*1)
                    device1.press("back")
                time.sleep(self.rest_interval*1)
                
        print("end Permissions change")
        time.sleep(self.rest_interval*2)
        backtime = 0
        while backtime <4:
            backtime=backtime+1
            device0.press("back")
            device1.press("back")
            time.sleep(self.rest_interval*1)
        device0.set_orientation(orientation1)
        device1.set_orientation(orientation2)
    
    def init_setting(self):
        print("init setting")
        if self.android_system == "11.0":
            self.init_setting_11()
        elif self.android_system == "a6s":
            self.init_setting_a6s()
        elif self.android_system == "honor":
            self.init_setting_honor()
        elif self.android_system == "8.0":
            self.init_setting_8()
    
    def init_setting_8(self):
        for device in self.devices:
            device.use.open_quick_settings()
            time.sleep(self.rest_interval*1)
            if device.use(description="Wi-Fi,Wifi signal full.,No internet.,AndroidWifi").count>0:
                device.use(description="Wi-Fi,Wifi signal full.,No internet.,AndroidWifi").click()
                device.use(text="ON").wait(timeout=3.0)
                device.use(text="ON").click()
                device.use(text="DONE").wait(timeout=3.0)
                device.use(text="DONE").click()
            elif device.use(description="Wi-Fi,").count>0:
                device.use(description="Wi-Fi,").click()
                device.use(text="OFF").wait(timeout=3.0)
                device.use(text="OFF").click()
                device.use(text="DONE").wait(timeout=3.0)
                device.use(text="DONE").click()
            device.use.press("back")
            time.sleep(self.rest_interval*1)
            device.use.press("back")

    def init_setting_honor(self):
        for device in self.devices:
            device.use.open_quick_settings()
            time.sleep(self.rest_interval*1)
            lines=device.use.dump_hierarchy().splitlines()
            for line in lines:
                if 'android.widget.Switch' in line and "text=\"On\"" in line and "content-desc=\"Airplane mode" in line:
                    device.use(description="Airplane mode").click()
                    time.sleep(self.rest_interval*1)
            device.use.press("home")

    def init_setting_a6s(self):
        for device in self.devices:
            device.use.open_quick_settings()
            time.sleep(self.rest_interval*1)
            lines=device.use.dump_hierarchy().splitlines()
            for line in lines:
                if 'android.widget.TextView' in line and "com.android.systemui" in line and "text=\"Portrait\"" in line:
                    device.use(text="Portrait").click()
                    device.use(text="OFF").click()
                    device.use(text="DONE").click()
                    time.sleep(self.rest_interval*1)
                elif 'android.widget.LinearLayout' in line and "com.android.systemui" in line and "content-desc=\"WLAN,Off.," in line:
                    device.use(description="WLAN,Off.,").click()
                    time.sleep(self.rest_interval*1)
            device.use.press("home")
    
    def init_setting_11(self):
        for device in self.devices:
            device.use.open_quick_settings()
            time.sleep(self.rest_interval*1)
            lines=device.use.dump_hierarchy().splitlines()
            for line in lines:
                if 'android.widget.Switch' in line and "screen" in line and "text=\"Off\"" in line:
                    device.use(description="Auto-rotate screen").click()
                    time.sleep(self.rest_interval*1)
                elif 'android.widget.Switch' in line and "Disturb" in line and "text=\"On\"" in line:
                    device.use(text="Do Not Disturb").click()
                    time.sleep(self.rest_interval*1)
                elif 'android.widget.Switch' in line and "Battery Saver" in line and "text=\"On\"" in line:
                    device.use(text="Battery Saver").click()
                    time.sleep(self.rest_interval*1)
            device.use.press("home")
        print("end initialization")
