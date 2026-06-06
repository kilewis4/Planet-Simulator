from Planet import Planet
import pygame

WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 700

"""
Class to initialize the components of the simulation
"""
class Sim:
    """
    Initializes pygame, screen, and more
    """
    def __init__(self):
        self.planet_list = [
            Planet("E137", 625, 350, 3, 0, 0, 10), 
            Planet("Z981", 800, 150, 1, 0, 0, 3),
            Planet("G426", 650, 200, 1, -0.1, 0.1, 3)
        ]
        self.circle_list = []
        pygame.font.init() 
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        Sim.initialize_pygame(self)
        Sim.run(self)


    """
    Method to initialize components the necessary components of pygame
    """
    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.trail_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)


    """
    Main game loop
    """
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill("black")
            self.screen.blit(self.trail_surface, (0, 0))
            self.trail_surface.fill((0, 0, 0, 10))
            self.circle_list = []
            for planet in self.planet_list:
                pygame.draw.circle(self.trail_surface, (100, 100, 255, 150), (planet.x_coord - (planet.vx * 50), planet.y_coord - (planet.vy * 50)), planet.size)
                self.circle_list.append(pygame.draw.circle(self.screen, "white", (planet.x_coord, planet.y_coord), planet.size))
                planet.update(self.planet_list)
            self.mouse_hover()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

        
    def mouse_hover(self):
        pos = pygame.mouse.get_pos()
        for planet, circle in zip(self.planet_list, self.circle_list):
            if circle.collidepoint(pos):
                text_surface = self.font.render(planet.name, False, "white", "black")
                self.screen.blit(text_surface, (pos[0] + 10, pos[1] + 10))


