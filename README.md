# SetDroid Prototype

## Publication

[1] "Understanding and Finding System Setting-Related Defects in Android Apps" by Jingling Sun, Ting Su, Junxin Li, Zhen Dong, Geguang Pu, Tao Xie and Zhendong Su. *The 30th ACM SIGSOFT International Symposium on Software Testing and Analysis* (ISSTA 2021)
```
@inproceedings{10.1145/3460319.3464806,
author = {Sun, Jingling and Su, Ting and Li, Junxin and Dong, Zhen and Pu, Geguang and Xie, Tao and Su, Zhendong},
title = {Understanding and Finding System Setting-Related Defects in Android Apps},
year = {2021},
isbn = {9781450384599},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3460319.3464806},
doi = {10.1145/3460319.3464806},
booktitle = {Proceedings of the 30th ACM SIGSOFT International Symposium on Software Testing and Analysis},
pages = {204–215},
numpages = {12},
keywords = {Testing, Setting, Empirical study, Android},
location = {Virtual, Denmark},
series = {ISSTA 2021}
}
```

## Getting Started

### Running SetDroid via Virtual Machine

#### Requirements

* You need to enable virtualization technology in your computer's BIOS, see [this link](https://stackoverflow.com/questions/35456063/enable-intel-vt-x-intel-virtualization-technology-intel-vt-x) for how to enable virtualization technology in the computer. Some computers have turned on virtualization by default. 
* Your computer needs at least 16G of memory, and at least 40G of storage.
* VirtualBox: we built our artifact by using version 6.1.20.
* Download the zip file from [this link](https://1drv.ms/u/s!AinXMMnLw-UDjTNrboNh0fTfss6G?e=v0Va1t), and extract it.

#### Setting up ([video tutorial](https://1drv.ms/u/s!AinXMMnLw-UDjgCWoQclrXqb6-xE?e=n6eiDy))

* Open VirtualBox, click "File", click "Import Appliance", then select the file named "SetDroid.ova" from the extracted contents (this step will take about five to ten minutes to complete). 
* After the import is completed, you should see "vm" as one of the listed VMs in your VirtualBox.
* Click "Settings", click "System", click "Processor", and check "Enable Nested VT-x/AMD-V"
* If you want to run the virtual machine more smoothly, you can click "Setting", click "Display", and then increase the value of "Video Memory" according to your situation.
* Run the virtual machine. The username and the password are both "setdroid".
* If you could not run the VM with "Nested VT-x/AMD-V" option enabled in VirtualBox, it may be because that you did not disable the Hyper-V option. You can disable Hyper-V launch temporarily. See [this link](https://forums.virtualbox.org/viewtopic.php?f=1&t=62339) for more information about that.
* If you want to copy & paste from host to "vm", you can open the terminal and execute the following command (you may not need to do so, because the virtual machine already contains all the files needed to run the tool):
```
sudo apt-get install virtualbox-guest-additions-iso
sudo mkdir /media/temp
sudo mount /usr/share/virtualbox/VBoxGuestAdditions.iso /media/temp
```

#### Run ([video tutorial](https://1drv.ms/u/s!AinXMMnLw-UDjgCWoQclrXqb6-xE?e=n6eiDy))

* Open the terminal and execute the following command:
```
/home/setdroid/Android/Sdk/emulator/emulator -avd Android8.0 -read-only -port 5554 &
```
* Wait for the first Android emulator to start. After the emulator is successfully started, return to the command-line interface, press enter, and then execute the following command:
```
/home/setdroid/Android/Sdk/emulator/emulator -avd Android8.0 -read-only -port 5556 &
```
* Wait for the second Android emulator to start. After the emulator is successfully started, return to the command-line interface, press enter, and then execute the following command:
```
cd /home/setdroid/SetDroid/Tool 
```
* Then execute the following command (this step will take about five to ten minutes to complete):
```
python3 start.py -app_path /home/setdroid/SetDroid/App/a2dp.Vol.apk -append_device emulator-5554 -append_device emulator-5556 -android_system emulator8 -append_strategy display_immediate_1 -testcase_count 1 -choice 0 -event_num 50
```
* At this point, SetDroid will start to run a round of example policy (Oracle checking rule I -immediate -display -1) on the example app ( A2DP Volume), which contains 50 events.
* The target app can be modified by the configuration parameter ```-app_path```. The number of runs can be modified by the configuration parameter ```-testcase_count```. The number of events contained in each test can be modified by the configuration parameter ```-event_num```. Setting change strategy can be changed through the configuration parameter ```-append_strategy```. You can also add more strategies to make them be executed in sequence.
* For example, the following command represents the sequential execution of two strategies (Oracle checking rule I - lazy - permission) and (Oracle checking rule II - language) on Amaze. Each strategy is executed 10 times, and each test contains 100 events (this command will take about one to two hours to complete, and you can interrupt the command through ```Ctrl-C``` at any time):
```
python3 start.py -app_path /home/setdroid/SetDroid/App/com.amaze.filemanager.apk -append_device emulator-5554 -append_device emulator-5556 -android_system emulator8 -append_strategy permssion_lazy_1 -append_strategy language -testcase_count 10 -event_num 100
```

### Building and Running SetDroid From Scratch

#### Requirements

- Download all the files from [this link](https://1drv.ms/u/s!AinXMMnLw-UDjTX9NJsPSWALFx5p?e=nwW830)
- Download all the apps from [this link](https://1drv.ms/u/s!AinXMMnLw-UDjWBJXwgywNLad3T9?e=S1mMXt)
- Android SDK: API 26+
- Python 3.8
- We use some libraries (uiautomator2, androguard, cv2, langid, numpy) provided by python, you can add them as prompted, for example:
```
pip3 install langid
```

#### Setting up

You can create an emulator before running SetDroid. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you to start using SetDroid quickly：
```
sdkmanager "system-images;android-26;google_apis;x86"
avdmanager create avd --force --name Android8.0 --package 'system-images;android-26;google_apis;x86' --abi google_apis/x86 --sdcard 512M --device "pixel_xl"
```
Next, you can start two identical emulators and assign their port numbers with the following commands:
```
emulator -avd Android8.0 -read-only -port 5554
emulator -avd Android8.0 -read-only -port 5556
```
#### Run
If you have downloaded our project and configured the environment, you only need to enter ```download_path/tool``` to execute our sample app with the following command:
```
python3 start.py -app_path /home/setdroid/SetDroid/App/a2dp.Vol.apk -append_device emulator-5554 -append_device emulator-5556 -android_system emulator8 -append_strategy display_immediate_1 -testcase_count 1
```
SetDroid provides several ways to test android apps by command lines. You need to view configuration help through the following commands and change them.
```
python3 start.py --help
```

## Detailed Description

### All Optional Parameters of SetDroid

* ```-pro_click``` The proportion of click events, which is 45% by default.
* ```-pro_longclick``` The proportion of long-press events, which is 25% by default.
* ```-pro_scroll``` The proportion of scroll events, which is 5% by default.
* ```-pro_home``` The proportion of click home button events, which is 0% by default.
* ```-pro_edit``` The proportion of edit events, which is 15% by default.
* ```-pro_naturalscreen``` The proportion of rotating to natural events, which is 1% by default.
* ```-pro_leftscreen``` The proportion of rotating to left events, which is 8% by default.
* ```-pro_back``` The proportion of click back button events, which is 1% by default.
* ```-pro_splitscreen``` The proportion of split-screen events, which is 0% by default.
* ```-app_path``` the APK address of the app you want to test.
* ```-append_device``` The serial numbers of devices used in the test, which can be obtained by executing "adb devices" in the terminal.
* ```-android_system``` The Android system of the test device, At present, only Android 8.0 system is supported.
* ```-root_path``` The storage path of the output file.
* ```-resource_path``` The path of the resource file that you want to import into the test devices in advance.
* ```-testcase_count``` The number of rounds that you want to test for each strategy.
* ```-event_num``` The number of events in per round of test.
* ```-setting_random_denominator``` Used to adjust the frequency of setting change event insertion.
* ```-append_strategy``` The strategies that you want to use (multiple test strategies can be executed in sequence), currently, the supported strategies are as follows, corresponding to the 14 strategies listed in Table 5 of the paper.

|Strategy name|Setting|Oracle rule|Injection strategy|Pair of events for setting changes|
|---|---|---|---|---|
|network_immediate_1|Network| I| Immediate |⟨turn on airplane, turn off airplane⟩|
|network_lazy_1 |Network| I |Lazy| ⟨turn on airplane, turn off airplane⟩|
|network_lazy_2 |Network| I |Lazy| ⟨switch to mobile data, switch to Wi-Fi⟩|
|location_lazy_1| Location| I| Lazy| ⟨turn off location, turn on location⟩|
|location_lazy_2| Location| I| Lazy| ⟨switch to "device only", switch to "high accuracy"⟩|
|sound_lazy_1| Sound| I| Lazy| ⟨turn on "do not disturb", turn off "do not disturb"⟩|
|battery_immediate_1| Battery| I| Immediate| ⟨turn on the power saving mode, add the app into the whitelist⟩|
|battery_lazy_1| Battery| I| Lazy| ⟨turn on the power saving mode, turn off the power saving mode⟩|
|display_immediate_1| Display| I| Immediate| ⟨switch to landscape, switch to portrait⟩|
|display_immediate_2| Display| I| Immediate| ⟨turn on multi-window, turn off multi-window⟩|
|permssion_lazy_1| Permission| I| Lazy| ⟨turn off permission, turn on permission⟩|
|developer_lazy_1| Developer| I| Lazy| ⟨turn on "Don’t keep activities", turn off "Don’t keep activities"⟩|
|language| Language| II| -| ⟨change system language, -⟩|
|time| Time| II| -| ⟨change hour format, -⟩|

### Description of Output Files ([video tutorial](https://1drv.ms/u/s!AinXMMnLw-UDjgCWoQclrXqb6-xE?e=n6eiDy))

* The output path of the tool is in ```/home/setdroid/SetDroid/Root```. 
* The result files of each app are classified and stored in ```/home/setdroid/SetDroid/Root```. 
* Open the folder of an app, and you will see the result files of each strategy for this app are stored by category. 
* Open the folder corresponding to a strategy, and you will see an ```error_realtime.txt``` file, a ```wrong_realtime.txt``` file, and many numbered folders correspond to each round of test results. 
* Open a numbered folder, and you can see a ```read_trace.txt``` file, a ```trace.txt``` file, an ```i_trace.html``` file, and a folder named ```screen```. 
* Open the ```screen``` folder, and you can see the screenshot of each step and the corresponding interface layout information file. 
* Next, I will introduce the content and use of each file.

#### error_realtime.txt

This file records the sequences that trigger the setting defects, which start with ```Start::x::run_count::y``` (x means the x-th error and Y means the error was captured during the y-th round of execution), and end with ```End::```

#### wrong_realtime.txt

This file records the sequences that trigger the suspected setting defects.

#### read_trace.txt

This file records the execution sequence of SetDroid, which is easy for SetDroid users to read.

#### trace.txt

This file records the execution sequence of SetDroid, which can be read and replayed by SetDroid.

#### i_trace.html

This file records the sequence of screenshots after each step, which is arranged horizontally. The events executed at each step are marked on the screenshot. After opening the file in the browser, there is a drag bar at the bottom, which can drag horizontally to view the whole sequence. When the error is captured, the screenshot is marked with a red frame. When the two interfaces are different, the screen capture is marked with a yellow frame.

### Tool Extension

If someone wants to extend the artifact, they can modify it in the following position of the tool.

#### Add settings change strategy

Add a new setting change function in injector.py, and add calls to it to ```change_setting_before_run``` or ```inject_setting_during_run``` as needed.

#### Add seed test generation policy

Add a new exploration class according to ```RandomPolicy``` class in policy.py, and inherit the ```Policy``` class

#### Add a new check condition

Add a new check function in check.py and call it in the corresponding position in the ```executor.py```

### Main Maintainers

* [Jingling Sun](https://jinglingsun.github.io/) 
* [Ting Su](http://tingsu.github.io/) 

