#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for loading UF850 robot using robot_descriptions package
"""

import mujoco
import numpy as np
import os

def load_uf850_with_robot_descriptions():
    """Load UF850 robot using robot_descriptions package"""
    try:
        from robot_descriptions.loaders.mujoco import load_robot_description
        
        print("Loading UF850 robot using robot_descriptions...")
        
        # Try to load UF850 robot
        try:
            model = load_robot_description("uf850_mj_description")
            print("✓ Successfully loaded UF850 robot using robot_descriptions!")
            return model
        except Exception as e:
            print("UF850 not found in robot_descriptions, trying other methods...")
            print("Error: {}".format(e))
            return None
            
    except ImportError:
        print("robot_descriptions package not installed")
        return None

def load_uf850_from_menagerie():
    """Load UF850 robot from MuJoCo Menagerie"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory to reach the menagerie root
    menagerie_dir = os.path.dirname(current_dir)
    uf850_path = os.path.join(menagerie_dir, "ufactory_uf850", "uf850_nohand.xml")
    
    if os.path.exists(uf850_path):
        print("Loading UF850 robot from MuJoCo Menagerie...")
        model = mujoco.MjModel.from_xml_path(uf850_path)
        print("✓ Successfully loaded UF850 robot from Menagerie!")
        return model
    else:
        print("Error: UF850 model file not found")
        return None

def explore_uf850_model(model):
    """Explore UF850 robot model"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("UF850 Robot Model Information")
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

def test_uf850_movement(model):
    """Test UF850 robot movement"""
    if model is None:
        return
    
    print("\n" + "="*50)
    print("Testing UF850 Robot Movement")
    print("="*50)
    
    # Create data object
    data = mujoco.MjData(model)
    
    # Define test positions for UF850
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

def get_uf850_specifications():
    """Get UF850 specifications"""
    specs = {
        'max_payload': '5kg',
        'workspace_radius': '850mm',
        'repeatability': '±0.1mm',
        'power': 'Medium Power',
        'applications': 'Assembly, pick and place, education, research'
    }
    return specs

def show_uf850_specifications():
    """Show UF850 specifications"""
    specs = get_uf850_specifications()
    print("\n" + "="*50)
    print("UF850 Robot Specifications")
    print("="*50)
    print("  Max Payload: {}".format(specs['max_payload']))
    print("  Workspace Radius: {}".format(specs['workspace_radius']))
    print("  Repeatability: {}".format(specs['repeatability']))
    print("  Power Level: {}".format(specs['power']))
    print("  Applications: {}".format(specs['applications']))

def main():
    """Main function"""
    print("Loading UF850 Robot using robot_descriptions")
    print("="*50)
    
    # Try to load using robot_descriptions
    model = load_uf850_with_robot_descriptions()
    
    # If failed, load from Menagerie
    if model is None:
        model = load_uf850_from_menagerie()
    
    if model is not None:
        # Explore model
        explore_uf850_model(model)
        
        # Test movement
        test_uf850_movement(model)
        
        # Show specifications
        show_uf850_specifications()
        
        print("\n" + "="*50)
        print("UF850 model loaded successfully!")
        print("To start interactive viewer, run:")
        print("python -m mujoco.viewer --mjcf ../ufactory_uf850/scene.xml")
        print("="*50)
    else:
        print("Failed to load UF850 robot model")

if __name__ == "__main__":
    main()
