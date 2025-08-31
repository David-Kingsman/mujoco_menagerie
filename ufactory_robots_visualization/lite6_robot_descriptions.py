#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for loading Lite 6 robot using robot_descriptions package
"""

import mujoco
import numpy as np
import os

def load_lite6_with_robot_descriptions():
    """Load Lite 6 robot using robot_descriptions package"""
    try:
        from robot_descriptions.loaders.mujoco import load_robot_description
        
        print("Loading Lite 6 robot using robot_descriptions...")
        
        # Try to load Lite 6 robot
        try:
            model = load_robot_description("lite6_mj_description")
            print("✓ Successfully loaded Lite 6 robot using robot_descriptions!")
            return model
        except Exception as e:
            print("Lite 6 not found in robot_descriptions, trying other methods...")
            print("Error: {}".format(e))
            return None
            
    except ImportError:
        print("robot_descriptions package not installed")
        return None

def load_lite6_from_menagerie():
    """Load Lite 6 robot from MuJoCo Menagerie"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory to reach the menagerie root
    menagerie_dir = os.path.dirname(current_dir)
    lite6_path = os.path.join(menagerie_dir, "ufactory_lite6", "lite6.xml")
    
    if os.path.exists(lite6_path):
        print("Loading Lite 6 robot from MuJoCo Menagerie...")
        model = mujoco.MjModel.from_xml_path(lite6_path)
        print("✓ Successfully loaded Lite 6 robot from Menagerie!")
        return model
    else:
        print("Error: Lite 6 model file not found")
        return None

def explore_lite6_model(model):
    """Explore Lite 6 robot model"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("Lite 6 Robot Model Information")
    print("="*50)
    
    # Basic information
    print("Basic Information:")
    print("  Joints: {}".format(model.njnt))
    print("  Actuators: {}".format(model.nu))
    print("  Geometries: {}".format(model.ngeom))
    print("  Bodies: {}".format(model.nbody))
    
    # Joint information
    print("\nJoint Information:")
    joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
    
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
    actuator_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
    
    for i, name in enumerate(actuator_names):
        if i < model.nu:
            print("  {}: {}".format(i, name))
    
    # Geometry information
    print("\nGeometry Information:")
    for i in range(min(model.ngeom, 10)):  # Show first 10 geometries
        geom_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i)
        if geom_name:
            geom_type = mujoco.mjtGeom(model.geom_type[i])
            print("  {}: {} (Type: {})".format(i, geom_name, geom_type))

def test_lite6_movement(model):
    """Test Lite 6 robot movement"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("Testing Lite 6 Robot Movement")
    print("="*50)
    
    # Create data object
    data = mujoco.MjData(model)
    
    # Define test positions for Lite 6
    test_positions = [
        ("Home Position", [0, 0, 0, 0, 0, 0]),
        ("Extended Position", [0, -1.5708, 0, -1.5708, 0, 0]),
        ("Bent Position", [-1.5708, -0.785, 1.5708, -2.356, 0, 0]),
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

def get_lite6_specifications():
    """Get Lite 6 specifications"""
    specs = {
        'max_payload': '3kg',
        'workspace_radius': '500mm',
        'repeatability': '±0.1mm',
        'power': 'Low Power',
        'applications': 'Light assembly, education, research, desktop automation'
    }
    return specs

def show_lite6_specifications():
    """Show Lite 6 specifications"""
    specs = get_lite6_specifications()
    print("\n" + "="*50)
    print("Lite 6 Robot Specifications")
    print("="*50)
    print("  Max Payload: {}".format(specs['max_payload']))
    print("  Workspace Radius: {}".format(specs['workspace_radius']))
    print("  Repeatability: {}".format(specs['repeatability']))
    print("  Power Level: {}".format(specs['power']))
    print("  Applications: {}".format(specs['applications']))

def main():
    """Main function"""
    print("Loading Lite 6 Robot using robot_descriptions")
    print("="*50)
    
    # Try to load using robot_descriptions
    model = load_lite6_with_robot_descriptions()
    
    # If failed, load from Menagerie
    if model is None:
        model = load_lite6_from_menagerie()
    
    if model is not None:
        # Explore model
        explore_lite6_model(model)
        
        # Test movement
        test_lite6_movement(model)
        
        # Show specifications
        show_lite6_specifications()
        
        print("\n" + "="*50)
        print("Lite 6 model loaded successfully!")
        print("To start interactive viewer, run:")
        print("python -m mujoco.viewer --mjcf ../ufactory_lite6/scene.xml")
        print("="*50)
    else:
        print("Failed to load Lite 6 robot model")

if __name__ == "__main__":
    main()
