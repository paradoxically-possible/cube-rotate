import turtle
import math
import random
import time
from typing import List, Tuple

# System Configuration
class Config:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    STAR_COUNT = 300
    CUBE_SIZE = 150
    ROTATION_SPEED = 0.02
    STAR_SPEED = 7
    HUE_SPEED = 0.008
    FPS = 60
    FRAME_TIME = 1.0 / FPS

# Color utilities
class ColorUtils:
    @staticmethod
    def hsv_to_rgb(h: float, s: float = 1.0, v: float = 1.0) -> Tuple[float, float, float]:
        """Convert HSV color to RGB color."""
        r = abs(math.sin(h * math.pi)) * 0.8 + 0.2
        g = abs(math.sin((h + 0.33) * math.pi)) * 0.8 + 0.2
        b = abs(math.sin((h + 0.67) * math.pi)) * 0.8 + 0.2
        return (r, g, b)

# Vector3D class for 3D math operations
class Vector3D:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other: 'Vector3D') -> float:
        """Calculate dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """Calculate cross product."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def magnitude(self) -> float:
        """Calculate vector magnitude."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self) -> 'Vector3D':
        """Return normalized vector."""
        mag = self.magnitude()
        if mag > 0:
            return Vector3D(self.x / mag, self.y / mag, self.z / mag)
        return Vector3D()

# Camera for view control
class Camera:
    def __init__(self):
        self.position = Vector3D(0, 0, -500)
        self.fov = Config.SCREEN_WIDTH * 0.8
    
    def move(self, delta: Vector3D) -> None:
        """Move camera by delta amount."""
        self.position = self.position + delta
    
    def project_point(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Project 3D point to 2D screen space."""
        x, y, z = point
        
        # Apply perspective projection
        camera_z = z - self.position.z
        if camera_z <= 0:
            # Point is behind camera
            return (0, 0, 0)
            
        scale = self.fov / camera_z
        screen_x = x * scale
        screen_y = y * scale
        
        return (screen_x, screen_y, camera_z)

# Advanced star particle
class StarParticle:
    def __init__(self):
        self.position = Vector3D()
        self.reset()
        self.hue = random.random()
        
    def reset(self) -> None:
        """Reset star to a new random position."""
        self.position.z = random.randint(10, Config.SCREEN_WIDTH)
        self.position.x = random.randint(-Config.SCREEN_WIDTH//2, Config.SCREEN_WIDTH//2)
        self.position.y = random.randint(-Config.SCREEN_HEIGHT//2, Config.SCREEN_HEIGHT//2)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.uniform(1, 3)
        self.hue_speed = random.uniform(0.002, 0.005)
        self.trail_length = random.randint(1, 5) if random.random() > 0.7 else 0
        self.flicker = random.random() > 0.9  # Some stars flicker
        self.flicker_speed = random.uniform(0.05, 0.2)
        self.flicker_state = 0
        
    def update(self, delta_time: float) -> None:
        """Update star position and properties."""
        # Scale movement by delta_time for frame-rate independence
        movement = Config.STAR_SPEED * self.speed * delta_time * 60
        self.position.z -= movement
        self.hue = (self.hue + self.hue_speed) % 1.0
        
        # Update flicker effect
        if self.flicker:
            self.flicker_state = (self.flicker_state + self.flicker_speed) % (2 * math.pi)
        
        if self.position.z < 1:
            self.reset()
            
    def get_screen_position(self, camera: Camera) -> Tuple[float, float, float]:
        """Convert 3D position to 2D screen position with perspective."""
        x, y, z = camera.project_point((self.position.x, self.position.y, self.position.z))
        
        # Calculate star size based on distance
        size = self.size * (1 - self.position.z/Config.SCREEN_WIDTH)
        
        # Apply flicker effect if enabled
        if self.flicker:
            flicker_factor = 0.5 + 0.5 * math.sin(self.flicker_state)
            size *= flicker_factor
        
        return x, y, size

# Base 3D object class
class Object3D:
    def __init__(self):
        self.position = Vector3D()
        self.rotation = Vector3D()
        self.scale = Vector3D(1, 1, 1)
        self.vertices: List[Tuple[float, float, float]] = []
        self.edges: List[Tuple[int, int]] = []
        self.faces: List[List[int]] = []
        self.hue_shift = 0.0
    
    def rotate(self, delta_time: float, speed_multiplier: float = 1.0) -> None:
        """Rotate the object based on current rotation speeds."""
        rotation_speed = Config.ROTATION_SPEED * speed_multiplier * delta_time * 60
        self.rotation.x += rotation_speed
        self.rotation.y += rotation_speed * 0.7
        self.rotation.z += rotation_speed * 0.3
        self.hue_shift = (self.hue_shift + Config.HUE_SPEED * delta_time * 60) % 1.0
    
    def transform_vertex(self, vertex: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Apply rotation transformation to a vertex."""
        x, y, z = vertex
        
        # Apply scale
        x *= self.scale.x
        y *= self.scale.y
        z *= self.scale.z
        
        # Rotate around X-axis
        y, z = (y * math.cos(self.rotation.x) - z * math.sin(self.rotation.x),
                y * math.sin(self.rotation.x) + z * math.cos(self.rotation.x))
        
        # Rotate around Y-axis
        x, z = (x * math.cos(self.rotation.y) + z * math.sin(self.rotation.y),
                -x * math.sin(self.rotation.y) + z * math.cos(self.rotation.y))
        
        # Rotate around Z-axis
        x, y = (x * math.cos(self.rotation.z) - y * math.sin(self.rotation.z),
                x * math.sin(self.rotation.z) + y * math.cos(self.rotation.z))
        
        # Apply translation
        x += self.position.x
        y += self.position.y
        z += self.position.z
        
        return (x, y, z)
    
    def calculate_face_normal(self, face: List[int], 
                              projected_vertices: List[Tuple[float, float, float]]) -> Vector3D:
        """Calculate normal vector for a face."""
        if len(face) < 3:
            return Vector3D(0, 0, 1)
            
        # Get three points from the face
        v0 = Vector3D(*projected_vertices[face[0]])
        v1 = Vector3D(*projected_vertices[face[1]])
        v2 = Vector3D(*projected_vertices[face[2]])
        
        # Calculate two edges
        edge1 = v1 - v0
        edge2 = v2 - v0
        
        # Cross product to get normal
        normal = edge1.cross(edge2)
        
        return normal.normalize()
    
    def should_render_face(self, face: List[int], 
                           projected_vertices: List[Tuple[float, float, float]]) -> bool:
        """Determine if a face should be rendered (backface culling)."""
        normal = self.calculate_face_normal(face, projected_vertices)
        
        # Camera is assumed to be looking at -Z direction
        view_vector = Vector3D(0, 0, 1)
        
        # If dot product is negative, face is facing the camera
        return normal.dot(view_vector) < 0
    
    def draw(self, turtle_obj: turtle.Turtle, camera: Camera, wireframe: bool = True) -> None:
        """Draw the 3D object using the provided turtle object."""
        # Transform and project all vertices
        projected_vertices = []
        for vertex in self.vertices:
            transformed = self.transform_vertex(vertex)
            projected = camera.project_point(transformed)
            projected_vertices.append(projected)
        
        if not wireframe:
            # Draw faces (solid rendering)
            # Sort faces by average Z for proper depth rendering
            face_data = []
            for i, face in enumerate(self.faces):
                if not self.should_render_face(face, projected_vertices):
                    continue
                    
                avg_z = sum(projected_vertices[v][2] for v in face) / len(face)
                face_data.append((face, avg_z, i))
            
            # Sort faces by Z depth (back to front)
            face_data.sort(key=lambda x: x[1], reverse=True)
            
            # Draw each face
            for face, _, face_idx in face_data:
                # Create color based on face index and hue shift
                hue = (self.hue_shift + face_idx * 0.05) % 1.0
                color = ColorUtils.hsv_to_rgb(hue)
                turtle_obj.color(color)
                
                # Draw the face as a filled polygon
                turtle_obj.penup()
                first_vertex = face[0]
                x, y, _ = projected_vertices[first_vertex]
                turtle_obj.goto(x, y)
                turtle_obj.pendown()
                turtle_obj.begin_fill()
                
                for vertex_idx in face[1:] + [first_vertex]:
                    x, y, _ = projected_vertices[vertex_idx]
                    turtle_obj.goto(x, y)
                
                turtle_obj.end_fill()
        else:
            # Draw edges with dynamic colors
            for i, edge in enumerate(self.edges):
                # Create color gradient along the edges
                hue = (self.hue_shift + i * 0.02) % 1.0
                color = ColorUtils.hsv_to_rgb(hue)
                
                turtle_obj.color(color)
                v1, v2 = edge
                x1, y1, z1 = projected_vertices[v1]
                x2, y2, z2 = projected_vertices[v2]
                
                # Skip edges with negative z (behind camera)
                if z1 <= 0 or z2 <= 0:
                    continue
                
                turtle_obj.penup()
                turtle_obj.goto(x1, y1)
                turtle_obj.pendown()
                turtle_obj.goto(x2, y2)

# Chromatic cube implementation
class ChromaticCube(Object3D):
    def __init__(self, size: float):
        super().__init__()
        self.size = size
        
        # Define cube vertices
        self.vertices = [
            (-size, -size, -size),  # 0: back bottom left
            (size, -size, -size),   # 1: back bottom right
            (size, size, -size),    # 2: back top right
            (-size, size, -size),   # 3: back top left
            (-size, -size, size),   # 4: front bottom left
            (size, -size, size),    # 5: front bottom right
            (size, size, size),     # 6: front top right
            (-size, size, size)     # 7: front top left
        ]
        
        # Define cube edges
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # front face
            (0, 4), (1, 5), (2, 6), (3, 7)   # connecting edges
        ]
        
        # Define cube faces
        self.faces = [
            [0, 1, 2, 3],  # back
            [4, 5, 6, 7],  # front
            [0, 1, 5, 4],  # bottom
            [2, 3, 7, 6],  # top
            [0, 3, 7, 4],  # left
            [1, 2, 6, 5]   # right
        ]

# Animation manager class
class AnimationManager:
    def __init__(self):
        # Initialize screen
        self.screen = turtle.Screen()
        self.screen.setup(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        self.screen.bgcolor('black')
        self.screen.title("3D Space Animation")
        self.screen.tracer(0, 0)
        
        # Create turtles for drawing
        self.cube_turtle = turtle.Turtle()
        self.star_turtle = turtle.Turtle()
        self.text_turtle = turtle.Turtle()
        
        for t in [self.cube_turtle, self.star_turtle, self.text_turtle]:
            t.hideturtle()
            t.speed(0)
        
        self.cube_turtle.pensize(2)
        
        # Create camera
        self.camera = Camera()
        
        # Create scene objects
        self.cube = ChromaticCube(Config.CUBE_SIZE)
        self.stars = [StarParticle() for _ in range(Config.STAR_COUNT)]
        
        # Animation state
        self.running = True
        self.wireframe_mode = True
        self.rotation_speed = 1.0
        self.last_frame_time = time.time()
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.current_fps = 0
        
        # Setup key bindings
        self.setup_controls()
        
    def setup_controls(self) -> None:
        """Set up keyboard controls."""
        self.screen.onkeypress(self.toggle_pause, "space")
        self.screen.onkeypress(self.increase_speed, "Up")
        self.screen.onkeypress(self.decrease_speed, "Down")
        self.screen.onkeypress(self.toggle_wireframe, "w")
        self.screen.onkeypress(lambda: self.move_camera(Vector3D(0, 0, 10)), "a")
        self.screen.onkeypress(lambda: self.move_camera(Vector3D(0, 0, -10)), "z")
        self.screen.onkeypress(self.exit_animation, "Escape")
        self.screen.listen()
    
    def toggle_pause(self) -> None:
        """Pause/resume the animation."""
        self.running = not self.running
        self.update_status()
    
    def increase_speed(self) -> None:
        """Increase rotation speed."""
        self.rotation_speed = min(3.0, self.rotation_speed + 0.1)
        self.update_status()
    
    def decrease_speed(self) -> None:
        """Decrease rotation speed."""
        self.rotation_speed = max(0.1, self.rotation_speed - 0.1)
        self.update_status()
    
    def toggle_wireframe(self) -> None:
        """Toggle between wireframe and solid mode."""
        self.wireframe_mode = not self.wireframe_mode
        self.update_status()
    
    def move_camera(self, delta: Vector3D) -> None:
        """Move camera by delta amount."""
        self.camera.move(delta)
    
    def exit_animation(self) -> None:
        """Exit the animation."""
        self.running = False
        self.screen.bye()
    
    def update_status(self) -> None:
        """Update status text."""
        self.text_turtle.clear()
        self.text_turtle.penup()
        self.text_turtle.goto(-Config.SCREEN_WIDTH/2 + 10, Config.SCREEN_HEIGHT/2 - 30)
        self.text_turtle.color("white")
        
        status_text = f"Mode: {'Wireframe' if self.wireframe_mode else 'Solid'} | "
        status_text += f"Speed: {self.rotation_speed:.1f} | "
        status_text += f"FPS: {self.current_fps:.1f} | "
        status_text += f"Status: {'Running' if self.running else 'Paused'}"
        status_text += "\nControls: Space=Pause, Up/Down=Speed, W=Wireframe, A/Z=Zoom, Esc=Exit"
        
        self.text_turtle.write(status_text, font=("Arial", 12, "normal"))
    
    def draw_stars(self) -> None:
        """Draw all star particles."""
        self.star_turtle.clear()
        
        for star in self.stars:
            x, y, size = star.get_screen_position(self.camera)
            if size <= 0:  # Skip stars with negative size
                continue
                
            color = ColorUtils.hsv_to_rgb(star.hue)
            self.star_turtle.color(color)
            
            # Draw star
            self.star_turtle.penup()
            self.star_turtle.goto(x, y)
            self.star_turtle.dot(size)
            
            # Draw trail if enabled
            if star.trail_length > 0:
                self.star_turtle.pensize(size * 0.7)
                self.star_turtle.pendown()
                
                # Calculate trail endpoint based on star's movement direction
                trail_x = x + (x / 30) * star.trail_length
                trail_y = y + (y / 30) * star.trail_length
                
                self.star_turtle.goto(trail_x, trail_y)
    
    def calculate_fps(self, current_time: float) -> None:
        """Calculate and update FPS counter."""
        self.frame_count += 1
        elapsed = current_time - self.last_fps_update
        
        # Update FPS every second
        if elapsed >= 1.0:
            self.current_fps = self.frame_count / elapsed
            self.frame_count = 0
            self.last_fps_update = current_time
    
    def update(self, delta_time: float) -> None:
        """Update animation state."""
        if not self.running:
            return
            
        # Update stars
        for star in self.stars:
            star.update(delta_time)
            
        # Update cube
        self.cube.rotate(delta_time, self.rotation_speed)
    
    def render(self) -> None:
        """Render the current frame."""
        self.cube_turtle.clear()
        
        # Draw stars first (background)
        self.draw_stars()
        
        # Draw cube
        self.cube.draw(self.cube_turtle, self.camera, self.wireframe_mode)
        
        # Update screen
        self.screen.update()
    
    def run(self) -> None:
        """Main animation loop."""
        self.update_status()
        
        try:
            while True:
                current_time = time.time()
                delta_time = current_time - self.last_frame_time
                self.last_frame_time = current_time
                
                # Calculate FPS
                self.calculate_fps(current_time)
                
                # Update state
                self.update(delta_time)
                
                # Render frame
                self.render()
                
                # Update status every 30 frames
                if self.frame_count % 30 == 0:
                    self.update_status()
                
                # Calculate remaining time to maintain target frame rate
                elapsed = time.time() - current_time
                remaining = max(0, Config.FRAME_TIME - elapsed)
                time.sleep(remaining)
                
        except (turtle.Terminator, KeyboardInterrupt):
            print("Animation terminated.")

# Main function
def main() -> None:
    """Initialize and run the animation."""
    animation = AnimationManager()
    animation.run()

# Run the program
if __name__ == "__main__":
    main()