import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks - Happy New Year!")

# Clock to control frame rate
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Font for the message
FONT = pygame.font.SysFont('Arial', 48, bold=True)

# Firework class
class Firework:
    def __init__(self):
        # Starting position at the bottom center
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        # Random color
        self.color = random.choice([
            (255, 69, 0),    # OrangeRed
            (255, 140, 0),   # DarkOrange
            (255, 215, 0),   # Gold
            (0, 191, 255),   # DeepSkyBlue
            (138, 43, 226),  # BlueViolet
            (255, 20, 147),  # DeepPink
            (0, 255, 127),   # SpringGreen
        ])
        # Velocity upwards
        self.vy = random.uniform(-8, -12)
        self.vx = random.uniform(-1, 1)
        # Flag to check if explosion happened
        self.exploded = False
        # List of particles
        self.particles = []

    def update(self):
        if not self.exploded:
            # Move the firework
            self.x += self.vx
            self.y += self.vy
            # Gravity
            self.vy += 0.2
            # Check if it should explode
            if self.vy >= 0:
                self.exploded = True
                self.explode()
        else:
            # Update particles
            for particle in self.particles:
                particle.update()
            # Remove dead particles
            self.particles = [p for p in self.particles if not p.is_dead()]

    def explode(self):
        num_particles = random.randint(30, 50)
        for _ in range(num_particles):
            self.particles.append(Particle(self.x, self.y, self.color))

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)
        else:
            for particle in self.particles:
                particle.draw(surface)

    def is_dead(self):
        return self.exploded and len(self.particles) == 0

# Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        # Random direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color  # Initially (R, G, B)
        self.lifetime = 100  # Frames
        self.age = 0
        # Initialize alpha
        self.alpha = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Gravity
        self.vy += 0.05
        self.age += 1
        # Fade out
        self.alpha = max(0, 255 - int((self.age / self.lifetime) * 255))

    def draw(self, surface):
        if self.age < self.lifetime:
            # Create a surface with per-pixel alpha
            surface_temp = pygame.Surface((4, 4), pygame.SRCALPHA)
            # Fill with color and current alpha
            surface_temp.fill((*self.color, self.alpha))
            # Blit to main surface
            surface.blit(surface_temp, (int(self.x), int(self.y)))

    def is_dead(self):
        return self.age >= self.lifetime

def draw_text(surface, text, font, color, center):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, rect)

def main():
    fireworks = []
    # Timer for launching fireworks
    launch_timer = 0
    launch_interval = 20  # Frames

    running = True
    while running:
        CLOCK.tick(FPS)
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Launch fireworks at intervals
        launch_timer += 1
        if launch_timer >= launch_interval:
            launch_timer = 0
            fireworks.append(Firework())

        # Update and draw fireworks
        for firework in fireworks:
            firework.update()
            firework.draw(SCREEN)

        # Remove dead fireworks
        fireworks = [f for f in fireworks if not f.is_dead()]

        # Display "Happy New Year" after some time
        if pygame.time.get_ticks() > 5000:  # 5 seconds
            draw_text(SCREEN, "Happy New Year!", FONT, (255, 255, 255), (WIDTH // 2, HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
