# Cube Rotate

A collection of Python scripts to display a rotating 3D cube with a star field background using the **turtle** module. This repository contains two main files:

- **Cube_Rotate.py**: Basic version with a 3D cube animation and simple star particles.
- **Cube_Rotate_Two.py**: Advanced version featuring dynamic coloring, keyboard interactivity, camera management, and both wireframe and solid rendering.

---

## Table of Contents

1. [Project Description](#project-description)  
2. [Key Features](#key-features)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [Running `Cube_Rotate.py`](#running-cube_rotatepy)  
   - [Running `Cube_Rotate_Two.py`](#running-cube_rotate_twopy)  
6. [Code Overview](#code-overview)  
   - [1. Cube_Rotate.py](#1-cube_rotatepy)  
   - [2. Cube_Rotate_Two.py](#2-cube_rotate_twopy)  
7. [Interactivity and Controls (`Cube_Rotate_Two.py`)](#interactivity-and-controls-cube_rotate_twopy)  
8. [Customization and Further Development](#customization-and-further-development)  
9. [Repository Structure](#repository-structure)  
10. [License](#license)  
11. [Contributing](#contributing)  

---

## Project Description

These two scripts use the built-in Python **turtle** module to draw a 3D cube animation and a “star field” effect. Although they rely on a 2D drawing library, a three-dimensional impression is created using:

- **Euler rotations** (X, Y, Z) on the cube’s vertices.  
- **Perspective projection** to map 3D coordinates onto a 2D screen.  
- **Star particles** moving toward the “camera” to simulate a deep-space backdrop.

There are two versions provided:

1. **Cube_Rotate.py**  
   - A basic implementation: a rotating cube on fixed axes, a limited number of star particles, no user controls, and mostly static coloring.  
   - Ideal for beginners who want to understand fundamental 3D rotation and turtle-based animations.

2. **Cube_Rotate_Two.py**  
   - A more advanced version featuring:  
     - **Star field** with 300 particles, dynamic “chromatic” coloring, flicker effects, and trails.  
     - **3D cube** represented by a generic `Object3D` → `ChromaticCube`, supporting backface culling and solid filling (not just wireframe).  
     - **Camera** with dynamic perspective projection, allowing zoom in/out.  
     - **Interactivity**: Pause/Resume, adjust rotation speed, toggle wireframe/solid, zoom, and overlay text showing FPS, mode, and controls.  
   - More modular and frame-rate independent (using `delta_time`).

---

## Key Features

- **3D Cube Animation**  
  - Euler rotations (X, Y, Z)  
  - Perspective projection  
  - Wireframe (edge drawing) and Solid (filled faces)  
  - Depth-based coloring (Cube_Rotate.py) or dynamic chromatic coloring (Cube_Rotate_Two.py)

- **Star Field Background**  
  - Particles move toward the “camera”  
  - Star size and brightness vary with distance  
  - (In the Two version) Hue-shifting coloring, flicker effects, and particle trails

- **Interactivity (Cube_Rotate_Two.py)**  
  - **Space**: Pause / Resume animation  
  - **Up/Down Arrows**: Increase / Decrease rotation speed  
  - **W**: Toggle between Wireframe and Solid  
  - **A**: Zoom in  
  - **Z**: Zoom out  
  - **Esc**: Exit

- **Frame-Rate Independent (Cube_Rotate_Two.py)**  
  - Particle movement and cube rotation scale based on `delta_time`, ensuring consistent animation even if FPS varies.

- **Status Overlay (Cube_Rotate_Two.py)**  
  - Displays mode (Wireframe/Solid), rotation speed multiplier, FPS, and control instructions in the top-left corner.

---

## Requirements

1. **Python 3.6+** (includes the `turtle` module).  
2. **Operating System**: Windows, macOS, Linux, or any platform supporting Python and a graphical interface (tkinter).  
   - Ensure `tkinter` is installed (usually included with Python in most distributions).  

No external dependencies are required. Simply have Python installed and able to run the `turtle` module.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/paradoxically-possible/cube-rotate.git
   cd cube-rotate
