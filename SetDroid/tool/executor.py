import json
import os
import logging
import subprocess
import time
from device import Device
from app import App
from injector import Injector
from policy import Policy,RandomPolicy
import uiautomator2 as u2
from state import State
from checker import Checker
from event import Event
import random
from view import View
from utils import Utils


            
class Executor(object):

    def __init__(self,devices,app,strategy_list,pro_click,pro_longclick,pro_scroll,
                pro_home,pro_edit,pro_naturalscreen,pro_leftscreen,pro_back,pro_splitscreen,emulator_path,android_system,
                root_path,resource_path,testcase_count,start_testcase_count,event_num,timeout,policy_name,
                setting_random_denominator,serial_or_parallel,emulator_name,is_login_app,rest_interval,trace_path,choice):
        
        self.policy_name=policy_name
        self.timeout = timeout
        self.pro_click = pro_click
        self.pro_longclick = pro_longclick
        self.pro_scroll = pro_scroll
        self.pro_home = pro_home
        self.pro_edit = pro_edit
        self.pro_naturalscreen = pro_naturalscreen
        self.pro_leftscreen = pro_leftscreen
        self.pro_back = pro_back
        self.pro_splitscreen = pro_splitscreen
        self.app = app
        self.devices = devices
        self.emulator_path = emulator_path
        self.android_system = android_system
        self.resource_path = resource_path
        self.strategy_list = strategy_list
        self.testcase_count = testcase_count
        self.start_testcase_count = start_testcase_count
        self.event_num = event_num
        self.setting_random_denominator = setting_random_denominator
        self.root_path = root_path
        self.policy = self.get_policy()
        self.serial_or_parallel = serial_or_parallel
        self.emulator_name = emulator_name
        self.is_login_app = is_login_app
        self.rest_interval = rest_interval
        self.guest_devices=self.devices[1:len(self.devices)]
        self.trace_path=trace_path
        self.choice=choice
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
        
        self.checker = Checker(devices=devices,
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
                choice=self.choice)

        self.utils = Utils(devices=devices)
    
    def get_policy(self):
        if self.policy_name=="random":
            print("Policy: Random")
            policy = RandomPolicy(self.devices,self.app,self.emulator_path,self.android_system,self.root_path,
                self.pro_click,self.pro_longclick,self.pro_scroll,self.pro_edit,self.pro_naturalscreen,self.pro_leftscreen,self.pro_back,self.pro_splitscreen,self.pro_home)
        else:
            print("No valid input policy specified. Using policy \"none\".")
            policy = None
        return policy
        
    def execute_event(self,device,event,num):
        try:
            have_view_action=["click","longclick","edit","scroll"]
            feature=""
            if event.action in have_view_action and event.view is not None:
                if device.use(resourceId=event.view.resourceId).count==0 or device.use(className=event.view.className).count==0:
                    lines = device.use.dump_hierarchy()
                    if (event.view.resourceId != "" and event.view.resourceId not in lines) or (event.view.className != "" and event.view.className not in lines):
                        return False
            
            if event.action.startswith("setting_"):
                self.injector.replay_setting(event,self.strategy_list)
            elif event.action == "check_setting_request":
                self.checker.check_setting_request()
            elif event.action == "check_login":
                self.checker.check_login()
            elif event.action == "click":
                feature=device.click(event.view,self.strategy_list)
            elif event.action == "longclick":
                device.longclick(event.view,self.strategy_list)
            elif event.action == "edit":
                device.edit(event.view,self.strategy_list,event.text)
            elif event.action == "scroll":
                device.scroll(event.view,self.strategy_list)
            elif event.action == "back":
                device.use.press("back")
            elif event.action == "home":
                device.use.press("home")
            elif event.action == "naturalscreen":
                device.use.set_orientation("n")
            elif event.action == "leftscreen":
                device.use.set_orientation("l")
            elif event.action == "start":
                device.start_app(self.app)
            elif event.action == "stop":
                device.stop_app(self.app)
            elif event.action == "clear":
                device.clear_app(self.app,self.is_login_app)
            elif event.action == "restart":
                device.restart(self.emulator_path,self.emulator_name)
            
            print(device.device_serial+":"+feature+":end execute\n")
            time.sleep(self.rest_interval*1)
            return True
        except Exception as ex:
            if num ==0:
                print(ex)
                return self.execute_event(device,event,1)
            else:
                print(ex)
                return False
   
    def replay(self,strategy):
        
        #init
        self.injector.init_setting()
        action_list = ["click","long_click","edit"]
        self.devices[1].set_strategy(strategy)
        path = os.path.join(self.root_path, "strategy_"+strategy)
        self.error_path = os.path.join(path, "error_replay")
        self.utils.create_dir(self.error_path)
        self.f_replay_record = open(os.path.join(path, "error_replay.txt"),'w',encoding='utf-8')
        self.error_event_lists = []
        self.f_replay = open(os.path.join(path, "error_realtime.txt"),'r',encoding='utf-8')
        lines = self.f_replay.readlines()
        
        for line in lines:
            
            self.error_event_lists.append(line)
            if "Start::" in line:
                #init dir for each error
                print("Start")
                record_flag = False
                linelist = line.split("::")
                self.utils.create_dir(os.path.join(self.error_path, linelist[1]))
                self.screen_path = os.path.join(self.error_path, linelist[1], "screen/")
                self.utils.create_dir(self.screen_path)
                f_read_trace = open(os.path.join(self.error_path, linelist[1], "read_trace.txt"),'w',encoding='utf-8')
                print(self.screen_path)
            elif "End::" in line:
                #end
                if record_flag == True:
                    for theline in self.error_event_lists:
                        self.f_replay_record.write(theline)
                        self.f_replay_record.flush()
                    self.error_event_lists = []
                    record_flag = False
                    f_read_trace.close()
                    self.utils.generate_html(os.path.join(self.error_path, linelist[1]),self.error_path,linelist[1])
            elif line.strip() !="":
                print("-----------------------"+'\n'+line)
                f_read_trace.write(line)
                f_read_trace.flush()
                #replay each event
                elementlist = line.split("::")
                event = self.get_replay_event(elementlist,line)
                event.print_event()
                if elementlist[1] == "save_state":
                    self.save_state(event.device.device_num,self.screen_path,elementlist[0],self.f_replay_record)
                else:
                    if event.action in action_list:
                        self.utils.draw_event(event)
                    args=(event.device,event,0)
                    self.devices[event.device.device_num].set_thread(self.execute_event,args)
                    if event.device.device_num == 1:
                        self.utils.start_thread()
                        for device in self.devices:
                            if device.thread is not None:
                                success_flag = device.thread.get_result()
                                if not success_flag:
                                    record_flag=True
                                device.set_thread(None,None)
                    time.sleep(self.rest_interval*1)
                if "device1" in line and "save_state" in line and self.devices[0].state is not None and self.devices[1].state is not None and not self.devices[0].state.same(self.devices[1].state):
                    print("different!")
                    event = Event(None, "wrong", self.devices[1], elementlist[0])
                    self.utils.draw_event(event)
                if "::start::" in line:
                    self.checker.check_start(0,strategy)

    def get_replay_event(self,elementlist,line):
        view =None
        if elementlist[4].strip()!="None":
            view=View(elementlist[4],None,[])
        if elementlist[2] == "device0":
            event = Event(view, elementlist[1], self.devices[0], elementlist[0])
        elif elementlist[2] == "device1":
            event = Event(view, elementlist[1], self.devices[1], elementlist[0])
        else:
            print(line+"error")
        return event
    
    def start_app(self,event_count):
        for device in self.devices:
            args=(self.app,)
            device.set_thread(device.start_app,args)
        self.utils.start_thread()
        
        for device in self.guest_devices:
            self.utils.write_read_event("::start::all devices::None::None"+'\n',event_count,None,"all devices",device.device_num)
            event = Event(None, "start", device, event_count)
            self.utils.write_event(event,device.device_num,device.f_trace)
            self.utils.draw_event(event)
    
    def clear_app(self,event_count):
        for device in self.devices:
            device.clear_app(self.app,self.is_login_app)
            device.use.set_orientation("n")
        
        for device in self.guest_devices:
            device.error_event_lists.clear()
            device.wrong_event_lists.clear()
            device.wrong_flag=True
            self.utils.write_read_event("::clear::all devices::None::None"+'\n',event_count,None,"all devices",device.device_num)
            event = Event(None, "clear", device, event_count)
            self.utils.write_event(event,device.device_num,device.f_trace)
            self.utils.draw_event(event)
    
    def clear_and_restart_app(self,event_count,strategy):
        for device in self.devices:
            device.clear_app(self.app,self.is_login_app)
            device.use.set_orientation("n")
        for device in self.guest_devices:
            device.error_event_lists.clear()
            device.wrong_event_lists.clear()
            device.wrong_flag=True
            event = Event(None, "naturalscreen", device, event_count)
            self.utils.write_event(event,device.device_num,device.f_trace)
            event = Event(None, "clear", device, event_count)
            event_count = self.write_draw_and_save_all(device,event,event_count)
        
        if event_count>3:
            event=self.injector.change_setting_after_run(event_count,strategy)
            if event is not None:
                event_count = self.write_draw_and_save_one(event,event_count)
        
        #check keyboard
        self.checker.check_keyboard()

        for device in self.devices:
            args=(self.app,)
            device.set_thread(device.start_app,args)
        self.utils.start_thread()
        self.checker.check_start(0,strategy)
        
        for device in self.guest_devices:
            event = Event(None, "start", device, event_count)
            event_count = self.write_draw_and_save_all(device,event,event_count)
        
        if self.checker.check_login():
            event = Event(None, "check_login", self.devices[1], event_count)
            event_count = self.write_draw_and_save_one(event,event_count)
        event=self.injector.change_setting_before_run(event_count,strategy)
        
        if event is not None:
            event_count = self.write_draw_and_save_one(event,event_count)
        return event_count
    
    def back_to_app(self,event_count,strategy):
        for device in self.devices:
            device.use.press("back")
        print("Back")
        time.sleep(self.rest_interval*1)
        if not self.checker.check_foreground():
            for device in self.devices:
                device.stop_app(self.app)
                args=(self.app,)
                device.set_thread(device.start_app,args)
            self.utils.start_thread()
            self.checker.check_start(1,strategy)
            
            for device in self.guest_devices:
                self.utils.write_read_event("::restart::all devices::None::None"+'\n',event_count,None,"all devices",device.device_num)
                event = Event(None, "back", device, event_count)
                self.utils.write_event(event,device.device_num,device.f_trace)
                event = Event(None, "home", device, event_count)
                self.utils.write_event(event,device.device_num,device.f_trace)
                event = Event(None, "start", device, event_count)
                self.utils.write_event(event,device.device_num,device.f_trace)
                self.utils.draw_event(event)
        else:
            for device in self.guest_devices:
                self.utils.write_read_event("::back::all devices::None::None"+'\n',event_count,None,"all devices",device.device_num)
                event = Event(None, "back", device, event_count)
                self.utils.write_event(event,device.device_num,device.f_trace)
                self.utils.draw_event(event)
    
    def save_all_state(self,event_count):
        time.sleep(self.rest_interval*1)
        for device in self.guest_devices:
            self.save_state(0,device.path+"screen/",event_count,device.f_trace)
            self.save_state(device.device_num,device.path+"screen/",event_count,device.f_trace)
            event = Event(None, "save_state", device, event_count)
            event.set_count(device.device_num)
            self.utils.write_event(event,device.device_num,device.f_trace)
        return event_count+1
    
    def update_all_state(self,event_count):
        event_count=event_count-1
        time.sleep(self.rest_interval*1)
        for device in self.guest_devices:
            self.update_state(0,device.path+"screen/",event_count,device.f_trace)
            self.update_state(device.device_num,device.path+"screen/",event_count,device.f_trace)
        event_count=event_count+1
    
    def save_state(self,device_count,path,event_count,f_trace):
        #get and save state of all devices
        lines = self.devices[device_count].screenshot_and_getstate(path,event_count)
        state = State(lines)
        self.devices[device_count].update_state(state)   
    
    def update_state(self,device_count,path,event_count,f_trace):
        lines = self.devices[device_count].use.dump_hierarchy().splitlines()
        state = State(lines)
        self.devices[device_count].update_state(state)
        if self.devices[device_count].last_state != self.devices[device_count].state:
            self.save_state(device_count,path,event_count,f_trace)
    
    def restart_devices(self,event_count):
        print("restart_devices")
        for device in self.devices:
            if device.is_emulator == 0:
                device.restart(self.emulator_path,self.emulator_name)
        for device in self.guest_devices:
            device.connect()
            device.error_event_lists.clear()
            device.wrong_event_lists.clear()
            device.wrong_flag=True
            self.utils.write_read_event("::restart::all devices::None::None"+'\n',event_count,None,"all devices",device.device_num)
            event = Event(None, "restart", device, event_count)
            self.utils.write_event(event,device.device_num,device.f_trace)
            self.utils.draw_event(event)
    
    def wait_load(self,event_count):
        wait_time=self.checker.check_loading()
        if wait_time>0:
            event_count=event_count-1
            event_count=self.save_all_state(event_count)

    def write_draw_and_save_one(self,event,event_count):
        self.utils.write_read_event(None,event_count,event,"all device",event.device.device_num)
        self.utils.write_one_device_event(event,event.device.device_num,event.device.f_trace)
        self.utils.draw_event(event)
        event_count=self.save_all_state(event_count)
        return event_count
    
    def write_draw_and_save_all(self,device,event,event_count):
        self.utils.write_read_event(None,event_count,event,"all device",event.device.device_num)
        self.utils.write_event(event,device.device_num,device.f_trace)
        self.utils.draw_event(event)
        event_count=self.save_all_state(event_count)
        return event_count
    
    def read_event(self,line,event_count):
        eventlist=line.split("::")
        action=eventlist[1]
        if eventlist[4] != "None\n":
            view=View(eventlist[4],None,[])
            event = Event(view, action, self.devices[0], event_count)
        else:
            event = Event(None, action, self.devices[0], event_count)
        return event
    def test(self):
        device = self.devices[1]
        self.devices[0].use.open_quick_settings()
        device.use.open_quick_settings()
        time.sleep(1)
        if device.use(description="Airplane mode",text="Off").count>0:
            device.use(description="Airplane mode",text="Off").click()
        elif device.use(description="Airplane mode",text="Off").count>0:
            device.use(description="Airplane mode",text="Off").click()

    
    def manual_test(self,strategy):
        #if execute serial, init the strategy of device1, otherwise, init all the guest devices' strategies
        if self.serial_or_parallel == 0:
            self.devices[0].set_strategy(strategy)
            self.devices[1].set_strategy(strategy)
            self.devices[1].make_strategy(self.root_path)
        else:
            for device in self.guest_devices:
                device.set_strategy(self.strategy_list[device.device_num-1])
                device.make_strategy(self.root_path)
        
        run_count=0
        for testcase_file in os.listdir(self.trace_path):
            testcase_f = open(os.path.join(self.trace_path,testcase_file),'r',encoding='utf-8')
            lines=testcase_f.readlines()
            
            #create folder of new run
            run_count=run_count+1
            for device in self.guest_devices:
                device.make_strategy_runcount(run_count,self.root_path)
            
            #init setting
            event_count=0.0
            event_count=self.save_all_state(event_count)
            self.injector.init_setting()
            
            #clear and start app
            event_count=self.clear_and_restart_app(event_count,strategy)
            
            for line in lines:

                #if the state of any device is different from last state, stoat need to judge (loading, foreground, same) again
                change_flag = False
                self.update_all_state(event_count)
                for device in self.devices:
                    if device.last_state != device.state:
                        change_flag = True
                        break
                
                if self.devices[0].last_state is not None and change_flag:
                    #wait loading
                    self.wait_load(event_count)

                    #check whether app is foreground
                    if not self.checker.check_foreground():
                        print("Not foreground")
                        self.back_to_app(event_count,strategy)
                        self.checker.check_loading()
                        event_count=self.save_all_state(event_count)
                    
                    #check keyboard
                    self.checker.check_keyboard()
                    
                    request_flag=0
                    #judge whether all devices are same
                    if not self.devices[0].state.same(self.devices[1].state):
                        #judge whether the guest devices requests settings
                        if self.checker.check_setting_request():
                            event = Event(None, "check_setting_request", self.devices[1], event_count)
                            event_count = self.write_draw_and_save_one(event,event_count)
                            request_flag=1
                        #write wrong
                        elif self.devices[1].wrong_flag==True:
                            print("Write wrong!")
                            self.utils.write_error(1,run_count,self.devices[1].wrong_event_lists,self.devices[1].f_wrong,self.devices[1].wrong_num)
                            self.devices[1].wrong_num=self.devices[1].wrong_num+1
                            event = Event(None, "wrong", self.devices[1], event_count)
                            self.utils.draw_event(event)

                    #check login page and login
                    if strategy!="language" and self.checker.check_login():
                        event = Event(None, "check_login", self.devices[1], event_count)
                        event_count = self.write_draw_and_save_one(event,event_count)

                    self.wait_load(event_count)
                        
                #choice a new event to execute
                event=self.read_event(line,event_count)
                self.utils.draw_event(event)
                event.print_event()
                
                #execute event
                for device in self.devices:
                    # success = self.execute_event(event,0)
                    args=(device,event,0)
                    device.set_thread(self.execute_event,args)
                self.utils.start_thread()
                for device in self.devices:
                    success = device.thread.get_result()
                    if not success:
                        fail_device = device.device_num
                        break
                
                #device0 can not execute choice event, choice another event, skip this loop
                if not success and fail_device == 0: 
                    self.utils.print_dividing_line(False,event_count)
                    continue
                #other devices cannot execute choice event due to setting, record fail, skip this loop
                elif not success: 
                    print("write error")
                    self.utils.print_dividing_line(False,event_count)
                    self.utils.write_read_event(None,event_count,event,"different",fail_device)
                    self.utils.write_event(event,fail_device,self.devices[fail_device].f_trace)
                    self.utils.draw_event(event)
                    event_count=self.save_all_state(event_count)
                    self.utils.write_error(fail_device,run_count,self.devices[fail_device].error_event_lists,self.devices[fail_device].f_error,self.devices[fail_device].error_num)
                    self.devices[fail_device].error_num=self.devices[fail_device].error_num+1
                    event_count=self.clear_and_restart_app(event_count,strategy)
                    continue
                #all devices execute success, record event and update state
                else: 
                    self.utils.print_dividing_line(True,event_count)
                    self.utils.write_read_event(None,event_count,event,"all device",device.device_num)
                    self.utils.write_event(event,device.device_num,device.f_trace)
                    event_count=self.save_all_state(event_count)
                
                #check keyboard
                self.checker.check_keyboard()

                #injecte a setting change
                self.update_all_state(event_count)
                event=self.injector.inject_setting_during_run(event_count,strategy,request_flag)
                time.sleep(2)
                if event != None:
                    self.checker.check_setting_request()
                    event_count = self.write_draw_and_save_one(event,event_count)
                    change_flag = False
                    self.update_all_state(event_count)
                    if not self.devices[0].last_state.same(self.devices[0].state) and not self.devices[0].state.same(self.devices[1].state):
                        self.checker.check_start(1,strategy)
                        print("Different due to permission")
                        change_flag = True
                        break
            
            event=self.injector.change_setting_after_run(event_count,strategy)
            if event is not None:
                event_count = self.write_draw_and_save_one(event,event_count)
            
            #at the end of each run, generate a html file
            for device in self.guest_devices:
                self.utils.generate_html(device.path,device.path,run_count) 
    
    def start(self,strategy):
        #if execute serial, init the strategy of device1, otherwise, init all the guest devices' strategies
        self.checker.set_strategy(strategy)
        if self.serial_or_parallel == 0:
            self.devices[0].set_strategy(strategy)
            self.devices[1].set_strategy(strategy)
            self.devices[1].make_strategy(self.root_path)
        else:
            for device in self.guest_devices:
                device.set_strategy(self.strategy_list[device.device_num-1])
                device.make_strategy(self.root_path)
        
        run_count=self.start_testcase_count
        while run_count < self.testcase_count:
            
            #create folder of new run
            run_count=run_count+1
            for device in self.guest_devices:
                device.use.press("back")
                device.use.press("back")
                device.make_strategy_runcount(run_count,self.root_path)
            
            #init setting
            event_count=0.0
            event_count=self.save_all_state(event_count)
            self.injector.init_setting()
            
            #clear and start app
            event_count=self.clear_and_restart_app(event_count,strategy)
            
            while event_count<self.event_num:

                #if the state of any device is different from last state, stoat need to judge (loading, foreground, same) again
                change_flag = False
                self.update_all_state(event_count)
                for device in self.devices:
                    if device.last_state != device.state:
                        change_flag = True
                        break
                
                request_flag=0
                if self.devices[0].last_state is not None and change_flag:
                    #wait loading
                    self.wait_load(event_count)

                    #check whether app is foreground
                    if not self.checker.check_foreground():
                        print("Not foreground")
                        self.back_to_app(event_count,strategy)
                        self.checker.check_loading()
                        event_count=self.save_all_state(event_count)
                    
                    #check keyboard
                    self.checker.check_keyboard()
                    
                    #judge whether all devices are same
                    if not self.devices[0].state.same(self.devices[1].state):
                        #judge whether the guest devices requests settings
                        if self.checker.check_setting_request():
                            event = Event(None, "check_setting_request", self.devices[1], event_count)
                            event_count = self.write_draw_and_save_one(event,event_count)
                            request_flag=1
                        #write wrong
                        elif self.app.package_name=="hk.alipay.wallet" and strategy=="wifi_off":
                            self.injector.turn_on_wifi()
                            for device in self.devices:
                                device.use.press("back")
                            event = Event(None, "wifi_back", self.devices[1], event_count)
                            event_count = self.write_draw_and_save_one(event,event_count)
                            request_flag=1
                        elif self.devices[1].wrong_flag==True:
                            print("Write wrong!")
                            self.utils.write_error(1,run_count,self.devices[1].wrong_event_lists,self.devices[1].f_wrong,self.devices[1].wrong_num)
                            self.devices[1].wrong_num=self.devices[1].wrong_num+1
                            event = Event(None, "wrong", self.devices[1], event_count)
                            self.utils.draw_event(event)

                    #check keyboard
                    self.checker.check_keyboard()

                    #check login page and login
                    if strategy!="language" and self.checker.check_login():
                        event = Event(None, "check_login", self.devices[1], event_count)
                        event_count = self.write_draw_and_save_one(event,event_count)

                    self.wait_load(event_count)
                
                self.update_all_state(event_count)

                #choice a new event to execute
                event=self.policy.choice_event(self.devices[0],event_count)
                self.utils.draw_event(event)
                event.print_event()
                
                #execute event
                for device in self.devices:
                    # success = self.execute_event(event,0)
                    args=(device,event,0)
                    device.set_thread(self.execute_event,args)
                self.utils.start_thread()
                for device in self.devices:
                    success = device.thread.get_result()
                    if not success:
                        fail_device = device.device_num
                        break
                
                #device0 can not execute choice event, choice another event, skip this loop
                if not success and fail_device == 0: 
                    self.utils.print_dividing_line(False,event_count)
                    continue
                #other devices cannot execute choice event due to setting, record fail, skip this loop
                elif not success: 
                    print("write error")
                    self.utils.print_dividing_line(False,event_count)
                    self.utils.write_read_event(None,event_count,event,"different",fail_device)
                    self.utils.write_event(event,fail_device,self.devices[fail_device].f_trace)
                    self.utils.draw_event(event)
                    event_count=self.save_all_state(event_count)
                    self.utils.write_error(fail_device,run_count,self.devices[fail_device].error_event_lists,self.devices[fail_device].f_error,self.devices[fail_device].error_num)
                    self.devices[fail_device].error_num=self.devices[fail_device].error_num+1
                    event_count=self.clear_and_restart_app(event_count,strategy)
                    continue
                #all devices execute success, record event and update state
                else: 
                    self.utils.print_dividing_line(True,event_count)
                    self.utils.write_read_event(None,event_count,event,"all device",device.device_num)
                    self.utils.write_event(event,device.device_num,device.f_trace)
                    event_count=self.save_all_state(event_count)
                
                self.checker.check_keyboard()

                #injecte a setting change
                event=self.injector.inject_setting_during_run(event_count,strategy,request_flag)
                if event is not None:
                    event_count = self.write_draw_and_save_one(event,event_count)

            event=self.injector.change_setting_after_run(event_count,strategy)
            if event is not None:
                event_count = self.write_draw_and_save_one(event,event_count)
            
            #at the end of each run, generate a html file
            for device in self.guest_devices:
                self.utils.generate_html(device.path,device.path,run_count) 
        


            
            