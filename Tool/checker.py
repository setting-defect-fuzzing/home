import json
import logging
import subprocess
import time
from device import Device
from app import App
import uiautomator2 as u2
import time
import re
from injector import Injector
from utils import Utils

class Checker(object):
    
    def __init__(self,devices,app,strategy_list,emulator_path,android_system,root_path,resource_path,testcase_count,event_num,timeout,setting_random_denominator,rest_interval,choice):
        
        self.timeout = timeout
        self.app = app
        self.devices = devices
        self.guest_devices=self.devices[1:len(self.devices)]
        self.emulator_path = emulator_path
        self.android_system = android_system
        self.root_path = root_path
        self.resource_path = resource_path
        self.strategy_list = strategy_list
        self.testcase_count = testcase_count
        self.event_num = event_num
        self.setting_random_denominator = setting_random_denominator
        self.rest_interval = rest_interval
        self.injector = Injector(devices=devices,
                app=app,
                strategy_list=strategy_list,
                emulator_path=emulator_path,
                android_system=android_system,
                root_path=root_path,
                resource_path=resource_path,
                testcase_count=testcase_count,
                event_num=event_num,
                timeout=timeout,
                setting_random_denominator=setting_random_denominator,
                rest_interval=rest_interval,
                choice=choice)
        self.utils = Utils(devices=devices)
    
    def check_time(self,path):
        fw = open(path+"/time_bug.txt",'w',encoding='utf-8')
        time_bugs=[]
        import os
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if "5556" in name and "xml" in name:
                    xml_path=os.path.join(root, name)
                    f = open(xml_path,'r',encoding='utf-8')
                    lines=f.readlines()
                    f.close()
                    for line in lines:
                        if "text=\"" in line and self.app.package_name in line:
                            text = line[line.find("text=\"")+6:len(line)]
                            text = text[0:text.find("\"")]
                            pattern = re.search("^(1[0-2]|0?[1-9]|0):([0-5]?[0-9])$", text)
                            if pattern != None and text not in time_bugs:
                                time_bugs.append(text)
                                fw.write(xml_path+'\n')
                                fw.write(text+'\n\n')
                                fw.flush()
        fw.close()

        
    def check_language(self,path):
        fw = open(path+"/language_bug.txt",'w',encoding='utf-8')
        language_bugs=[]
        import os
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if "5556" in name and "xml" in name:
                    xml_path=os.path.join(root, name)
                    f = open(xml_path,'r',encoding='utf-8')
                    lines=f.readlines()
                    f.close()
                    for line in lines:
                        if "text=\"" in line and self.app.package_name in line:
                            text = line[line.find("text=\"")+6:len(line)]
                            text = text[0:text.find("\"")]
                            import langid
                            language_classify=langid.classify(text)
                            if "en" in language_classify[0] and text!="" and text not in language_bugs:
                                print(text)
                                language_bugs.append(text)
                                fw.write(xml_path+'\n')
                                fw.write(text+'\n\n')
                                fw.flush()
        fw.close()



    def check_keyboard(self):
        for device in self.devices:
            # device.use.set_clipboard('text', 'label')
            lines = device.state.lines
            if "com.sohu.inputmethod.sogou:id/imeview_keyboard" in lines or "com.baidu.input_huawei" in lines:
                print("close_keyboard")
                device.close_keyboard()
    
    def check_samestate(self):
        if self.devices[0].state.same_but_not_language(self.devices[1].state):
            return True
        return False
    
    def check_foreground(self):
        packagelist=[self.app.package_name,"com.google.android.permissioncontroller","com.android.packageinstaller","com.android.permissioncontroller"]
        lines = self.devices[0].use.dump_hierarchy()
        for package in packagelist:
            if package in lines:
                return True
        return False
    
    def check_start(self,times,strategy):
        try:
            if self.app.package_name == "fr.free.nrw.commons" and times==0:
                print("Feimao start 0")
                time.sleep(self.rest_interval*20)
                for device in self.devices:
                    device.use(scrollable=True).scroll.horiz.toEnd(max_swipes=50)
                    device.use(text="YES!").wait(timeout=10.0)
                    device.use(text="YES!",instance=0).click()
                    device.use(text="Skip").wait(timeout=10.0)
                    device.use(text="Skip",instance=0).click()
                    device.use(text="YES").wait(timeout=10.0)
                    device.use(text="YES",instance=0).click()
                print("Feimao start end 0")
            else:
                print("Other start")
                time.sleep(self.rest_interval*2)
        except:
            print("")

    def check_setting_request(self):
        flag=False
        for device in self.guest_devices:
            if device.strategy == "permssion_lazy_1":
                if self.check_permission_request(device):
                    self.devices[1].permission=True
                    return True
            elif device.strategy == "network_lazy_1":
                if self.check_network_request(device):
                    return True
            elif device.strategy == "location_lazy_1":
                if self.check_location_request(device):
                    return True
        return flag
    
    def check_location_request(self,device):
        Flag = False
        gpslist = ["location","gps","位置","加载","connection"]
        requestlist = ["unavailable","try again","开启","检查","失败","重新","重试","not available","not enabled"]
        lines2 = device.use.dump_hierarchy()
        if (self.containsAny(lines2.lower(), gpslist) and self.containsAny(lines2.lower(), requestlist)):
            print("Allow location")
            if device.use(text="SETTINGS").count > 0:
                device.use(text="SETTINGS").click()
                device.use(text="OFF").wait()
                device.use(text="OFF").click()
                device.use.press("back")
                self.devices[1].gps_state = True
            else:
                self.injector.location_lazy_1()
            Flag = True
        return Flag

    def check_notification_request(self,device):
        Flag = False
        notificationlist = ["通知"]
        requestlist = ["unavailable","try again","开启"]
        lines2 = device.use.dump_hierarchy()
        if (self.containsAny(lines2.lower(), notificationlist) and self.containsAny(lines2.lower(), requestlist)):
            print("Allow notification")
            if device.use(text="忽略").count > 0:
                device.use(text="忽略").click()
            Flag = True
        return Flag
    
    def check_network_request(self,device):
        Flag = False
        wifilist = ["wifi","network","网络","加载","connection"]
        requestlist = ["unavailable","try again","开启","检查","失败","重新","重试","not available"]
        lines2 = device.use.dump_hierarchy()
        if (self.containsAny(lines2.lower(), wifilist) and self.containsAny(lines2.lower(), requestlist)):
            print("Allow network")
            self.injector.network_lazy_1()
            for device in self.devices:
                # if device.use(scrollable=True,packageName=self.app.package_name).count>0:
                #     device.use(scrollable=True,packageName=self.app.package_name).scroll.vert.backward(steps=5)
                #     device.use(scrollable=True,packageName=self.app.package_name).scroll.vert.forward(steps=5)
                if device.use(textContains="重试").count>0:
                    device.use(textContains="重试").click()
                    time.sleep(self.rest_interval*1)
            Flag = True
        return Flag

    def check_permission_request(self,device):
        Flag = False
        while device.use(className="android.widget.Button",packageName="com.google.android.permissioncontroller").count > 0:
            print("Allow permission:permissioncontroller")
            device.use(className="android.widget.Button",packageName="com.google.android.permissioncontroller").click()
            time.sleep(self.rest_interval*1)
            Flag = True
        while device.use(className="android.widget.Button",packageName="com.android.packageinstaller").count > 0:
            print("Allow permission:packageinstaller")
            device.use(className="android.widget.Button",packageName="com.android.packageinstaller",instance=1).click()
            time.sleep(self.rest_interval*1)
            Flag = True
        while device.use(className="android.widget.Button",packageName="com.google.android.packageinstaller").count > 0:
            print("Allow permission:packageinstaller")
            device.use(className="android.widget.Button",packageName="com.google.android.packageinstaller",instance=1).click()
            time.sleep(self.rest_interval*1)
            Flag = True
        
        permissionlist = ["权限","permission","authoriz"]
        requestlist = ["需要","开启","allow","允许","request","ensure","require","检查"]
        speciallist = ["migrate"]
        lines2 = device.use.dump_hierarchy()
        if device.use(packageName="com.android.settings",text="Permissions").count>0:
            device.use(packageName="com.android.settings",text="Permissions").click()
            time.sleep(self.rest_interval*1)
            while device.use(text="OFF",className="android.widget.Switch").count>0:
                device.use(text="OFF",className="android.widget.Switch").click()
            while device.use(text="我知道了",resourceId="com.ss.android.ugc.aweme:id/e9y").count>0:
                device.use(text="我知道了",resourceId="com.ss.android.ugc.aweme:id/e9y").click()
            while device.use(packageName=self.app.package_name).count<1:
                device.use.press("back")
                time.sleep(self.rest_interval*1)
        elif device.use(packageName="com.android.settings",text="APPS").count>0:
            device.use(scrollable=True,instance = 0).scroll.to(text=self.app.app_name)
            device.use(text=self.app.app_name).click()
            device.use(text="Battery").wait(timeout=3.0)
            device.use(scrollable=True,instance = 0).scroll.to(text="Permissions")
            self.check_permission_request(device)
        elif (self.containsAny(lines2.lower(), permissionlist) and self.containsAny(lines2.lower(), requestlist)) or self.containsAny(lines2.lower(), speciallist):
            print("Allow permission")
            again_flag=1
            if device.use(text="允许").count > 0:
                device.use(text="允许").click()
                again_flag=0
            elif device.use(text="设置").count > 0:
                device.use(text="设置").click()
                again_flag=0
            elif device.use(text="去设置").count > 0:
                device.use(text="去设置").click()
                again_flag=0
            elif device.use(text="确定").count > 0:
                device.use(text="确定").click()
                again_flag=0
            elif device.use(text="Settings").count > 0:
                device.use(text="Settings").click()
                again_flag=0
            elif device.use(text="Allow storage permissions in order to fully enjoy WeChat features.").count > 0:
                device.use(textContains="Allow").click()
                again_flag=0
            elif device.use(className="android.widget.Button").count > 0:
                device.use(className="android.widget.Button").click()
                again_flag=0
            if again_flag==0:
                time.sleep(self.rest_interval*3)
                self.check_permission_request(device)
                Flag = True
        return Flag
    
    def containsAny(self,seq, aset):
        return True if any(i in seq for i in aset) else False

    def check_loading(self):
        wait_time=0
        for device in self.devices:
            if device.use(className="android.widget.ProgressBar").count>0 and wait_time < self.rest_interval*5:
                time.sleep(self.rest_interval*5)
                wait_time=wait_time+self.rest_interval*5
                print("wait load")
            elif wait_time > self.rest_interval*20 or wait_time == self.rest_interval*20:
                print("so long wait")
        return wait_time
    
    def check_crash(self):
        for device in self.devices:
            device.last_crash_logcat = device.crash_logcat
            f_crash = open(self.root_path+"/"+device.device_serial+"_logcat.txt",'r',encoding='utf-8')
            device.crash_logcat=f_crash.read()
            if device.use(text="Close app").count>0:
                device.use(text="Close app").click()
            if device.crash_logcat!=device.last_crash_logcat:
                crash_info = device.crash_logcat[len(device.last_crash_logcat):len(device.crash_logcat)-1]+'\n'
                return crash_info
        return None
        