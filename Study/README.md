## Study Dataset

### project_lists.xlsx

This file contains all the Android projects officially released on Google Play and F-Droid that we obtained through GitHub's REST API. We listed their repo names, the number of closed issues, the number of open issues, and the number of stars on GitHub. We keep the apps with more than 200 issues in this list as study objects, a total of 180 apps.

### app_infomation.xlsx (corresponding to Figure 2 in our paper)

This file contains all the information (star numbers, issue numbers, installations, and categories) of our study objects, corresponding to the data in Figure 2 in the paper.

### setting_keyword_issues.xlsx

This file contains all issues of 180 apps obtained through keyword filtering. We listed their repo name, URL, open time, closed time, and setting keywords mentioned in the issue.

### study_list.xlsx (corresponding to Table 3 in our paper)

This file contains 1,074 setting issues of 180 apps that we obtained through manual inspection. For each issue, we listed its URL, consequence, whether it was closed, whether it was repaired, the length of the reproduce steps reported by the reporter, the setting that caused the issue, and the root cause of the issue.

### specific_APIs_list.xlsx

This file lists the specific APIs that we used when investigating the usage of settings in the apps. We listed their corresponding setting categories, the classes they belong to, and the forms used in the static analysis.

### usage_of_settings.xlsx (corresponding to Table 2 in our paper)

This file lists the APIs related to the setting categories used by each app. For each app, we counted the usage of six settings. The number 1 means that at least one API corresponding to this setting category has been detected in the code of the app.