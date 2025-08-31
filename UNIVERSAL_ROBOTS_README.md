# Universal Robots Visualization

This directory contains a dedicated folder for Universal Robots visualization scripts.

## 📁 Universal Robots Visualization

All Universal Robots related scripts and documentation are now organized in the `universal_robots_visualization/` folder.

### Quick Access

```bash
# Navigate to the visualization folder
cd universal_robots_visualization

# Run the main demo
python3 universal_robots_demo.py

# Run individual robot demos
python3 ur5e_robot_descriptions.py
python3 ur30_robot_descriptions.py
```

### 3D Visualization

From the visualization folder:

```bash
# UR5e 3D viewer
python -m mujoco.viewer --mjcf ../universal_robots_ur5e/scene.xml

# UR30 3D viewer
python -m mujoco.viewer --mjcf ../universal_robots_ur30/scene.xml
```

### Contents

The `universal_robots_visualization/` folder contains:

- **`universal_robots_demo.py`** - Main script with both robots
- **`ur5e_robot_descriptions.py`** - UR5e dedicated script
- **`ur30_robot_descriptions.py`** - UR30 dedicated script
- **`README.md`** - Quick start guide
- **`README_Universal_Robots.md`** - Detailed documentation

---

**Note**: All scripts are now organized in the dedicated folder for better project structure.
