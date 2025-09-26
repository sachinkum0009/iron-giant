"""
Main script for running the Isaac Sim robot simulation with modular class structure.
"""

import argparse
from pathlib import Path
import numpy as np

from isaacsim import SimulationApp

# Initialize simulation app first
simulation_app = SimulationApp({"headless": False})

# Import our modular classes from the iron_giant package
from iron_giant import SimulationWorld


def main():
    """Main function to set up and run the simulation."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("usd_path", type=Path)
    args = parser.parse_args()
    
    usd_path: Path = args.usd_path.resolve()
    assert usd_path.exists(), f"USD file not found: {usd_path}"
    
    # Create simulation world
    sim_world = SimulationWorld(usd_path)
    
    # Add two robots with different positions and orientations
    robot1 = sim_world.add_robot(
        name="robot1",
        position=np.array([1.0, 0.0, 0.0]),
        orientation=np.array([0.7071, 0.0, 0.0, 0.7071]),  # No rotation
        phase_offset=0.0
    )
    
    robot2 = sim_world.add_robot(
        name="robot2", 
        position=np.array([-1.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),  # 90 degrees Z rotation
        phase_offset=np.pi / 3  # 60 degrees phase difference
    )
    
    # Initialize and run simulation
    sim_world.initialize_simulation()
    sim_world.run_simulation()


if __name__ == "__main__":
    main()
