# Introduction

**BatchExpAsc** is a utility script. It utilizes [Blender](https://www.blender.org/) and [KrxImpExp](https://gitlab.com/Patrix9999/krximpexp) to batch port ASC animations from Gothic from one skeleton to another similar one.

Its primary purpose is to export provided animations applied to a certain skeleton.
Provided skeleton should at least contain all the bones that are present in the skeleton used in animations.

This can be very helpful if you want to add a new bones to your armature, or apply physics to every movement animation.  
The updated animations will be automatically exported to the given output directory.

# Requirements

Before using the script, make sure that you've installed all of the required components for this script.

- [python](https://www.python.org/)
- [Blender](https://www.blender.org/)
- [KrxImpExp](https://gitlab.com/Patrix9999/krximpexp)

# Usage

Before running the script, adjust the settings in [config.ini](/config.ini) to your needs.  
Make sure to set all of the options correctly, just read the comments and follow the guide.

### Windows

Open up the **powershell** in the main project directory and type:
```
./run.bat
```

Or in CMD:
```
run.bat
```

### Other

Open up **any terminal** in the main project directory and use this command:
```
python main.py -c config.ini -m 0
```

### Arguments

- `-c, --config` : Path to the config file
- `-m, --max_processes` : Maximum number of processes to use (calculated automatically based on CPU count if not set)

### Configuration

Instead of using a skeleton `.ASC` file, it is possible and **recommended** to use a skeleton from a pre-created Blender scene (`.blend` file)
containing one. It is useful in cases when the goal is to add a procedurally generated secondary movements to a certain bones in the skeleton (physics).
In Blender it is done by bone constraints, KrxImpExp bakes the constraints into keyframes automatically thus by providing a Blender scene with 
the skeleton that has constraints applied to it you can batch bake those constraints into keyframes and export them for each animation.

**Important: you must either provide a skeleton or a `.blend` scene, not both.**

For more details see [config.ini](/config.ini)

# Aknowledgements

- [Patrix](https://github.com/Patrix9999) - For the idea and readme file for this script
