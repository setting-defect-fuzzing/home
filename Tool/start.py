import argparse
from setdroid import SetDroid

def parse_args():
    """
    parse command line input
    """
    parser = argparse.ArgumentParser(description="Start SetDroid to detect setting issues.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-pro_click", action="store", dest="pro_click", required=False,
                        help="The percentage of click event", default=45)
    parser.add_argument("-pro_longclick", action="store", dest="pro_longclick", required=False,
                        help="The percentage of click event", default=25)
    parser.add_argument("-pro_scroll", action="store", dest="pro_scroll", required=False,
                        help="The percentage of click event", default=5)
    parser.add_argument("-pro_home", action="store", dest="pro_home", required=False,
                        help="The percentage of click event", default=0)
    parser.add_argument("-pro_edit", action="store", dest="pro_edit", required=False,
                        help="The percentage of click event", default=15)
    parser.add_argument("-pro_naturalscreen", action="store", dest="pro_naturalscreen", required=False,
                        help="The percentage of click event", default=1)
    parser.add_argument("-pro_leftscreen", action="store", dest="pro_leftscreen", required=False,
                        help="The percentage of click event", default=80)
    parser.add_argument("-pro_back", action="store", dest="pro_back", required=False,
                        help="The percentage of click event", default=1)
    parser.add_argument("-pro_splitscreen", action="store", dest="pro_splitscreen", required=False,
                        help="The percentage of click event", default=0)
    parser.add_argument("-app_path", action="store", dest="app_path", required=True,
                        help="The path of the application you want to test")
    parser.add_argument("-is_emulator", action="store", dest="is_emulator", required=False, default=0, type=int,
                        help="Whether the devices are emulators")
    parser.add_argument('-append_device', action='append', dest="append_device", required=True,
                        help="Serial of the device")
    parser.add_argument('-serial_or_parallel', action='store', dest="serial_or_parallel", required=False, default=0, type=int,
                        help="0 is serial, 1 is parallel")
    parser.add_argument("-append_strategy", action="append", dest="strategy_list", required=False, 
                        help="Selected strategy")
    parser.add_argument("-choice", action="store", dest="choice", required=False, default=0, type=int,
                        help="Run or replay")
    parser.add_argument("-emulator_path", action="store", dest="emulator_path", required=False, default="E:\\Sdk\\emulator\\emulator.exe",
                        help="Emulator path")
    parser.add_argument("-android_system", action="store", dest="android_system", required=False, default="emulator8",
                        help="System of the device")
    parser.add_argument("-root_path", action="store", dest="root_path", required=False, default="../Output/",
                        help="Output path")
    parser.add_argument("-emulator_name", action="store", dest="emulator_name", required=False, default="Android8.0",
                        help="the emulator name")
    parser.add_argument("-resource_path", action="store", dest="resource_path", required=False, default="Document/",
                        help="Resource path")
    parser.add_argument("-testcase_count", action="store", dest="testcase_count", required=False, default=10, type=int,
                        help="How many testcases are generated for each strategy")
    parser.add_argument("-start_testcase", action="store", dest="start_testcase_count", required=False, default=0, type=int,
                        help="start from which testcase")
    parser.add_argument("-event_num", action="store", dest="event_num", required=False, default=100, type=int,
                        help="How many events are in each test case")
    parser.add_argument("-timeout", action="store", dest="timeout", required=False, default=-1, type=int,
                        help="How long to run at most")
    parser.add_argument("-policy_name", action="store", dest="policy_name", required=False, default="random",
                        help="Policy name")
    parser.add_argument("-setting_random_denominator", action="store", dest="setting_random_denominator", required=False, default=5, type=int,
                        help="Setting random denominator")
    parser.add_argument("-app_name", action="store", dest="app_name", required=False,
                        help="App name")
    parser.add_argument("-is_login_app", action="store", dest="is_login_app", required=False, default=0, type=int,
                        help="0 = app needed to login, 1 = app did not need to login")
    parser.add_argument("-rest_interval", action="store", dest="rest_interval", required=False, default=1, type=int,
                        help="time to sleep")
    parser.add_argument("-trace_path", action="store", dest="trace_path", required=False, default="../Trace",
                        help="path of traces")

    options = parser.parse_args()
    # print options
    return options

def main():
    opts = parse_args()
    import os
    if not os.path.exists(opts.app_path):
        print("APK does not exist.")
        return
    
    if len(opts.append_device)<2:
        print("You need to define at least two devices")
        return
    
    if  len(opts.strategy_list)+1!=len(opts.append_device) and opts.serial_or_parallel == 1:
        print("You need n+1 devices to execute n strategies")
        return

    if len(opts.append_device)>2 and opts.serial_or_parallel ==0:
        print("You can only execute serial strategy in 2 device")
        return

    setdroid = SetDroid(
        pro_click=opts.pro_click,
        pro_longclick=opts.pro_longclick,
        pro_scroll=opts.pro_scroll,
        pro_home=opts.pro_home,
        pro_edit=opts.pro_edit,
        pro_naturalscreen=opts.pro_naturalscreen,
        pro_leftscreen=opts.pro_leftscreen,
        pro_back=opts.pro_back,
        pro_splitscreen=opts.pro_splitscreen,
        app_path=opts.app_path,
        is_emulator=opts.is_emulator,
        devices_serial=opts.append_device,
        choice=opts.choice,
        emulator_path=opts.emulator_path,
        android_system=opts.android_system,
        root_path=opts.root_path,
        resource_path=opts.resource_path,
        strategy_list=opts.strategy_list,
        testcase_count=opts.testcase_count,
        start_testcase_count=opts.start_testcase_count,
        event_num=opts.event_num,
        timeout=opts.timeout,
        policy_name=opts.policy_name,
        setting_random_denominator=opts.setting_random_denominator,
        serial_or_parallel=opts.serial_or_parallel,
        app_name=opts.app_name,
        emulator_name=opts.emulator_name,
        is_login_app=opts.is_login_app,
        rest_interval=opts.rest_interval,
        trace_path=opts.trace_path
    )
    setdroid.start()
    setdroid.stop()

if __name__ == "__main__":
    main()