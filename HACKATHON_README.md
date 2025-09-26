# Iron Giant: Dual-Robot Pick-and-Place Simulation 🤖🤖

A sophisticated Isaac Sim robotics simulation showcasing coordinated dual-robot operations for advanced pick-and-place tasks. This project demonstrates the future of industrial automation through multi-robot collaboration.

![Robot Simulation](docs/two_robots.png)

## 🎯 Project Vision

This hackathon project explores the potential of **multi-robot coordination** in industrial automation scenarios. By leveraging two synchronized robots working in tandem, we can achieve:

- **Enhanced productivity** through parallel task execution
- **Improved reliability** with redundant robot systems  
- **Complex manipulation tasks** requiring multi-arm coordination
- **Scalable automation** solutions for modern manufacturing

## 🏗️ Architecture Overview

The project follows a modular, object-oriented design built on NVIDIA Isaac Sim:

```
iron_giant/
├── simulation_world.py    # Main simulation orchestrator
├── robot.py              # Individual robot management & control
├── camera_manager.py     # Vision system for monitoring operations
└── main_world.py         # Entry point & scene setup
```

### Core Components

#### 🌍 SimulationWorld
- **Environment Management**: Sets up physics simulation, ground plane, and objects
- **Multi-Robot Orchestration**: Coordinates multiple robot instances
- **Scene Integration**: Manages USD asset loading and positioning
- **Camera Integration**: Provides visual monitoring and data capture

#### 🤖 Robot Class  
- **Modular Robot Control**: Individual robot instantiation and management
- **Pose Management**: Precise positioning and orientation control
- **Animation System**: Synchronized sinusoidal joint movements with phase offsets
- **Articulation Interface**: Direct joint position control for pick-and-place operations

#### 📷 CameraManager
- **Real-time Monitoring**: RGB and depth image capture
- **Data Collection**: Automated frame saving for analysis
- **Visual Feedback**: Distance measurements and spatial awareness

## 🎮 Pick-and-Place Scenario

### Dual-Robot Configuration

The simulation instantiates **two coordinated robots**:

```python
# Robot 1: Primary manipulator
robot1 = sim_world.add_robot(
    name="robot1",
    position=np.array([1.0, 0.0, 0.0]),
    orientation=np.array([0.7071, 0.0, 0.0, 0.7071]),
    phase_offset=0.0
)

# Robot 2: Secondary manipulator  
robot2 = sim_world.add_robot(
    name="robot2", 
    position=np.array([-1.0, 0.0, 0.0]),
    orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    phase_offset=np.pi / 3  # 60° phase difference for coordination
)
```

### Interactive Environment

The workspace includes various objects that robots can interact with:

- **🎯 Target Cube**: Red dynamic cuboid for manipulation tasks
- **♟️ Chess Set**: Complex object requiring precision handling  
- **🖥️ GeForce RTX 3080**: Delicate electronic component simulation
- **🏗️ Stanley Stand**: Tool organization and storage simulation

### Coordination Strategy

- **Phase-Offset Animation**: Robots operate with synchronized but offset movements
- **Spatial Separation**: Strategic positioning prevents collision while enabling collaboration  
- **Complementary Operations**: One robot can pick while the other places
- **Visual Feedback Loop**: Camera system monitors operations for quality control

## 🚀 Quick Start

### Prerequisites
- NVIDIA Isaac Sim 5.0
- Python 3.11
- CUDA-compatible GPU

### Installation & Running

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/sachinkum0009/iron-giant.git
cd iron-giant

# Run the dual-robot simulation
./run_sim.sh
```



## 🙏 Acknowledgments

- **NVIDIA Isaac Sim**: For the powerful robotics simulation platform
- **Workr Labs**: For the comprehensive robot asset library  
- **Hackathon Organizers**: For the opportunity to showcase innovation
- **Open Source Community**: For the foundational tools and libraries

---

**Built with ❤️ for the future of robotics automation**

*This project demonstrates the potential of coordinated multi-robot systems in transforming industrial automation, making complex manipulation tasks more efficient, reliable, and scalable.*