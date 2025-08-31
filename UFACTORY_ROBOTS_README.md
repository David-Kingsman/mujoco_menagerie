# UFACTORY Robots Visualization

This directory contains a dedicated folder for UFACTORY robots visualization scripts.

## 📁 UFACTORY Robots Visualization

All UFACTORY robots related scripts and documentation are now organized in the `ufactory_robots_visualization/` folder.

### Quick Access

```bash
# Navigate to the visualization folder
cd ufactory_robots_visualization

# Run the main demo
python3 ufactory_robots_demo.py

# Run individual robot demos
python3 xarm6_robot_descriptions.py
python3 xarm7_robot_descriptions.py
python3 lite6_robot_descriptions.py
python3 uf850_robot_descriptions.py
```

### 3D Visualization

From the visualization folder:

```bash
# XArm 6 3D viewer
python -m mujoco.viewer --mjcf ../ufactory_xarm6/scene.xml

# XArm 7 3D viewer
python -m mujoco.viewer --mjcf ../ufactory_xarm7/scene.xml

# Lite 6 3D viewer
python -m mujoco.viewer --mjcf ../ufactory_lite6/scene.xml

# UF850 3D viewer
python -m mujoco.viewer --mjcf ../ufactory_uf850/scene.xml
```

### Contents

The `ufactory_robots_visualization/` folder contains:

- **`ufactory_robots_demo.py`** - Main script with all robots
- **`xarm6_robot_descriptions.py`** - XArm 6 dedicated script
- **`xarm7_robot_descriptions.py`** - XArm 7 dedicated script
- **`lite6_robot_descriptions.py`** - Lite 6 dedicated script
- **`uf850_robot_descriptions.py`** - UF850 dedicated script
- **`README.md`** - Quick start guide
- **`README_UFACTORY_Robots.md`** - Detailed documentation

---

**Note**: All scripts are now organized in the dedicated folder for better project structure.
