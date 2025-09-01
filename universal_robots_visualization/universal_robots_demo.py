#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Robots (UR5e and UR30) General Demo Script
"""

import mujoco
import numpy as np
import os

class UniversalRobot:
    """Universal Robots robot base class"""
    
    def __init__(self, name, model_path, scene_path):
        self.name = name
        self.model_path = model_path
        self.scene_path = scene_path
        self.model = None
        self.data = None
        
    def load_model(self):
        """Load robot model"""
        if os.path.exists(self.model_path):
            print("Loading {} robot model...".format(self.name))
            self.model = mujoco.MjModel.from_xml_path(self.model_path)
            self.data = mujoco.MjData(self.model)
            print("✓ Successfully loaded {} robot model!".format(self.name))
            return True
        else:
            print("Error: {} model file not found: {}".format(self.name, self.model_path))
            return False
    
    def get_info(self):
        """Get robot basic information"""
        if self.model is None:
            return None
            
        info = {
            'name': self.name,
            'joints': self.model.njnt,
            'actuators': self.model.nu,
            'geometries': self.model.ngeom,
            'bodies': self.model.nbody
        }
        return info
    
    def explore_model(self):
        """Explore robot model"""
        if self.model is None:
            return
            
        print("\n" + "="*60)
        print("{} Robot Model Information".format(self.name))
        print("="*60)
        
        info = self.get_info()
        print("Basic Information:")
        print("  Robot Name: {}".format(info['name']))
        print("  Joints: {}".format(info['joints']))
        print("  Actuators: {}".format(info['actuators']))
        print("  Geometries: {}".format(info['geometries']))
        print("  Bodies: {}".format(info['bodies']))
        
        # Joint information
        print("\nJoint Information:")
        joint_names = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", 
                      "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
        
        for i, name in enumerate(joint_names):
            if i < self.model.njnt:
                joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, name)
                if joint_id >= 0:
                    joint_type = mujoco.mjtJoint(self.model.jnt_type[joint_id])
                    if self.model.jnt_limited[joint_id]:
                        range_info = "Range: [{:.2f}, {:.2f}]".format(
                            self.model.jnt_range[joint_id, 0], 
                            self.model.jnt_range[joint_id, 1]
                        )
                    else:
                        range_info = "Unlimited"
                    print("  {}: {} (Type: {}, {})".format(i, name, joint_type, range_info))
        
        # Actuator information
        print("\nActuator Information:")
        actuator_names = ["shoulder_pan", "shoulder_lift", "elbow", "wrist_1", "wrist_2", "wrist_3"]
        
        for i, name in enumerate(actuator_names):
            if i < self.model.nu:
                print("  {}: {}".format(i, name))
    
    def test_movement(self):
        """Test robot movement"""
        if self.model is None or self.data is None:
            return
            
        print("\n" + "="*60)
        print("Testing {} Robot Movement".format(self.name))
        print("="*60)
        
        # Define test positions
        test_positions = [
            ("Home Position", [-1.5708, -1.5708, 1.5708, -1.5708, -1.5708, 0]),
            ("Extended Position", [0, -1.5708, 0, -1.5708, 0, 0]),
            ("Bent Position", [-3.1415, -0.785, 1.5708, -2.356, 0, 0]),
            ("Side Position", [-1.5708, -1.5708, 0, -1.5708, 0, 1.5708])
        ]
        
        for name, qpos in test_positions:
            print("\nTest Position: {}".format(name))
            
            # Set joint positions
            if len(qpos) <= self.model.njnt:
                self.data.qpos[:len(qpos)] = qpos
                
                # Forward kinematics
                mujoco.mj_forward(self.model, self.data)
                
                # Get end effector position
                if self.model.nbody > 0:
                    end_effector_pos = self.data.xpos[-1]
                    print("  End Effector Position: [{:.3f}, {:.3f}, {:.3f}]".format(
                        end_effector_pos[0], end_effector_pos[1], end_effector_pos[2]
                    ))
                    
                    # Calculate workspace radius
                    radius = np.sqrt(end_effector_pos[0]**2 + end_effector_pos[1]**2 + end_effector_pos[2]**2)
                    print("  Workspace Radius: {:.3f}m".format(radius))
    
    def get_specifications(self):
        """Get robot specifications"""
        specs = {
            'UR5e': {
                'max_payload': '5kg',
                'workspace_radius': '850mm',
                'repeatability': '±0.03mm',
                'power': 'Medium Power',
                'applications': 'Precision assembly, laboratory research, education'
            },
            'UR30': {
                'max_payload': '30kg',
                'workspace_radius': '1750mm',
                'repeatability': '±0.05mm',
                'power': 'High Power',
                'applications': 'Heavy lifting, industrial manufacturing, logistics'
            }
        }
        return specs.get(self.name, {})
    
    def show_specifications(self):
        """Show robot specifications"""
        specs = self.get_specifications()
        if specs:
            print("\n" + "="*60)
            print("{} Robot Specifications".format(self.name))
            print("="*60)
            print("  Max Payload: {}".format(specs['max_payload']))
            print("  Workspace Radius: {}".format(specs['workspace_radius']))
            print("  Repeatability: {}".format(specs['repeatability']))
            print("  Power Level: {}".format(specs['power']))
            print("  Applications: {}".format(specs['applications']))

def compare_robots(ur5e, ur30):
    """Compare two robots"""
    print("\n" + "="*60)
    print("UR5e vs UR30 Comparison Analysis")
    print("="*60)
    
    if ur5e.model is not None and ur30.model is not None:
        ur5e_info = ur5e.get_info()
        ur30_info = ur30.get_info()
        
        print("Technical Parameters Comparison:")
        print("  {:15} {:15} {:15}".format("Parameter", "UR5e", "UR30"))
        print("  {:15} {:15} {:15}".format("-"*15, "-"*15, "-"*15))
        print("  {:15} {:15} {:15}".format("Joints", str(ur5e_info['joints']), str(ur30_info['joints'])))
        print("  {:15} {:15} {:15}".format("Actuators", str(ur5e_info['actuators']), str(ur30_info['actuators'])))
        print("  {:15} {:15} {:15}".format("Geometries", str(ur5e_info['geometries']), str(ur30_info['geometries'])))
        print("  {:15} {:15} {:15}".format("Bodies", str(ur5e_info['bodies']), str(ur30_info['bodies'])))
    
    ur5e_specs = ur5e.get_specifications()
    ur30_specs = ur30.get_specifications()
    
    print("\nPerformance Comparison:")
    print("  {:15} {:15} {:15}".format("Performance", "UR5e", "UR30"))
    print("  {:15} {:15} {:15}".format("-"*15, "-"*15, "-"*15))
    print("  {:15} {:15} {:15}".format("Max Payload", ur5e_specs['max_payload'], ur30_specs['max_payload']))
    print("  {:15} {:15} {:15}".format("Workspace", ur5e_specs['workspace_radius'], ur30_specs['workspace_radius']))
    print("  {:15} {:15} {:15}".format("Repeatability", ur5e_specs['repeatability'], ur30_specs['repeatability']))
    print("  {:15} {:15} {:15}".format("Power Level", ur5e_specs['power'], ur30_specs['power']))

def main():
    """Main function"""
    print("Universal Robots (UR5e and UR30) General Demo")
    print("="*60)
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create robot instances
    ur5e = UniversalRobot(
        "UR5e",
        os.path.join(current_dir, "..", "universal_robots_ur5e", "ur5e.xml"),
        os.path.join(current_dir, "..", "universal_robots_ur5e", "scene.xml")
    )
    
    ur30 = UniversalRobot(
        "UR30",
        os.path.join(current_dir, "..", "universal_robots_ur30", "ur30_fixed.xml"),
        os.path.join(current_dir, "..", "universal_robots_ur30", "scene_fixed.xml")
    )
    
    # Load models
    ur5e_loaded = ur5e.load_model()
    ur30_loaded = ur30.load_model()
    
    if ur5e_loaded:
        ur5e.explore_model()
        ur5e.test_movement()
        ur5e.show_specifications()
    
    if ur30_loaded:
        ur30.explore_model()
        ur30.test_movement()
        ur30.show_specifications()
    
    # Compare robots
    if ur5e_loaded and ur30_loaded:
        compare_robots(ur5e, ur30)
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("To start interactive viewer, run:")
    if ur5e_loaded:
        print("  UR5e: python -m mujoco.viewer --mjcf ../universal_robots_ur5e/scene.xml")
    if ur30_loaded:
        print("  UR30: python -m mujoco.viewer --mjcf ../universal_robots_ur30/scene.xml")
    print("="*60)

if __name__ == "__main__":
    main()
