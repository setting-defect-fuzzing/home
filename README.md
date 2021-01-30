# Study Dataset

We publish the usage data sets used in our research in the folder "Study Dataset".

### project_lists

This file contains all the Android projects officially released on Google Play and F-Droid that we obtained through GitHub's REST API. We listed their repo names, the number of closed issues, the number of open issues, and the number of stars on GitHub. We keep the apps with more than 200 issues in this list as study objects, a total of 180 apps.

### setting_keyword_issues

This file contains all issues of 180 apps obtained through keyword filtering. We listed their repo name, url, open time, closed time, and setting keywords mentioned in the issue.

### study_list

This file contains 1,074 setting issues of 180 apps that we obtained through manual inspection. For each issue, we listed its url, consequence, whether it was closed, whether it was repaired, the length of the reproduce steps reported by the reporter, the setting that caused the issue, and the root cause of the issue.

### speciﬁc_APIs_list

This file lists the specific APIs that we used when investigating the usage of settings in the apps. We listed their corresponding setting categories, the classes they belong to, and the forms used in the static analysis.

### usage_of_settings

This file lists the APIs related to the setting categories used by each app. For each app, we counted the usage of six settings. The number 1 means that at least one API corresponding to this setting category has been detected in the code of the app.

# SetDroid

### Download

```
git clone https://github.com/setting-defect-fuzzing/home.git
```

### Environment

If your system has the following support, you can run SetDroid normally
- Python 3.8

We use some libraries provided by python, you can add them as prompted, for example:
```
pip install langid
```
- Android SDK: API 26+

You can create an emulator before running SetDroid. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you to start using SetDroid quickly：
```
sdkmanager "system-images;android-26;google_apis;x86"
avdmanager create avd --force --name Android8.0 --package 'system-images;android-26;google_apis;x86' --abi google_apis/x86 --sdcard 512M --device "pixel_xl"
```
Next, you can start two identical emulators and assign their port numbers with the following commands:
```
emulator -avd Android8.0 -read-only -port 5554 &
emulator -avd Android8.0 -read-only -port 5556 &
```
### Run
If you have downloaded our project and configured the environment, you only need to enter "download_path/home/setdroid/tool" to execute our sample app with the following command:
```
python complex.py
```
SetDroid provides several ways to test android apps by command lines. You need to view configuration help through the following commands and change them.
```
python complex.py --help
```

# Bugs detected by SetDroid

|Issue ID|App name|\#Downloads|\#Stars|Bug state|Cause setting|Consequence|
|---|---|---|---|---|---|---|
|1|APhotoManager|-|162|Confirmed|Permission|Crash|
|2|A2DP Volume|100K-500K|71|Fixed|Display|Crash|
|3|A2DP Volume|100K-500K|71|Fixed|Display|Data Lost|
|4|A2DP Volume|100K-500K|71|Fixed|Display|Crash|
|5|A2DP Volume|100K-500K|71|Fixed|Display & Permission|Data Lost|
|6|A2DP Volume|100K-500K|71|Confirmed|Developer|Function failure|
|7|AlwaysOn|10M-50M|121|Confirmed|Language|Disrespect of Settings|
|8|AlwaysOn|10M-50M|121|Confirmed|Language|Incomplete Translation(5)|
|9|AnkiDroid|5M-10M|3.2K|Fixed|Permission|Stuck|
|10|AntennaPod|500K-1M|3.3K|Fixed|Network|Lack of Refresh|
|11|Commons|50K-100K|649|Discussion|Location|Infinite Loading|
|12|Commons|50K-100K|649|Confirmed|Permission|Crash|
|13|Forecastie|10K-50K|609|Fixed|Permission|Lack of Prompt|
|14|Forecastie|10K-50K|609|Fixed|Language|Incomplete Translation(5)|
|15|Forecastie|10K-50K|609|Confirmed|Display|Data Lost|
|16|Good Weather|5K-10K|196|Waiting|Network|Infinite Loading|
|17|Good Weather|5K-10K|196|Waiting|Location|Lack of Prompt|
|18|Good Weather|5K-10K|196|Waiting|Language|Language Confusion|
|19|Materialistic|100K-500K|2.1K|Waiting|Network|Lack of Refresh|
|20|Omni Notes|100K-500K|2.2K|Fixed|Permission|Lack of Prompt|
|21|Omni Notes|100K-500K|2.2K|Fixed|Location|Error Prompt|
|22|Omni Notes|100K-500K|2.2K|Fixed|Language|Disrespect of Settings|
|23|Omni Notes|100K-500K|2.2K|Fixed|Language|Incomplete Translation(2)|
|24|Opensuduku|10K-50K|209|Confirmed|Language|Incomplete Translation(7)|
|25|RedReader|50K-100K|1.1K|Discussion|Network|Infinite Loading|
|26|RedReader|50K-100K|1.1K|Confirmed|Language|Incomplete Translation(23)|
|27|Timber|100K-500K|6.4k|Confirmed|Display|Data Lost|
|28|Timber|100K-500K|6.4k|Waiting|Permission|Crash|
|29|Timber|100K-500K|6.4k|Waiting|Language|Incomplete Translation(9)|
|30|Vanilla Music|500K-1M|777|Waiting|Display|Crash|
|31|OpenBikeSharing|1K-5K|58|Confirmed|Display|Function Failure|
|32|Suntimes|-|134|Fixed|Location|Infinite Loading|
|33|RadioBeacon|-|43|Confirmed|Network|Stuck|
|34|RadioBeacon|-|43|Confirmed|Permission|Crash|
|35|RunnerUp|10K-50K|511|Fixed|Permission|Lack of Prompt|
|36|Amaze|1M-5M|3K|Fixed|Display & Permission|Black Screen|
|37|Amaze|1M-5M|3K|Fixed|Display & Permission|Data Lost|
|38|Amaze|1M-5M|3K|Fixed|Network|Lack of Prompt|
|39|Amaze|1M-5M|3K|Fixed|Display & Permission|Crash|
|40|Amaze|1M-5M|3K|Fixed|Permission|Crash|
|41|Habits|1M-5M|3.6K|Fixed|Display|Data Lost|
|42|Habits|1M-5M|3.6K|Fixed|Language|Incomplete Translation(2)|