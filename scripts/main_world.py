"""
Main script for running the Isaac Sim robot simulation with modular class structure.
"""

import argparse
from pathlib import Path
import numpy as np

from isaacsim import SimulationApp
CONFIG = {
    "width": 1280,
    "height": 720,
    "window_width": 1920,
    "window_height": 1080,
    "headless": True,
    "hide_ui": False,  # Show the GUI
    "renderer": "RaytracedLighting",
    "display_options": 3286,  # Set display options to show default grid
}
# Initialize simulation app first
simulation_app = SimulationApp(launch_config=CONFIG)

from isaacsim.core.utils.extensions import enable_extension
simulation_app.set_setting("/app/window/drawMouse", True)

# Enable Livestream extension
enable_extension("omni.services.livestream.nvcf")

# Import our modular classes from the iron_giant package
from iron_giant import SimulationWorld

geforce3080_usd_path = Path("/home/asus/backup/zzzzz/isaac/revel_hackathon/revel_files/geforce3080/geforce3080.usd")
chess_usd_path = Path("/home/asus/backup/zzzzz/isaac/revel_hackathon/revel_files/chess/chess.usd")
stanley_stand_usd_path = Path("/home/asus/backup/zzzzz/isaac/revel_hackathon/revel_files/stanley_stand/stanley_stand.usd")

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
    sim_world.add_usd(
        usd_path=chess_usd_path,
        prim_path="/World/Chess",
        position=np.array([0.0, 2.0, 0.5]),  # Position it 2 units along Y-axis and 0.5 units up
        orientation=np.array([1.0, 0.0, 0.0, 0.0])  # No rotation (identity quaternion)
    )
    sim_world.add_usd(
        usd_path=stanley_stand_usd_path,
        prim_path="/World/StanleyStand",
        position=np.array([2.0, 0.0, 0.0]),  # Position it 2 units along X-axis
        orientation=np.array([1.0, 0.0, 0.0, 0.0])  # No rotation (identity quaternion)
    )
    sim_world.add_usd(
        usd_path=geforce3080_usd_path,
        prim_path="/World/GeForce3080",
        position=np.array([-2.0, 0.0, 0.0]),  # Position it -2 units along X-axis
        orientation=np.array([1.0, 0.0, 0.0, 0.0])  # No rotation (identity quaternion)
    )
    
    # Initialize and run simulation
    sim_world.initialize_simulation()
    sim_world.run_simulation()


if __name__ == "__main__":
    main()
