#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for loading XArm 7 robot using robot_descriptions package
"""

import mujoco
import numpy as np
import os

def load_xarm7_with_robot_descriptions():
    """Load XArm 7 robot using robot_descriptions package"""
    try:
        from robot_descriptions.loaders.mujoco import load_robot_description
        
        print("Loading XArm 7 robot using robot_descriptions...")
        
        # Try to load XArm 7 robot
        try:
            model = load_robot_description("xarm7_mj_description")
            print("✓ Successfully loaded XArm 7 robot using robot_descriptions!")
            return model
        except Exception as e:
            print("XArm 7 not found in robot_descriptions, trying other methods...")
            print("Error: {}".format(e))
            return None
            
    except ImportError:
        print("robot_descriptions package not installed")
        return None

def load_xarm7_from_menagerie():
    """Load XArm 7 robot from MuJoCo Menagerie"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory to reach the menagerie root
    menagerie_dir = os.path.dirname(current_dir)
    xarm7_path = os.path.join(menagerie_dir, "ufactory_xarm7", "xarm7.xml")
    
    if os.path.exists(xarm7_path):
        print("Loading XArm 7 robot from MuJoCo Menagerie...")
        model = mujoco.MjModel.from_xml_path(xarm7_path)
        print("✓ Successfully loaded XArm 7 robot from Menagerie!")
        return model
    else:
        print("Error: XArm 7 model file not found")
        return None

def explore_xarm7_model(model):
    """Explore XArm 7 robot model"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("XArm 7 Robot Model Information")
    print("="*50)
    
    # Basic information
    print("Basic Information:")
    print("  Joints: {}".format(model.njnt))
    print("  Actuators: {}".format(model.nu))
    print("  Geometries: {}".format(model.ngeom))
    print("  Bodies: {}".format(model.nbody))
    
    # Joint information
    print("\nJoint Information:")
    joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]
    
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
    actuator_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]
    
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

def test_xarm7_movement(model):
    """Test XArm 7 robot movement"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("Testing XArm 7 Robot Movement")
    print("="*50)
    
    # Create data object
    data = mujoco.MjData(model)
    
    # Define test positions for XArm 7
    test_positions = [
        ("Home Position", [0, 0, 0, 0, 0, 0, 0]),
        ("Extended Position", [0, -1.5708, 0, -1.5708, 0, 0, 0]),
        ("Bent Position", [-1.5708, -0.785, 1.5708, -2.356, 0, 0, 0]),
        ("Side Position", [-1.5708, -1.5708, 0, -1.5708, 0, 1.5708, 0])
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

def get_xarm7_specifications():
    """Get XArm 7 specifications"""
    specs = {
        'max_payload': '5kg',
        'workspace_radius': '700mm',
        'repeatability': '±0.1mm',
        'power': 'Medium Power',
        'applications': 'Light assembly, pick and place, education, research'
    }
    return specs

def show_xarm7_specifications():
    """Show XArm 7 specifications"""
    specs = get_xarm7_specifications()
    print("\n" + "="*50)
    print("XArm 7 Robot Specifications")
    print("="*50)
    print("  Max Payload: {}".format(specs['max_payload']))
    print("  Workspace Radius: {}".format(specs['workspace_radius']))
    print("  Repeatability: {}".format(specs['repeatability']))
    print("  Power Level: {}".format(specs['power']))
    print("  Applications: {}".format(specs['applications']))

def main():
    """Main function"""
    print("Loading XArm 7 Robot using robot_descriptions")
    print("="*50)
    
    # Try to load using robot_descriptions
    model = load_xarm7_with_robot_descriptions()
    
    # If failed, load from Menagerie
    if model is None:
        model = load_xarm7_from_menagerie()
    
    if model is not None:
        # Explore model
        explore_xarm7_model(model)
        
        # Test movement
        test_xarm7_movement(model)
        
        # Show specifications
        show_xarm7_specifications()
        
        print("\n" + "="*50)
        print("XArm 7 model loaded successfully!")
        print("To start interactive viewer, run:")
        print("python -m mujoco.viewer --mjcf ../ufactory_xarm7/scene.xml")
        print("="*50)
    else:
        print("Failed to load XArm 7 robot model")

if __name__ == "__main__":
    main()
