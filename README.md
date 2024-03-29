

# wwwEnum, an opensource webapp enumeration tool

DISCLAIMER: The use of the tool called wwwEnum is at your own risk. I, as the creator of wwwEnum, am not responsible for any damages or unauthorized actions caused by its usage. **It is crucial that users understand the potential consequences of interacting with web servers and ensure they have proper authorization before utilizing wwwEnum. Users should possess a comprehensive understanding of how web servers may respond to their actions.** Please exercise caution and act responsibly.


## The idea:
On an improperly configured pfSense server, distinct responses are generated depending on the existence of specific files. 
For example, requesting "x.x.x.x/wizards" may result in a 403 Forbidden error, while "x.x.x.x/help.php" could produce a 404 or 200 status code, depending on file existence.
By leveraging these file availability differences across different pfSense versions, it becomes possible to narrow down and identify the specific version in use.

NOTE: For private repo's you will have to edit the script to use authorization tokens

## Usage:

```
python init.py
python init2.py
python differences.py
python wordlistgenerator.py
```
Then manually inspect the json files.


## Details 

There are 6 python scripts.
The execution order is

0. (Optional) getversions.py  -> used by initWithVersions
1. (init1.py, init2.py) OR initWithVersions.py. 
2. differences.py
3. (Optional) wordlistgenerator.py -> use with dirbuster

"init.py" and "init2.py" create a csv file of every item in the designated branches. They are not a user friendly scripts. They are essentially the same file, however in my POC, pfsense, the /www directory changes paths. For versions 1_2, 2_0, 2_1 and 2_2 the path is path = "usr/local/www". In every other branch, the path is "src/usr/local/www". paths to repos will have to be set manually. Versions will have to be listed manually. Any deviations will have to be accounted for manually. 

"initWithVersions.py" is useful if every /www path is the same. Run, getversions.py first to generate a text file containing every possible branch. Then initWithVersions will just create csv files for every version listed in versions.txt

"generatewordlist.py" -- This generates wordlist.txt which can now be used to fuzz the targets files and directories, in my case pfsense.

"differencesgenerator.py" creates N json files, one for every version. In each json, it shows the differences between the given version and every other version. Example
master.json will show the differences between master and 1_2, master and 2_0, master and 2_1, etc... NOTE: There is alot of redundant data, in the future I'll try to create a more streamlined file.

## POC

Take the example image below of the "master.json" file generated by "differencesgenerator.py" . This json shows the differences between master and every other version. Added files indicates that the master branch has these files while the other branch does not. Missing files indicates the revese; In other words, the opposing version has the file but the master branch does not.

![image](https://github.com/Szwochm/wwwEnum/assets/1501624/79197d57-f745-46f3-8b7a-8bfc9cc8837c)



As you can see there are no files to distingish between the master branch, and RELENG_2_6_0. However master has the file system_register.php, and 2_5_1 does not. We can quickly verify this on the github to ensure that the script is functioning.

![image](https://github.com/Szwochm/wwwEnum/assets/1501624/fff83f9a-e0f5-45bf-b751-7cf6fbf06f4a)



So now when we request <IP>/system_register.php we get a 200 code.
 
 
 
 ![image](https://github.com/Szwochm/wwwEnum/assets/1501624/b8fd7611-ae82-4dbf-87ec-4234eb4fdf58)
 
 This indicates that this file does exist, thus we can make an educated guess that the version of pfsense is either 2_6_0 or the master branch.
 NOTE: Sometimes it appears that nothing happens. If you receive a 200 request on some files, and a 404 on others, that is a strong indication that this method workds. 403's may or may not indicate the existence of a file / directory.
 
 To further verify we can try files from other versions
 
![image](https://github.com/Szwochm/wwwEnum/assets/1501624/fe071ebe-5d1a-4fc7-9a46-dfcc04c812c5)
 
 On attempting the request to csrf_error.php which exists on master but not 2_4_3 we get the following...
 ![image](https://github.com/Szwochm/wwwEnum/assets/1501624/efa3a36e-692c-40b2-8aa1-15ab1214f8e6)

 So obviously the file exists. This is in the "added files" section indicating that the master branch has this file but 2_4_3 does not. -- Note review the disclaimer. Know what will happen if you request arbitary files on a webapp.
 
 Lets try one more file to verify that it cannot be 2_4_3.
 
 ![image](https://github.com/Szwochm/wwwEnum/assets/1501624/70227378-860e-4d52-b9db-22625156d342)

 This file was in the missing section of the master.json file. This indicates that the master branch is missing this file, while 2_4_3 has this file.
 And there you have it. Based on the following steps I think you can safely assume that the pfsense version being used is either 2_6_0 or master.
 
 
Future plans: 
 
 1) Combine all of the scripts into one for convienance and easier usability.
 
 2) Optimize so that the scripts aren't redundant, and for faster speed.










