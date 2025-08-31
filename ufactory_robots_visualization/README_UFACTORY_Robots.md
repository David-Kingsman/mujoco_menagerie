# UFACTORY Robots Visualization

This project provides comprehensive visualization and analysis tools for UFACTORY robots in MuJoCo, including XArm 6, XArm 7, Lite 6, and UF850 robots.

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- MuJoCo Python bindings
- robot_descriptions package (optional)

### Installation

```bash
# Install required packages
pip install mujoco robot_descriptions numpy

# Navigate to the visualization folder
cd ufactory_robots_visualization
```

### Running the Demos

```bash
# Run the main demo with all robots
python3 ufactory_robots_demo.py

# Run individual robot demos
python3 xarm6_robot_descriptions.py
python3 xarm7_robot_descriptions.py
python3 lite6_robot_descriptions.py
python3 uf850_robot_descriptions.py
```

### 3D Visualization

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

## 📁 File Descriptions

### Individual Robot Scripts

- **`xarm6_robot_descriptions.py`** - XArm 6 robot visualization and analysis
- **`xarm7_robot_descriptions.py`** - XArm 7 robot visualization and analysis
- **`lite6_robot_descriptions.py`** - Lite 6 robot visualization and analysis
- **`uf850_robot_descriptions.py`** - UF850 robot visualization and analysis

### General Demo Script

- **`ufactory_robots_demo.py`** - Comprehensive demo with all UFACTORY robots

### Documentation

- **`README.md`** - Quick start guide
- **`README_UFACTORY_Robots.md`** - Detailed documentation (this file)

## 🤖 Robot Models

### XArm 6
- **Joints**: 6 DOF
- **Max Payload**: 5kg
- **Workspace Radius**: 700mm
- **Applications**: Light assembly, pick and place, education

### XArm 7
- **Joints**: 7 DOF
- **Max Payload**: 5kg
- **Workspace Radius**: 700mm
- **Applications**: Light assembly, pick and place, education, research

### Lite 6
- **Joints**: 6 DOF
- **Max Payload**: 3kg
- **Workspace Radius**: 500mm
- **Applications**: Light assembly, education, research, desktop automation

### UF850
- **Joints**: 6 DOF
- **Max Payload**: 5kg
- **Workspace Radius**: 850mm
- **Applications**: Assembly, pick and place, education, research

## 🔧 Usage

### Basic Robot Information

Each script provides:
- Robot model loading and validation
- Joint and actuator information
- Geometry details
- Forward kinematics testing

### Movement Testing

The scripts test predefined positions:
- **Home Position**: All joints at zero
- **Extended Position**: Extended arm configuration
- **Bent Position**: Bent arm configuration
- **Side Position**: Side-reaching configuration

### Comparison Analysis

The main demo script provides:
- Technical parameter comparison
- Performance metrics comparison
- Workspace analysis

## 🎯 Features

### Model Loading
- Automatic fallback from robot_descriptions to Menagerie
- Path validation and error handling
- Model integrity checks

### Forward Kinematics
- End-effector position calculation
- Workspace radius computation
- Multiple test positions

### Robot Comparison
- Side-by-side parameter comparison
- Performance metrics analysis
- Application suitability assessment

## 🛠️ Troubleshooting

### Common Issues

1. **Model Loading Errors**
   ```bash
   # Check if model files exist
   ls ../ufactory_xarm6/xarm6.xml
   ls ../ufactory_xarm7/xarm7.xml
   ls ../ufactory_lite6/lite6.xml
   ls ../ufactory_uf850/uf850_nohand.xml
   ```

2. **MuJoCo Installation Issues**
   ```bash
   # Reinstall MuJoCo
   pip uninstall mujoco
   pip install mujoco
   ```

3. **Python Version Issues**
   ```bash
   # Ensure Python 3.7+
   python3 --version
   ```

### Error Messages

- **"Model file not found"**: Check file paths and ensure models are in the correct directories
- **"robot_descriptions package not installed"**: Install with `pip install robot_descriptions`
- **"Failed to load robot model"**: Verify MuJoCo installation and model file integrity

## 🔍 Extended Features

### Custom Joint Positions

You can modify the test positions in each script:

```python
# Example: Add custom position
test_positions = [
    ("Custom Position", [0.5, -0.3, 1.2, -0.8, 0.1, 0.9])
]
```

### Workspace Analysis

The scripts calculate workspace radius for each position:

```python
# Workspace radius calculation
radius = np.sqrt(x**2 + y**2 + z**2)
```

### Model Exploration

Access detailed model information:

```python
# Joint information
joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "joint1")

# Geometry information
geom_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i)
```

## 📚 Resources

### UFACTORY Documentation
- [XArm Official Documentation](https://www.ufactory.cc/xarm)
- [Lite 6 Documentation](https://www.ufactory.cc/lite6)
- [UF850 Documentation](https://www.ufactory.cc/uf850)

### MuJoCo Resources
- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)
- [robot_descriptions Package](https://github.com/robot-descriptions/robot_descriptions)

### Related Projects
- [Universal Robots Visualization](../universal_robots_visualization/)
- [MuJoCo Menagerie Models](../)

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with multiple robot models
5. Submit a pull request

## 📄 License

This project is part of the MuJoCo Menagerie visualization tools and follows the same license terms.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Verify model file integrity
3. Test with individual robot scripts
4. Review MuJoCo documentation

---

**Note**: This visualization project is designed for educational and research purposes. For production use, refer to official UFACTORY documentation and support.
