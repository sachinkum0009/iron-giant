"""
SimulationWorld class for managing the overall simulation environment in Isaac Sim.
"""

from pathlib import Path
import numpy as np
from typing import Optional, List

from isaacsim.core.api import World
from isaacsim.core.api.objects import DynamicCuboid

from .robot import Robot
from .camera_manager import CameraManager


class SimulationWorld:
    """Main class to manage the simulation world and coordinate all components."""
    
    def __init__(self, usd_path: Path):
        """
        Initialize the simulation world.
        
        Args:
            usd_path: Path to the robot USD file
        """
        self.usd_path = usd_path
        self.world = World()
        self.robots: List[Robot] = []
        self.camera_manager: Optional[CameraManager] = None
        
        self._setup_world()
    
    def _setup_world(self):
        """Set up the basic world environment."""
        # Add default ground plane
        self.world.scene.add_default_ground_plane()  # type: ignore
        
        # Add a cube object
        # cube_2 = self.world.scene.add(  # type: ignore
        #     DynamicCuboid(
        #         prim_path="/World/cube_2",
        #         name="cube_2",
        #         position=np.array([0.0, 0.0, 0.0]),
        #         scale=np.array([0.2, 0.2, 0.2]),
        #         size=1.0,
        #         color=np.array([255, 0, 0]),
        #     )
        # )
        
        # Set up camera
        self.camera_manager = CameraManager()
        
        print("Robots positioned using Core API")

    def add_usd(self, usd_path: Path, prim_path: str, position: np.ndarray, orientation: np.ndarray):
        """
        Add a USD file to the simulation world at the specified prim path with position and orientation.
        
        Args:
            usd_path: Path to the USD file
            prim_path: Prim path where the USD will be added
            position: 3D position as numpy array [x, y, z]
            orientation: Quaternion orientation as numpy array [w, x, y, z]
        """
        from isaacsim.core.utils.stage import add_reference_to_stage
        from isaacsim.core.prims import XFormPrim
        
        # Add the USD reference to the stage
        add_reference_to_stage(str(usd_path), prim_path)
        
        # Create XFormPrim to handle the transform
        xform = XFormPrim(prim_paths_expr=prim_path)
        
        # Set position and orientation using the same method as robots
        pos_reshaped = position.reshape(1, -1)
        orient_reshaped = orientation.reshape(1, -1)
        xform.set_world_poses(pos_reshaped, orient_reshaped)
    
    def add_robot(self, name: str, position: np.ndarray, orientation: np.ndarray, 
                  phase_offset: float = 0.0) -> Robot:
        """
        Add a robot to the simulation.
        
        Args:
            name: Name identifier for the robot
            position: 3D position as numpy array [x, y, z]
            orientation: Quaternion orientation as numpy array [w, x, y, z]
            phase_offset: Phase offset for animation
            
        Returns:
            Robot instance
        """
        prim_path = f"/World/{name}"
        robot = Robot(
            world=self.world,
            usd_path=self.usd_path,
            prim_path=prim_path,
            name=name,
            position=position,
            orientation=orientation,
            phase_offset=phase_offset
        )
        self.robots.append(robot)
        return robot
    
    def initialize_simulation(self):
        """Initialize the simulation and all robots."""
        self.world.reset()
        for robot in self.robots:
            robot.initialize()
    
    def run_simulation(self, slowdown_factor: int = 30):
        """
        Run the main simulation loop.
        
        Args:
            slowdown_factor: Factor to slow down robot animations
        """
        frame = 0
        
        while True:
            # Step the simulation
            self.world.step(render=True)
            
            # Capture and save images
            if self.camera_manager:
                self.camera_manager.capture_and_save_images(frame)
            
            # Animate all robots
            for robot in self.robots:
                robot.animate(frame, slowdown_factor)
            
            frame += 1