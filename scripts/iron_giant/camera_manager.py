"""
CameraManager class for handling camera setup, image capture, and saving in Isaac Sim.
"""

import numpy as np
import imageio
from typing import Optional, Tuple

import omni.usd
from omni.isaac.sensor import Camera
from pxr import UsdGeom


class CameraManager:
    """A class to manage camera setup, image capture, and saving."""
    
    def __init__(self, prim_path: str = "/World/MyCamera", 
                 position: Tuple[float, float, float] = (0, 0, 5)):
        """
        Initialize camera manager.
        
        Args:
            prim_path: Camera prim path in the scene
            position: Camera position as (x, y, z) tuple
        """
        self.prim_path = prim_path
        self.position = position
        self.camera: Optional[Camera] = None
        
        self._setup_camera()
    
    def _setup_camera(self):
        """Set up the camera in the simulation."""
        # Create camera prim
        stage = omni.usd.get_context().get_stage()
        camera_prim = UsdGeom.Camera.Define(stage, self.prim_path)
        camera_prim.AddTranslateOp().Set(self.position)
        
        # Initialize camera object
        self.camera = Camera(prim_path=self.prim_path)
        self.camera.initialize()
        
        # Add additional data to camera frame
        self.camera.add_distance_to_image_plane_to_frame()  # For depth
        self.camera.add_motion_vectors_to_frame()           # For motion vectors
    
    def capture_and_save_images(self, frame_number: int, save_interval: int = 10):
        """
        Capture RGB and depth images and save them if it's a save frame.
        
        Args:
            frame_number: Current frame number
            save_interval: Save images every N frames
        """
        if self.camera is None:
            return
            
        # Capture RGB image
        rgb_img = self.camera.get_rgb()
        
        # Capture depth and other data
        camera_data = self.camera.get_current_frame()
        depth_image = camera_data.get('distance_to_image_plane')
        
        # Print center pixel distance info
        if depth_image is not None:
            height, width = depth_image.shape
            center_x = width // 2
            center_y = height // 2
            center_distance = depth_image[center_y, center_x]
            print(f"Center pixel ({center_x}, {center_y}) distance: {center_distance:.3f}")
        
        # Save images if it's a save frame
        if frame_number % save_interval == 0:
            self._save_rgb_image(rgb_img, frame_number)
            self._save_depth_image(depth_image, frame_number)
    
    def _save_rgb_image(self, rgb_img: Optional[np.ndarray], frame_number: int):
        """Save RGB image to file."""
        if rgb_img is not None:
            filename = f"rgb_frame_{frame_number:04d}.png"
            imageio.imwrite(filename, rgb_img)
            print(f"Saved {filename} with shape: {rgb_img.shape}")
    
    def _save_depth_image(self, depth_image: Optional[np.ndarray], frame_number: int):
        """Save depth image to file."""
        if depth_image is not None:
            # Normalize depth image for saving (convert to 0-255 range)
            depth_normalized = ((depth_image - depth_image.min()) / 
                              (depth_image.max() - depth_image.min()) * 255).astype(np.uint8)
            filename = f"depth_frame_{frame_number:04d}.png"
            imageio.imwrite(filename, depth_normalized)
            print(f"Saved {filename} with shape: {depth_image.shape}, type: {type(depth_image)}")