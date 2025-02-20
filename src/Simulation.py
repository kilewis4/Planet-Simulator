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
        self.planet_list = [Planet("dumb", 500, 300, 5, -0.1, -0.1, 10), Planet("dumb2", 800, 150, 1, 0, 0, 3),
                            Planet("dumb3", 650, 200, 1, 0, 0, 3)]
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

    """
    Main game loop
    """
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill("black")
            for planet in self.planet_list:
                pygame.draw.circle(self.screen, "white", (planet.x_coord, planet.y_coord), planet.size)
                planet.update(self.planet_list)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        

