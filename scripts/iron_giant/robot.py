"""
Robot class for managing robot creation, positioning, and animation in Isaac Sim.
"""

from pathlib import Path
import numpy as np
from typing import Optional

from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.core.prims import SingleArticulation, XFormPrim


class Robot:
    """A class to manage robot creation, positioning, and animation."""
    
    def __init__(self, world, usd_path: Path, prim_path: str, name: str, 
                 position: np.ndarray = np.array([0.0, 0.0, 0.0]), 
                 orientation: np.ndarray = np.array([1.0, 0.0, 0.0, 0.0]),
                 phase_offset: float = 0.0):
        """
        Initialize a robot instance.
        
        Args:
            world: The Isaac Sim world instance
            usd_path: Path to the robot USD file
            prim_path: Unique prim path for this robot instance
            name: Name identifier for the robot
            position: 3D position offset as numpy array [x, y, z]
            orientation: Quaternion orientation as numpy array [w, x, y, z]
            phase_offset: Phase offset for animation (in radians)
        """
        self.world = world
        self.usd_path = usd_path
        self.prim_path = prim_path
        self.name = name
        self.position = position
        self.orientation = orientation
        self.phase_offset = phase_offset
        
        self.articulation: Optional[SingleArticulation] = None
        self.xform: Optional[XFormPrim] = None
        
        self._setup_robot()
    
    def _setup_robot(self):
        """Set up the robot in the simulation."""
        # Add robot to stage
        add_reference_to_stage(str(self.usd_path), self.prim_path)
        
        # Create articulation and transform objects
        self.articulation = SingleArticulation(prim_path=self.prim_path)
        self.xform = XFormPrim(prim_paths_expr=self.prim_path)
        
        # Set position and orientation
        self.set_pose(self.position, self.orientation)
    
    def set_pose(self, position: np.ndarray, orientation: np.ndarray):
        """Set the robot's position and orientation."""
        if self.xform is not None:
            # Reshape to match expected format for Core API
            pos_reshaped = position.reshape(1, -1)
            orient_reshaped = orientation.reshape(1, -1)
            self.xform.set_world_poses(pos_reshaped, orient_reshaped)
            self.position = position
            self.orientation = orientation
    
    def initialize(self):
        """Initialize the robot articulation."""
        if self.articulation is not None:
            self.articulation.initialize()
    
    def animate(self, frame: int, slowdown_factor: int = 30):
        """
        Animate the robot with sinusoidal joint movements.
        
        Args:
            frame: Current frame number
            slowdown_factor: Factor to slow down the animation
        """
        if self.articulation is None:
            return
            
        # Get number of joints
        ndof = len(self.articulation.get_joint_positions())
        joints = [0.0] * ndof
        
        # Calculate time with phase offset
        t = frame / slowdown_factor + self.phase_offset
        
        # Set joint positions with different amplitudes for variety
        if ndof >= 1:
            joints[0] = np.sin(t)
        if ndof >= 2:
            joints[1] = np.sin(t) * 0.5
        if ndof >= 3:
            joints[2] = np.sin(t) * 0.5
        if ndof >= 4:
            joints[3] = np.sin(t) * 0.7
        if ndof >= 5:
            joints[4] = -np.sin(t) * 0.7
        if ndof >= 6:
            joints[5] = np.sin(t)
        
        # Set the joint positions
        self.articulation.set_joint_positions(positions=np.array(joints))
        
        print(f"{self.name} len of joints: {ndof}")
    
    def get_joint_positions(self) -> np.ndarray:
        """Get current joint positions."""
        if self.articulation is not None:
            return self.articulation.get_joint_positions()
        return np.array([])