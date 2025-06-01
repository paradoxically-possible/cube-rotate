# Cube Rotate

A collection of Python scripts to render a rotating 3D cube with a star field background using the **turtle** module. This repository contains two main files:

- **Cube_Rotate.py**: A basic version that animates a 3D cube and simple star particles.
- **Cube_Rotate_Two.py**: An advanced version with dynamic coloring, keyboard interactivity, camera control, and both wireframe and solid rendering.

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

Both scripts in this repository utilize Python's built-in **turtle** module to draw 3D animation (a cube) and a star field (moving background stars). Although turtle is a 2D graphics module, a 3D illusion is achieved through:

- **Euler rotation** (X, Y, Z) of the cube's vertices.
- **Perspective projection** mapping 3D coordinates to the 2D screen.
- **Star particles** moving toward the "camera" to simulate space motion.

Two versions are available:

1. **Cube_Rotate.py**  
   - Basic implementation: rotating cube on one axis, limited star particles, no user input, static coloring.  
   - Ideal for beginners learning 3D rotation and animation concepts with turtle.

2. **Cube_Rotate_Two.py**  
   - Advanced version:  
     - **Star field** with more particles (300) and chromatic coloring (hue-shift), flicker effects, and trails.  
     - **3D Cube** modeled via `Object3D` → `ChromaticCube` supporting backface culling and solid rendering.  
     - **Camera system** for dynamic projection and zoom.  
     - **Keyboard interactivity**: Pause, speed control, toggle wireframe/solid, zoom, and on-screen FPS/instruction overlay.  
   - More modular and frame-rate independent (uses `delta_time`).

---

## Key Features

- **3D Cube Animation**  
  - Euler rotation (X, Y, Z)  
  - Perspective projection  
  - Wireframe (edges only) and solid (filled faces) modes  
  - Depth-based or dynamic hue coloring

- **Star Field Background**  
  - Particles moving toward the viewer  
  - Size and brightness scale with depth  
  - (In _Two_ version) hue-shift coloring, flicker effects, and motion trails

- **Interactivity (Cube_Rotate_Two.py)**  
  - **Space**: Pause / Resume animation  
  - **Arrow Up / Down**: Increase / Decrease rotation speed  
  - **W**: Toggle Wireframe / Solid mode  
  - **A / Z**: Zoom In / Out  
  - **Esc**: Exit animation

- **Frame-Rate Independent (Cube_Rotate_Two.py)**  
  - Star motion and cube rotation are time-based, ensuring consistent animation on all systems.

- **Status Overlay (Cube_Rotate_Two.py)**  
  - Displays mode (Wireframe/Solid), rotation speed, FPS, and key controls in the upper-left corner.

---

## Requirements

1. **Python 3.6+** (includes the `turtle` module by default)  
2. **Operating System**: Windows, macOS, Linux, or any system that supports Python and a graphical interface (tkinter)  
   - Ensure `tkinter` is installed (usually bundled with Python)

No external dependencies are required—just make sure Python is installed and `turtle` works.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/paradoxically-possible/cube-rotate.git
   cd cube-rotate
   ````

2. **(Optional) Create a Virtual Environment**
   To isolate the Python environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate.bat     # Windows
   ```

3. **(No Additional Dependencies)**
   This project only uses standard library modules (`turtle`, `math`, `random`, `time`).

---

## Usage

### Running `Cube_Rotate.py`

1. Open a terminal in the repository directory.
2. Run:

   ```bash
   python Cube_Rotate.py
   ```
3. A Turtle window will appear showing a cyan 3D cube rotating with background stars.

   * **Note**: This version has no keyboard controls; the animation runs continuously until the window is closed.

### Running `Cube_Rotate_Two.py`

1. Open a terminal in the repository directory.

2. Run:

   ```bash
   python Cube_Rotate_Two.py
   ```

3. A Turtle window will open, showing a chromatic cube and colorful stars with effects like flicker and trail.

4. **Keyboard Controls**:

   * **Space** → Pause / Resume the animation.
   * **Up Arrow** → Increase rotation speed (max multiplier = 3.0).
   * **Down Arrow** → Decrease rotation speed (min multiplier = 0.1).
   * **W** → Toggle between Wireframe and Solid modes.
   * **A** → Zoom in (camera moves forward).
   * **Z** → Zoom out (camera moves backward).
   * **Esc** → Exit the program and close the window.

5. An on-screen status will display:

   ```
   Mode: <Wireframe/Solid> | Speed: <multiplier> | FPS: <current_fps> | Status: <Running/Paused>
   Controls: Space=Pause, Up/Down=Speed, W=Wireframe, A/Z=Zoom, Esc=Exit
   ```

---

## Code Overview

### 1. Cube\_Rotate.py

A minimal implementation focusing on:

* Euler rotation on X/Y/Z axes
* Perspective projection based on FOV
* Star particles moving along Z-axis with depth-based brightness
* No interactivity (keyboard/mouse)
* All objects rendered using basic turtle lines and dots

### 2. Cube\_Rotate\_Two.py

A modular and interactive version, featuring:

* Chromatic coloring for stars and cube edges/faces (via sine-based hue)
* Star flicker effects and trails
* Frame-rate independence using `delta_time`
* Camera class for perspective transformation and zooming
* `Object3D` base class for scalable 3D object handling
* Keyboard controls for animation state and rendering style
* On-screen status overlay showing real-time metrics

---

## Interactivity and Controls (`Cube_Rotate_Two.py`)

* **Space**

  * Toggle **Pause** / **Resume**. While paused, all objects freeze but the window remains responsive.
  * The overlay updates to show "Status: Paused".

* **Arrow Keys**

  * **↑ Up Arrow** → Increases `rotation_speed` by 0.1 (max 3.0)
  * **↓ Down Arrow** → Decreases `rotation_speed` by 0.1 (min 0.1)

* **W Key**

  * Toggle between **Wireframe** (edges only) and **Solid** (face-filled) rendering.
  * Wireframe mode uses hue gradients for edges.
  * Solid mode uses face-based hue fill with backface culling and Z-sorting.

* **A / Z Keys**

  * **A** → Zoom in (move camera along +Z)
  * **Z** → Zoom out (move camera along -Z)
  * This affects how both the cube and stars are projected on-screen.

* **Escape (Esc)**

  * Closes the Turtle window and exits the program safely.

---

## Customization and Further Development

### Suggested Modifications

1. **Adjust Star Count**

   * `Config.STAR_COUNT` in the second script or `STAR_COUNT` in the first.
   * Higher counts increase realism but may reduce performance.

2. **Change Cube Size or Rotation Speed**

   * `Config.CUBE_SIZE`, `Config.ROTATION_SPEED`, and `rotation_speed` control scale and motion.

3. **Add New 3D Shapes** (in `Cube_Rotate_Two.py`)

   * Subclass `Object3D` (e.g., `ChromaticPyramid`)
   * Define `vertices`, `edges`, and optionally `faces`.
   * Rendering is automatically handled by the parent class.

4. **Lighting Effects**

   * Add directional light and apply basic shading:

     ```python
     light_dir = Vector3D(0, 0, -1)
     intensity = max(0, normal.dot(light_dir))
     shaded_color = tuple(c * intensity for c in base_color)
     ```

5. **Improve Star Rendering**

   * Use sprites or glow effects instead of flat dots.
   * Apply blur or color variance based on "distance".

6. **Change Color Scheme**

   * Edit `ColorUtils.hsv_to_rgb()` for new patterns or brightness range.
   * Add keys to dynamically adjust `Config.HUE_SPEED`.

7. **Switch to Performance-Oriented Libraries**

   * If Turtle becomes limiting, migrate to **Pygame**, **PyOpenGL**, or **Panda3D** for hardware-accelerated 3D rendering.

---

## Repository Structure

```
cube-rotate/
├── Cube_Rotate.py
├── Cube_Rotate_Two.py
├── README.md
└── LICENSE (optional)
```

* **Cube\_Rotate.py** — Basic 3D cube with stars using turtle
* **Cube\_Rotate\_Two.py** — Modular, interactive, and chromatic version
* **README.md** — Full documentation and usage instructions
* **LICENSE** — Add a license file (e.g., MIT, Apache 2.0)

---

## License

No explicit license is currently set. To open this project for public use, consider including a license file (e.g., MIT).
Example `LICENSE` contents:

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

Adapt as needed for your intended usage.

---

## Contributing

All contributions, suggestions, and bug reports are welcome!
To contribute:

1. **Fork** this repository
2. **Create a new branch** for your feature/fix:

   ```bash
   git checkout -b new-feature
   ```
3. **Commit** your changes with clear messages
4. **Push** the branch to your fork and create a **Pull Request**

Please follow Python's style guide (PEP8) when possible and document any significant changes.
