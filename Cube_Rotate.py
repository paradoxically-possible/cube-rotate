"""
3D Space Animation with Rotating Cube and Star Field

This script creates a space-like animation featuring a rotating 3D cube
and star particles that create a starfield effect using Python's turtle module.
"""

import turtle
import math
import random
import time

# System Configuration
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
STAR_COUNT = 100
ROTATION_SPEED = 0.02  # Radians per frame
STAR_SPEED = 7
CUBE_SIZE = 150
TARGET_FPS = 60
FRAME_DURATION = 1.0 / TARGET_FPS

# Colors
BACKGROUND_COLOR = "black"
CUBE_COLOR = "cyan"
STAR_COLOR_BASE = (0.8, 0.8, 0.9)  # Base color for stars (RGB)

# Z-depth settings
MIN_Z = 1  # Minimum Z value to prevent division by zero
MAX_Z = SCREEN_WIDTH  # Maximum Z distance for stars
FOV = SCREEN_WIDTH * 0.8  # Field of view for projection


class StarParticle:
    """Represents a star particle in 3D space that moves toward the viewer."""
    
    def __init__(self):
        """Initialize a star particle with random properties."""
        self.reset()
        
    def reset(self):
        """Reset star to a new random position and properties."""
        self.z = random.randint(MIN_Z + 9, MAX_Z)  # Start deeper in space
        self.x = random.randint(-SCREEN_WIDTH//2, SCREEN_WIDTH//2)
        self.y = random.randint(-SCREEN_HEIGHT//2, SCREEN_HEIGHT//2)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.uniform(1, 3)
        
    def update(self):
        """Update star position by moving it closer to the viewer."""
        self.z -= STAR_SPEED * self.speed
        if self.z < MIN_Z:
            self.reset()
            
    def get_projected_position(self):
        """Calculate the 2D screen position of the star."""
        if self.z < MIN_Z:
            return None  # Skip stars that are too close
            
        scale = 100 / self.z
        x = self.x * scale
        y = self.y * scale
        return x, y
        
    def get_color(self):
        """Calculate star color based on distance (further stars are dimmer)."""
        # Map z from MIN_Z-MAX_Z to brightness level 1.0-0.0
        brightness = max(0.0, min(1.0, 1.0 - (self.z / MAX_Z)))
        return (
            brightness, 
            STAR_COLOR_BASE[1] * brightness, 
            STAR_COLOR_BASE[2]
        )
        
    def get_size(self):
        """Calculate star size based on distance (further stars are smaller)."""
        size = self.size * (1 - self.z / MAX_Z)
        return max(0.1, size)  # Ensure minimum size


class RotatingCube:
    """Represents a 3D cube that can rotate on all three axes."""
    
    def __init__(self, size):
        """Initialize a cube with the given size."""
        self.size = size
        # Define cube vertices (corners)
        self.vertices = [
            (-size, -size, -size),  # 0: front bottom left
            (size, -size, -size),   # 1: front bottom right
            (size, size, -size),    # 2: front top right
            (-size, size, -size),   # 3: front top left
            (-size, -size, size),   # 4: back bottom left
            (size, -size, size),    # 5: back bottom right
            (size, size, size),     # 6: back top right
            (-size, size, size)     # 7: back top left
        ]
        # Define cube edges
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # back face
            (0, 4), (1, 5), (2, 6), (3, 7)   # connecting edges
        ]
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
    def rotate(self):
        """Update rotation angles for all three axes."""
        self.angle_x += ROTATION_SPEED
        self.angle_y += ROTATION_SPEED * 0.7
        self.angle_z += ROTATION_SPEED * 0.3
        
    def _apply_rotation(self, x, y, z):
        """Apply 3D rotation to a point."""
        # X-axis rotation
        y, z = (
            y * math.cos(self.angle_x) - z * math.sin(self.angle_x),
            y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        )
        # Y-axis rotation
        x, z = (
            x * math.cos(self.angle_y) + z * math.sin(self.angle_y),
            -x * math.sin(self.angle_y) + z * math.cos(self.angle_y)
        )
        # Z-axis rotation
        x, y = (
            x * math.cos(self.angle_z) - y * math.sin(self.angle_z),
            x * math.sin(self.angle_z) + y * math.cos(self.angle_z)
        )
        return x, y, z
        
    def _project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates."""
        # Orthographic projection with perspective
        z_adjusted = max(z, -FOV + 1)  # Prevent division by zero
        scale = FOV / (FOV + z_adjusted)
        return x * scale, y * scale
        
    def get_projected_vertices(self):
        """Calculate all projected vertices after rotation."""
        projected_vertices = []
        rotated_vertices = []  # Store the rotated 3D vertices for depth calculation
        
        for x, y, z in self.vertices:
            # Apply rotation
            rx, ry, rz = self._apply_rotation(x, y, z)
            rotated_vertices.append((rx, ry, rz))
            
            # Project to 2D
            px, py = self._project_3d_to_2d(rx, ry, rz)
            projected_vertices.append((px, py))
            
        return projected_vertices, rotated_vertices
        
    def draw(self, turtle_obj):
        """Draw the cube using the provided turtle object."""
        # Get projected vertices and rotated 3D vertices
        projected_vertices, rotated_vertices = self.get_projected_vertices()
        
        # Draw cube edges with depth-based coloring
        for edge in self.edges:
            # Get the vertices for this edge
            v1, v2 = edge
            x1, y1 = projected_vertices[v1]
            x2, y2 = projected_vertices[v2]
            
            # Calculate average Z depth of this edge
            z1 = rotated_vertices[v1][2]
            z2 = rotated_vertices[v2][2]
            avg_z = (z1 + z2) / 2
            
            # Calculate color intensity based on Z depth
            # Edges further back (more positive Z) are dimmer
            max_z = self.size * 1.5
            min_z = -max_z
            z_range = max_z - min_z
            
            # Map z from min_z-max_z to brightness level 1.0-0.3
            brightness = 1.0 - 0.7 * ((avg_z - min_z) / z_range)
            brightness = max(0.3, min(1.0, brightness))
            
            # Set edge color based on depth
            turtle_obj.pencolor(brightness, brightness, 1)  # Blue-cyan effect
            
            # Draw the edge
            turtle_obj.penup()
            turtle_obj.goto(x1, y1)
            turtle_obj.pendown()
            turtle_obj.goto(x2, y2)
            turtle_obj.penup()


class SpaceAnimation:
    """Manages the entire space animation with stars and cube."""
    
    def __init__(self):
        """Initialize the animation environment."""
        # Set up screen
        self.screen = turtle.Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.bgcolor(BACKGROUND_COLOR)
        self.screen.title("3D Space Animation")
        self.screen.tracer(0)  # Turn off animation updates for manual control
        
        # Create objects
        self.cube = RotatingCube(CUBE_SIZE)
        self.stars = [StarParticle() for _ in range(STAR_COUNT)]
        
        # Set up drawing turtles
        self.cube_turtle = turtle.Turtle()
        self.star_turtle = turtle.Turtle()
        
        # Configure turtles
        for t in [self.cube_turtle, self.star_turtle]:
            t.hideturtle()
            t.pensize(2)
            t.speed(0)  # Fastest drawing speed
        
        # Animation state
        self.running = True
        self.last_frame_time = time.time()
        self.frame_count = 0
        self.start_time = time.time()
        
        # Register window close handler
        self.screen._root.protocol("WM_DELETE_WINDOW", self.close)
        
    def close(self):
        """Handle window close event."""
        self.running = False
        
    def draw_stars(self):
        """Draw all star particles."""
        self.star_turtle.clear()
        for star in self.stars:
            # Get projected position
            position = star.get_projected_position()
            if position is None:
                continue
                
            x, y = position
            
            # Check if star is within visible screen bounds (with margin)
            margin = 50  # Extra margin to allow stars just outside the visible area
            if (abs(x) > SCREEN_WIDTH/2 + margin or 
                abs(y) > SCREEN_HEIGHT/2 + margin):
                continue
            
            # Set color and position
            self.star_turtle.color(*star.get_color())
            self.star_turtle.penup()
            self.star_turtle.goto(x, y)
            
            # Draw star as a dot
            self.star_turtle.dot(star.get_size())
            
    def update(self):
        """Update the animation state for one frame."""
        # Update star positions
        for star in self.stars:
            star.update()
            
        # Update cube rotation
        self.cube.rotate()
        
        # Update frame statistics
        self.frame_count += 1
        
    def render(self):
        """Render the current frame."""
        # Clear previous frame
        self.cube_turtle.clear()
        self.star_turtle.clear()
        
        # Draw all elements
        self.draw_stars()
        self.cube.draw(self.cube_turtle)
        
        # Update the screen
        self.screen.update()
        
    def run(self):
        """Run the main animation loop."""
        try:
            while self.running:
                # Calculate time elapsed since last frame
                current_time = time.time()
                elapsed = current_time - self.last_frame_time
                
                # Only render if enough time has passed for next frame
                if elapsed >= FRAME_DURATION:
                    # Calculate actual sleep time to maintain consistent frame rate
                    self.last_frame_time = current_time
                    
                    # Update and render animation
                    self.update()
                    self.render()
                else:
                    # Sleep to prevent CPU hogging, but not too long to maintain frame rate
                    sleep_time = max(0.001, FRAME_DURATION - elapsed - 0.002)
                    time.sleep(sleep_time)
                    
        except turtle.Terminator:
            # Handle case when window is closed suddenly
            print("Animation terminated.")
        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C)
            print("Animation stopped by user.")
        except Exception as e:
            # Handle other exceptions
            print(f"Error occurred: {e}")
        finally:
            # Safe cleanup
            try:
                turtle.bye()
            except:
                pass  # If window is already destroyed, ignore errors


# Main entry point
if __name__ == "__main__":
    # Note: The turtle module is not ideal for high-performance graphics.
    # For more complex 3D scenes, consider using PyGame, Panda3D, or other libraries.
    animation = SpaceAnimation()
    animation.run()