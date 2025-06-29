# BatchExpAsc

**BatchExpAsc** is a powerful automation tool for Gothic modding that streamlines the process of batch converting ASC animations between different skeletal rigs. Built specifically for the Gothic and Gothic II modding community, it leverages Blender and KrxImpExp to efficiently retarget animations from one skeleton to another compatible one.

## 🎯 Purpose

The primary goal of BatchExpAsc is to automate the tedious process of manually retargeting animations when working with modified or enhanced skeletal rigs. This is particularly valuable when:

- **Adding new bones** to existing character armatures
- **Applying physics simulations** to movement animations through bone constraints
- **Migrating animations** between different character models with similar bone structures
- **Batch processing** large collections of ASC animation files

The tool automatically handles the retargeting process and exports updated animations to your specified output directory.

## ✨ Key Features

- **Automated Batch Processing**: Process multiple ASC animations simultaneously with configurable parallel processing
- **Flexible Skeleton Input**: Support for both standalone ASC skeleton files and Blender scene (.blend) files containing rigged skeletons
- **Physics Integration**: Automatically bake bone constraints (physics simulations) into keyframes during export
- **(!)Cross-Platform Compatibility**: Works on Windows, supposed to work on Linux (untested)
- **Configurable Workflow**: Comprehensive configuration system via INI file
- **Resource Optimization**: Intelligent CPU usage with automatic process count detection

## 🛠️ Technical Requirements

### Prerequisites

Ensure you have the following components installed before using BatchExpAsc:

| Component | Version | Purpose |
|-----------|---------|---------|
| **[Python](https://www.python.org/)** | 3.10+ | Core script execution |
| **[Blender](https://www.blender.org/)** | 3.6+ recommended | 3D processing and animation handling |
| **[KrxImpExp](https://gitlab.com/Patrix9999/krximpexp)** | Latest | Gothic ASC import/export functionality |

## 🚀 Quick Start

### 1. Configuration

Before running BatchExpAsc, configure your settings in `config.ini`. The configuration file contains detailed comments explaining each option:

```ini
# Example configuration structure (see config.ini for full details)
[Paths]
blender_exe_path = "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
blender_scene_path = "C:\Users\YourFancyName\Desktop\YourBlenderScene.blend"
body_asc_path = ""
anims_dir = "C:\Users\YourFancyName\Desktop\YourFancyAnimations"
output_dir = "C:\Users\YourFancyName\Desktop\YourExportedAnimations"
export_format = 0
```

### 2. Execution

#### Windows Users

Using PowerShell:
```powershell
./run.bat
```

or run this command directly from the script directory:

```powershell
python main.py -c config.ini -m 0
```

Using Command Prompt:
```cmd
run.bat
```

or

```cmd
python main.py -c config.ini -m 0
```

#### Linux Users

Using any terminal:
```bash
python main.py -c config.ini -m 0
```

## 📋 Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--config` | `-c` | Path to configuration file | `config.ini` |
| `--max_processes` | `-m` | Maximum concurrent processes (0 = auto-detect) | `0` |

### Usage Examples

```bash
# Use default configuration
python main.py

# Specify custom config file
python main.py -c custom_config.ini

# Limit to 4 parallel processes
python main.py -c config.ini -m 4

# Use custom config with single-threaded processing
python main.py -c my_config.ini -m 1
```

## ⚙️ Configuration Guide

### Skeleton Input Methods

BatchExpAsc supports two distinct approaches for providing the target skeleton:

#### Method 1: ASC Skeleton File
```ini
blender_scene_path = ""
body_asc_path = "C:\Users\YourFancyName\Desktop\YourAscSkeleton.asc"
```

Best for: Simple skeleton retargeting without additional modifications.

#### Method 2: Blender Scene File (Recommended)
```ini
blender_scene_path = "C:\Users\YourFancyName\Desktop\YourBlenderScene.blend"
body_asc_path = ""
```

**Advantages of Blender Scene Method:**
- **Physics Integration**: Bone constraints are automatically baked into keyframes
- **Enhanced Control**: Full access to Blender's rigging and constraint systems
- **Procedural Animation**: Support for secondary motion, cloth simulation, and dynamic effects
- **Custom Modifications**: Pre-configured skeleton modifications and enhancements

> **⚠️ Important**: You must choose either an ASC skeleton file **OR** a Blender scene file, not both.

## 🔧 Workflow Overview

1. **Input Validation**: Verify all required files and dependencies are available
2. **Skeleton Loading**: Import target skeleton from ASC file or Blender scene
3. **Animation Processing**: For each ASC animation file:
   - Import animation data
   - Apply to target skeleton
   - Process bone constraints (if using Blender scene method)
   - Bake physics/constraints into keyframes
   - Export retargeted animation
4. **Batch Export**: Save all processed animations to the specified output directory
5. **Cleanup**: Remove temporary files and provide processing summary

### Common Use Cases

- **Character Model Updates**: Retarget animations when switching between different character models
- **Skeleton Enhancement**: Add new bones for improved facial animation, cloth simulation, or accessory attachment
- **Physics Implementation**: Apply realistic secondary motion to hair, clothing, and equipment
- **Animation Library Management**: Standardize animation sets across multiple character variants

## 🤝 Contributing

Contributions are welcome! If you encounter issues or have suggestions for improvements:

1. Check if there are any issues in the repository
2. Create detailed bug reports with reproduction steps
3. Submit pull requests with clear descriptions of changes

## 📝 License

This project builds upon the Gothic modding community's collaborative efforts. Please respect the licensing terms of all dependencies, particularly KrxImpExp and Blender.

## 🙏 Acknowledgments

- **[Patrix](https://github.com/Patrix9999)** - Original concept, guidance, and KrxImpExp maintenance
- **V. Baranov** - Original KrxImpExp development
- **Gothic Modding Community** - Continued support and testing
- **Blender Foundation** - Providing the powerful 3D creation suite that makes this automation possible

---

**Need Help?** If you encounter issues or need assistance with BatchExpAsc, please create an issue in this repository with detailed information about your setup and the problem you're experiencing.
