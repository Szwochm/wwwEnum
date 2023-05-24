wwwEnum
+=======================================+
The idea:
On an improperly configured pfSense server, distinct responses are generated depending on the existence of specific files. 
For example, requesting "x.x.x.x/wizards" may result in a 403 Forbidden error, while "x.x.x.x/help.php" could produce a 404 or 200 status code, depending on file existence.
By leveraging these file availability differences across different pfSense versions, it becomes possible to narrow down and identify the specific version in use.

The stealthy way will use an optimal path to make as few requests as possible

The loud way will check every possible file and make a prediction based on the response
+=======================================+

How it works:

init.py and init2.py grab every branch from github. they are essentially the same file
However in my POC, pfsense, the /www directory changes paths. for versions 1_2, 2_0, 2_1 and 2_2 the path is path = "usr/local/www"
For every other branch, the path is "src/usr/local/www".

After generating the csvs, I move them all into a seperate folder versionscvs. In this folder  I use "generatewordlist.py".
This generates wordlist.txt which can now be used to fuzz the targets files and directories, in my case pfsense.

"changes.py" aims to automate the process described below by "manualEnum.py". Still a work in progress

"manualEnum.py" generates differences_versions.txt. This is an easy to read text file you can use to manually figure out
which version is being used. For example consider this excerpt:

File Name Differences between RELENG_2_4_4 and RELENG_2_4_3.csv:
Files missing from first version:
- license.php
Files missing from second version:
+ services_acb.php
+ csrf_error.php
+ status_unbound.php
+ services_acb_backup.php
+ services_acb_settings.php

File Name Differences between RELENG_2_4_3 and RELENG_2_4_2.csv:
Files missing from first version:
- copynotice.inc
Files missing from second version:
+ getqueuestats.php

Using this info, we can try <IP>/license.php. If we get a 403 forbidden or 200, we know that the version cannot be 2_4_4.
We can then try <IP>/getqueuestats. If this returns a 404, we know it cannot be 2_4_2. Using this process of logic and elimination
we can narrow down which version is the mostly likely to be used.
 If this returns a 404 not found, we know that the target is likely not the master branch.






