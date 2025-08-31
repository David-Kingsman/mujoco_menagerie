# Universal Robots Visualization in MuJoCo

This folder contains scripts and documentation for visualizing Universal Robots UR5e and UR30 robots in MuJoCo.

## 📁 Contents

- **`universal_robots_demo.py`** - Main script showing both robots with comparison
- **`ur5e_robot_descriptions.py`** - UR5e dedicated script
- **`ur30_robot_descriptions.py`** - UR30 dedicated script
- **`README_Universal_Robots.md`** - Detailed documentation

## 🚀 Quick Start

```bash
# Navigate to this folder
cd universal_robots_visualization

# Run main demo (recommended)
python3 universal_robots_demo.py

# Run individual demos
python3 ur5e_robot_descriptions.py
python3 ur30_robot_descriptions.py
```

## 🖥️ 3D Visualization

From this folder, run:

```bash
# UR5e viewer
python -m mujoco.viewer --mjcf ../universal_robots_ur5e/scene.xml

# UR30 viewer
python -m mujoco.viewer --mjcf ../universal_robots_ur30/scene.xml
```

## 🤖 Robot Comparison

| Feature | UR5e | UR30 |
|---------|------|------|
| **Max Payload** | 5kg | 30kg |
| **Workspace** | 850mm | 1750mm |
| **Repeatability** | ±0.03mm | ±0.05mm |
| **Power** | Medium | High |

## 📚 Features

- ✅ Automatic robot loading via robot_descriptions
- ✅ Complete model information display
- ✅ Movement testing with predefined positions
- ✅ Performance comparison analysis
- ✅ 3D visualization support
- ✅ Object-oriented design for easy extension

## 🔗 Resources

- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)
- [Universal Robots](https://www.universal-robots.com/)

---

**Tip**: Start with `universal_robots_demo.py` to see both robots in action!
