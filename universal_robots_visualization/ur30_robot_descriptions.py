#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for loading UR30 robot using robot_descriptions package
"""

import mujoco
import numpy as np
import os

def load_ur30_with_robot_descriptions():
    """Load UR30 robot using robot_descriptions package"""
    try:
        from robot_descriptions.loaders.mujoco import load_robot_description
        
        print("Loading UR30 robot using robot_descriptions...")
        
        # Try to load UR30 robot
        try:
            model = load_robot_description("ur30_mj_description")
            print("✓ Successfully loaded UR30 robot using robot_descriptions!")
            return model
        except Exception as e:
            print("UR30 not found in robot_descriptions, trying other methods...")
            print("Error: {}".format(e))
            return None
            
    except ImportError:
        print("robot_descriptions package not installed")
        return None

def load_ur30_from_menagerie():
    """Load UR30 robot from MuJoCo Menagerie"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory to reach the menagerie root
    menagerie_dir = os.path.dirname(current_dir)
    ur30_path = os.path.join(menagerie_dir, "universal_robots_ur30", "ur30_fixed.xml")
    
    if os.path.exists(ur30_path):
        print("Loading UR30 robot from MuJoCo Menagerie...")
        model = mujoco.MjModel.from_xml_path(ur30_path)
        print("✓ Successfully loaded UR30 robot from Menagerie!")
        return model
    else:
        print("Error: UR30 model file not found")
        return None

def explore_ur30_model(model):
    """Explore UR30 robot model"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("UR30 Robot Model Information")
    print("="*50)
    
    # Basic information
    print("Basic Information:")
    print("  Joints: {}".format(model.njnt))
    print("  Actuators: {}".format(model.nu))
    print("  Geometries: {}".format(model.ngeom))
    print("  Bodies: {}".format(model.nbody))
    
    # Joint information
    print("\nJoint Information:")
    joint_names = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", 
                  "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    
    for i, name in enumerate(joint_names):
        if i < model.njnt:
            joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
            if joint_id >= 0:
                joint_type = mujoco.mjtJoint(model.jnt_type[joint_id])
                if model.jnt_limited[joint_id]:
                    range_info = "Range: [{:.2f}, {:.2f}]".format(
                        model.jnt_range[joint_id, 0], 
                        model.jnt_range[joint_id, 1]
                    )
                else:
                    range_info = "Unlimited"
                print("  {}: {} (Type: {}, {})".format(i, name, joint_type, range_info))
    
    # Actuator information
    print("\nActuator Information:")
    actuator_names = ["shoulder_pan", "shoulder_lift", "elbow", "wrist_1", "wrist_2", "wrist_3"]
    
    for i, name in enumerate(actuator_names):
        if i < model.nu:
            print("  {}: {} (Type: {})".format(i, name, get_actuator_type(model, i)))
    
    # Geometry information
    print("\nGeometry Information:")
    for i in range(min(model.ngeom, 15)):  # Show first 15 geometries
        geom_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i)
        if geom_name:
            geom_type = mujoco.mjtGeom(model.geom_type[i])
            print("  {}: {} (Type: {})".format(i, geom_name, geom_type))

def get_actuator_type(model, actuator_id):
    """Get actuator type"""
    if actuator_id < model.nu:
        # Determine type based on actuator class
        if hasattr(model, 'actuator_class'):
            class_id = model.actuator_class[actuator_id]
            if class_id == 0:  # size4
                return "High Power (330Nm)"
            elif class_id == 1:  # size3
                return "Medium Power (150Nm)"
            elif class_id == 2:  # size2
                return "Low Power (56Nm)"
        return "Standard Actuator"
    return "Unknown"

def test_ur30_movement(model):
    """Test UR30 robot movement"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("Testing UR30 Robot Movement")
    print("="*50)
    
    # Create data object
    data = mujoco.MjData(model)
    
    # Define test positions (UR30 joint ranges may be different)
    test_positions = [
        ("Home Position", [-1.5708, -1.5708, 1.5708, -1.5708, -1.5708, 0]),
        ("Extended Position", [0, -1.5708, 0, -1.5708, 0, 0]),
        ("Bent Position", [-3.1415, -0.785, 1.5708, -2.356, 0, 0]),
        ("Side Position", [-1.5708, -1.5708, 0, -1.5708, 0, 1.5708])
    ]
    
    for name, qpos in test_positions:
        print("\nTest Position: {}".format(name))
        
        # Set joint positions
        if len(qpos) <= model.njnt:
            data.qpos[:len(qpos)] = qpos
            
            # Forward kinematics
            mujoco.mj_forward(model, data)
            
            # Get end effector position
            if model.nbody > 0:
                end_effector_pos = data.xpos[-1]
                print("  End Effector Position: [{:.3f}, {:.3f}, {:.3f}]".format(
                    end_effector_pos[0], end_effector_pos[1], end_effector_pos[2]
                ))
                
                # Calculate workspace radius
                radius = np.sqrt(end_effector_pos[0]**2 + end_effector_pos[1]**2 + end_effector_pos[2]**2)
                print("  Workspace Radius: {:.3f}m".format(radius))

def compare_ur5e_ur30():
    """Compare UR5e and UR30 differences"""
    print("\n" + "="*50)
    print("UR5e vs UR30 Comparison")
    print("="*50)
    
    print("Main Differences:")
    print("  UR5e:")
    print("    - Max Payload: 5kg")
    print("    - Workspace: 850mm radius")
    print("    - Repeatability: ±0.03mm")
    print("    - Actuator Power: Medium")
    
    print("  UR30:")
    print("    - Max Payload: 30kg")
    print("    - Workspace: 1750mm radius")
    print("    - Repeatability: ±0.05mm")
    print("    - Actuator Power: High Power")
    
    print("\nApplication Scenarios:")
    print("  UR5e: Precision assembly, laboratory research, education")
    print("  UR30: Heavy lifting, industrial manufacturing, logistics")

def main():
    """Main function"""
    print("Loading UR30 Robot using robot_descriptions")
    print("="*50)
    
    # Try to load using robot_descriptions
    model = load_ur30_with_robot_descriptions()
    
    # If failed, load from Menagerie
    if model is None:
        model = load_ur30_from_menagerie()
    
    if model is not None:
        # Explore model
        explore_ur30_model(model)
        
        # Test movement
        test_ur30_movement(model)
        
        # Comparison information
        compare_ur5e_ur30()
        
        print("\n" + "="*50)
        print("UR30 model loaded successfully!")
        print("To start interactive viewer, run:")
        print("python -m mujoco.viewer --mjcf ../universal_robots_ur30/scene.xml")
        print("="*50)
    else:
        print("Failed to load UR30 robot model")

if __name__ == "__main__":
    main()
