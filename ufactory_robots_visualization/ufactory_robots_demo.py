#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UFACTORY Robots (XArm 6, XArm 7, Lite 6, UF850) General Demo Script
"""

import mujoco
import numpy as np
import os

class UFactoryRobot:
    """UFACTORY robot base class"""
    
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
        joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
        if self.name == "XArm 7":
            joint_names.append("joint7")
        
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
        actuator_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
        if self.name == "XArm 7":
            actuator_names.append("joint7")
        
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
            ("Home Position", [0, 0, 0, 0, 0, 0]),
            ("Extended Position", [0, -1.5708, 0, -1.5708, 0, 0]),
            ("Bent Position", [-1.5708, -0.785, 1.5708, -2.356, 0, 0]),
            ("Side Position", [-1.5708, -1.5708, 0, -1.5708, 0, 1.5708])
        ]
        
        # Add 7th joint for XArm 7
        if self.name == "XArm 7":
            test_positions = [
                ("Home Position", [0, 0, 0, 0, 0, 0, 0]),
                ("Extended Position", [0, -1.5708, 0, -1.5708, 0, 0, 0]),
                ("Bent Position", [-1.5708, -0.785, 1.5708, -2.356, 0, 0, 0]),
                ("Side Position", [-1.5708, -1.5708, 0, -1.5708, 0, 1.5708, 0])
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
            'XArm 6': {
                'max_payload': '5kg',
                'workspace_radius': '700mm',
                'repeatability': '±0.1mm',
                'power': 'Medium Power',
                'applications': 'Light assembly, pick and place, education'
            },
            'XArm 7': {
                'max_payload': '5kg',
                'workspace_radius': '700mm',
                'repeatability': '±0.1mm',
                'power': 'Medium Power',
                'applications': 'Light assembly, pick and place, education, research'
            },
            'Lite 6': {
                'max_payload': '3kg',
                'workspace_radius': '500mm',
                'repeatability': '±0.1mm',
                'power': 'Low Power',
                'applications': 'Light assembly, education, research, desktop automation'
            },
            'UF850': {
                'max_payload': '5kg',
                'workspace_radius': '850mm',
                'repeatability': '±0.1mm',
                'power': 'Medium Power',
                'applications': 'Assembly, pick and place, education, research'
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

def compare_ufactory_robots(robots):
    """Compare UFACTORY robots"""
    print("\n" + "="*60)
    print("UFACTORY Robots Comparison Analysis")
    print("="*60)
    
    # Get loaded robots
    loaded_robots = [robot for robot in robots if robot.model is not None]
    
    if len(loaded_robots) >= 2:
        print("Technical Parameters Comparison:")
        print("  {:15} {:15} {:15} {:15} {:15}".format("Parameter", "XArm 6", "XArm 7", "Lite 6", "UF850"))
        print("  {:15} {:15} {:15} {:15} {:15}".format("-"*15, "-"*15, "-"*15, "-"*15, "-"*15))
        
        # Get info for each robot
        robot_info = {}
        for robot in loaded_robots:
            info = robot.get_info()
            if info:
                robot_info[robot.name] = info
        
        # Display joint counts
        joint_counts = []
        for name in ["XArm 6", "XArm 7", "Lite 6", "UF850"]:
            if name in robot_info:
                joint_counts.append(str(robot_info[name]['joints']))
            else:
                joint_counts.append("N/A")
        
        print("  {:15} {:15} {:15} {:15} {:15}".format("Joints", *joint_counts))
        
        # Display actuator counts
        actuator_counts = []
        for name in ["XArm 6", "XArm 7", "Lite 6", "UF850"]:
            if name in robot_info:
                actuator_counts.append(str(robot_info[name]['actuators']))
            else:
                actuator_counts.append("N/A")
        
        print("  {:15} {:15} {:15} {:15} {:15}".format("Actuators", *actuator_counts))
    
    # Performance comparison
    print("\nPerformance Comparison:")
    print("  {:15} {:15} {:15} {:15} {:15}".format("Performance", "XArm 6", "XArm 7", "Lite 6", "UF850"))
    print("  {:15} {:15} {:15} {:15} {:15}".format("-"*15, "-"*15, "-"*15, "-"*15, "-"*15))
    
    specs_data = {
        "XArm 6": {"max_payload": "5kg", "workspace": "700mm", "repeatability": "±0.1mm", "power": "Medium"},
        "XArm 7": {"max_payload": "5kg", "workspace": "700mm", "repeatability": "±0.1mm", "power": "Medium"},
        "Lite 6": {"max_payload": "3kg", "workspace": "500mm", "repeatability": "±0.1mm", "power": "Low"},
        "UF850": {"max_payload": "5kg", "workspace": "850mm", "repeatability": "±0.1mm", "power": "Medium"}
    }
    
    for metric in ["max_payload", "workspace", "repeatability", "power"]:
        values = []
        for name in ["XArm 6", "XArm 7", "Lite 6", "UF850"]:
            values.append(specs_data[name][metric])
        print("  {:15} {:15} {:15} {:15} {:15}".format(metric.replace("_", " ").title(), *values))

def main():
    """Main function"""
    print("UFACTORY Robots (XArm 6, XArm 7, Lite 6, UF850) General Demo")
    print("="*60)
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create robot instances
    xarm6 = UFactoryRobot(
        "XArm 6",
        os.path.join(current_dir, "..", "ufactory_xarm6", "xarm6_nohand.xml"),
        os.path.join(current_dir, "..", "ufactory_xarm6", "scene.xml")
    )
    
    xarm7 = UFactoryRobot(
        "XArm 7",
        os.path.join(current_dir, "..", "ufactory_xarm7", "xarm7.xml"),
        os.path.join(current_dir, "..", "ufactory_xarm7", "scene.xml")
    )
    
    lite6 = UFactoryRobot(
        "Lite 6",
        os.path.join(current_dir, "..", "ufactory_lite6", "lite6.xml"),
        os.path.join(current_dir, "..", "ufactory_lite6", "scene.xml")
    )
    
    uf850 = UFactoryRobot(
        "UF850",
        os.path.join(current_dir, "..", "ufactory_uf850", "uf850_nohand.xml"),
        os.path.join(current_dir, "..", "ufactory_uf850", "scene.xml")
    )
    
    # Load models
    xarm6_loaded = xarm6.load_model()
    xarm7_loaded = xarm7.load_model()
    lite6_loaded = lite6.load_model()
    uf850_loaded = uf850.load_model()
    
    # Explore and test each robot
    robots = [xarm6, xarm7, lite6, uf850]
    loaded_robots = []
    
    for robot in robots:
        if robot.model is not None:
            robot.explore_model()
            robot.test_movement()
            robot.show_specifications()
            loaded_robots.append(robot)
    
    # Compare robots
    if len(loaded_robots) >= 2:
        compare_ufactory_robots(robots)
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("To start interactive viewer, run:")
    if xarm6_loaded:
        print("  XArm 6: python -m mujoco.viewer --mjcf ../ufactory_xarm6/scene.xml")
    if xarm7_loaded:
        print("  XArm 7: python -m mujoco.viewer --mjcf ../ufactory_xarm7/scene.xml")
    if lite6_loaded:
        print("  Lite 6: python -m mujoco.viewer --mjcf ../ufactory_lite6/scene.xml")
    if uf850_loaded:
        print("  UF850: python -m mujoco.viewer --mjcf ../ufactory_uf850/scene.xml")
    print("="*60)

if __name__ == "__main__":
    main()
