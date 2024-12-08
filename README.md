# Introduction

**BatchExpAsc** is a utility script for [Blender](https://www.blender.org/) that utilizes [KrxImpExp](https://gitlab.com/Patrix9999/krximpexp).

Its primary purpose is to import animations and update their skeleton using a provided **armature model**.  
The new animations with updated skeleton will be exported to given directory.

This script can be very helpful if you want to add a new bones to your armature, or apply physics to every movement animation.  
The updated animations will be automatically exported to the given output directory.

# Requirements

Before using the script, make sure that you've installed all of the required components for this script.

- [python](https://www.python.org/)
- [Blender](https://www.blender.org/)
- [KrxImpExp](https://gitlab.com/Patrix9999/krximpexp)

# Usage

Before running the script, adjust the settings in [config.ini](/config.ini) to your needs.  
Make sure to set all of the options correctly, just read the comments and follow the guide.

### Batch script

Open up the **powershell** in the main project directory and type:
```
./run.bat
```

### Generic command

Open up **any terminal** in the main project directory and type this command:
```
python main.py -c config.ini -m 0
```