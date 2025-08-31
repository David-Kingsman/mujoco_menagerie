# UFACTORY Robots Visualization

Visualization and analysis tools for UFACTORY robots in MuJoCo.

## 🤖 Supported Robots

- **XArm 6** - 6 DOF collaborative robot
- **XArm 7** - 7 DOF collaborative robot  
- **Lite 6** - Lightweight 6 DOF robot
- **UF850** - 6 DOF industrial robot

## 🚀 Quick Start

```bash
# Run main demo with all robots
python3 ufactory_robots_demo.py

# Run individual robot demos
python3 xarm6_robot_descriptions.py
python3 xarm7_robot_descriptions.py
python3 lite6_robot_descriptions.py
python3 uf850_robot_descriptions.py
```

## 🎮 3D Visualization

```bash
# XArm 6
python -m mujoco.viewer --mjcf ../ufactory_xarm6/scene.xml

# XArm 7
python -m mujoco.viewer --mjcf ../ufactory_xarm7/scene.xml

# Lite 6
python -m mujoco.viewer --mjcf ../ufactory_lite6/scene.xml

# UF850
python -m mujoco.viewer --mjcf ../ufactory_uf850/scene.xml
```

## 📁 Files

- **`ufactory_robots_demo.py`** - Main demo with all robots
- **`xarm6_robot_descriptions.py`** - XArm 6 dedicated script
- **`xarm7_robot_descriptions.py`** - XArm 7 dedicated script
- **`lite6_robot_descriptions.py`** - Lite 6 dedicated script
- **`uf850_robot_descriptions.py`** - UF850 dedicated script
- **`README_UFACTORY_Robots.md`** - Detailed documentation

## 🔧 Features

- Robot model loading and validation
- Forward kinematics testing
- Joint and actuator information
- Workspace analysis
- Robot comparison tables
- 3D interactive visualization

**Tip**: Start with `ufactory_robots_demo.py` to see all robots in action!
