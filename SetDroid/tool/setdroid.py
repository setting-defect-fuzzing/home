import logging
import os
import sys
import pkg_resources
import shutil
from threading import Timer
from device import Device
from app import App
from executor import Executor
import uiautomator2 as u2
import time

class SetDroid(object):
    instance = None
    def __init__(self,
                devices_serial,
                pro_click=100,
                pro_longclick=10,
                pro_scroll=10,
                pro_edit=10,
                pro_naturalscreen=5,
                pro_leftscreen=10,
                pro_back=5,
                pro_home=5,
                pro_splitscreen=0,
                app_path=None,
                is_emulator=True,
                choice=0,
                emulator_path=None,
                android_system=None,
                root_path=None,
                resource_path=None,
                strategy_list=None,
                testcase_count=None,
                start_testcase_count=None,
                event_num=None,
                timeout=None,
                policy_name="random",
                setting_random_denominator=5,
                serial_or_parallel=None,
                app_name=None,
                emulator_name=None,
                is_login_app=None,
                rest_interval=None,
                trace_path=None):
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SetDroid')
        self.enabled = True
        SetDroid.instance = self
        self.timer = None
        
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
        self.app_path = app_path
        self.is_emulator = is_emulator
        self.devices_serial = devices_serial
        self.devices=[]
        self.choice = choice
        self.emulator_path = emulator_path
        self.android_system = android_system
        self.resource_path = resource_path
        self.strategy_list = strategy_list
        self.testcase_count = testcase_count
        self.start_testcase_count = start_testcase_count
        self.event_num = event_num
        self.app = App(app_path, root_path, app_name)
        self.setting_random_denominator = setting_random_denominator
        self.serial_or_parallel = serial_or_parallel
        self.emulator_name = emulator_name
        self.is_login_app = is_login_app
        self.rest_interval = rest_interval
        self.trace_path = trace_path
        self.start_time = 0

        if root_path is not None:
            if not os.path.isdir(root_path):
                os.makedirs(root_path)
        else:
            print("None root path")
            return
        self.root_path = root_path+self.app.package_name+"/"
        if not os.path.isdir(self.root_path):
            os.makedirs(self.root_path)
        
        i=0
        for device_serial in devices_serial:
            device = Device(
                device_serial=device_serial,
                is_emulator=is_emulator,
                device_num=i,
                rest_interval=rest_interval)
            self.devices.append(device)
            i=i+1

        self.executor = Executor(
                devices=self.devices,
                app=self.app,
                strategy_list=self.strategy_list,
                pro_click=self.pro_click,
                pro_longclick=self.pro_longclick,
                pro_scroll=self.pro_scroll,
                pro_home=self.pro_home,
                pro_edit=self.pro_edit,
                pro_naturalscreen=self.pro_naturalscreen,
                pro_leftscreen=self.pro_leftscreen,
                pro_back=self.pro_back,
                pro_splitscreen=self.pro_splitscreen,
                emulator_path=self.emulator_path,
                android_system=self.android_system,
                root_path=self.root_path,
                resource_path=self.resource_path,
                testcase_count=self.testcase_count,
                start_testcase_count=self.start_testcase_count,
                event_num=self.event_num,
                timeout=self.timeout,
                policy_name=self.policy_name,
                setting_random_denominator=self.setting_random_denominator,
                serial_or_parallel=self.serial_or_parallel,
                emulator_name=self.emulator_name,
                is_login_app=self.is_login_app,
                rest_interval=self.rest_interval,
                trace_path=self.trace_path,
                choice = self.choice)
        

    @staticmethod
    def get_instance():
        if SetDroid.instance is None:
            print("Error: SetDroid is not initiated!")
            sys.exit(-1)
        return SetDroid.instance

    def start(self):
        
        """
        start interacting
        :return:
        """
        if not self.enabled:
            return
        # self.logger.info("Starting SetDroid")

        if self.timeout > 0:
            self.timer = Timer(self.timeout, self.stop)
            self.timer.start()
        self.start_time = time.time()
        
        #connect device and install app
        if self.is_login_app != 0:
            for device in self.devices:
                device.connect()
                device.install_app(self.app.app_path)
        else:
            for device in self.devices:
                # device.restart(self.emulator_path,self.emulator_name)
                device.connect()
        
        if self.choice == 0: #run
            if self.serial_or_parallel == 0:
                for strategy in self.strategy_list:
                    # try:
                    self.executor.start(strategy)
                    # except:
                    #     continue
            else:
                self.executor.start(0)
        elif self.choice == 1: #replay
            for strategy in self.strategy_list:
                self.executor.replay(strategy)
        elif self.choice == 2: #replay
            for strategy in self.strategy_list:
                self.executor.manual_test(strategy)
        elif self.choice == 3:
            self.executor.test()
            for device in self.devices:
                device.screenshot_and_getstate(self.root_path,-1)
        else: #screenshot
            for device in self.devices:
                device.screenshot_and_getstate(self.root_path,-1)
    
    def stop(self):
        self.enabled = False
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        end = time.time()
        try:
            print(end-self.start_time)
        except:
            print("end:"+end)
        
    
