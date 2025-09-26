"""
Iron Giant - A modular Isaac Sim robot simulation framework.

This package provides classes for managing robots, cameras, and simulation environments
in Isaac Sim with a clean, object-oriented architecture.
"""

from .robot import Robot
from .camera_manager import CameraManager
from .simulation_world import SimulationWorld

__all__ = ['Robot', 'CameraManager', 'SimulationWorld']
__version__ = '1.0.0'