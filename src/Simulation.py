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
        # start with no default planets; user will spawn via UI
        self.planet_list = []
        self.circle_list = []
        pygame.font.init() 
        # use system/default font (avoid Comic Sans)
        self.font = pygame.font.SysFont(None, 26)

        # side-menu state for spawning planets
        self.menu_active = False
        # fields: name, mass, vx, vy, size
        self.menu_fields = [
            {"label": "name", "text": "P", "type": "str"},
            {"label": "mass", "text": "1.0", "type": "float"},
            {"label": "vx", "text": "0.0", "type": "float"},
            {"label": "vy", "text": "0.0", "type": "float"},
            {"label": "size", "text": "5", "type": "int"},
        ]
        self.focus_index = None
        # camera: center world coords and zoom
        self.cam_x = WINDOW_WIDTH / 2
        self.cam_y = WINDOW_HEIGHT / 2
        self.zoom = 1.0
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
        # no trail surface (trails removed)


    """
    Main game loop
    """
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Toggle side menu with Tab
                    if event.key == pygame.K_TAB:
                        self.menu_active = not self.menu_active
                        # reset focus when opening
                        if self.menu_active:
                            self.focus_index = 0
                        else:
                            self.focus_index = None
                    else:
                        # if menu is active and a field is focused, send text input
                        if self.menu_active and self.focus_index is not None:
                            if event.key == pygame.K_BACKSPACE:
                                cur = self.menu_fields[self.focus_index]["text"]
                                self.menu_fields[self.focus_index]["text"] = cur[:-1]
                            elif event.key == pygame.K_RETURN:
                                # move focus to next field
                                self.focus_index = (self.focus_index + 1) % len(self.menu_fields)
                            else:
                                try:
                                    char = event.unicode
                                    if char:
                                        self.menu_fields[self.focus_index]["text"] += char
                                except Exception:
                                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # if menu is active and click inside menu, set focus accordingly
                    if self.menu_active:
                        menu_rect = pygame.Rect(WINDOW_WIDTH - 320, 20, 300, 40 * len(self.menu_fields) + 20)
                        if menu_rect.collidepoint(mouse_pos):
                            # determine which field was clicked
                            rel_y = mouse_pos[1] - (menu_rect.y + 10)
                            idx = rel_y // 40
                            if 0 <= idx < len(self.menu_fields):
                                self.focus_index = int(idx)
                            continue
                        # clicked outside menu: spawn a planet at click location
                        if event.button == 1:
                            self._spawn_planet_at(mouse_pos)
                elif event.type == pygame.MOUSEWHEEL:
                    # zoom with mouse wheel (event.y is scroll direction)
                    try:
                        factor = 1.1 ** event.y
                        self.zoom *= factor
                        self.zoom = max(0.1, min(self.zoom, 5.0))
                    except Exception:
                        pass
            # continuous panning with arrow keys / WASD
            keys = pygame.key.get_pressed()
            pan_speed = 10 / max(self.zoom, 0.01)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.cam_x -= pan_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.cam_x += pan_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.cam_y -= pan_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.cam_y += pan_speed
            self.screen.fill("black")
            # no global trail blit (trails removed)
            self.circle_list = []
            # update physics once per frame (Planet.update updates all bodies)
            if self.planet_list:
                # call update on the first planet to update all bodies
                self.planet_list[0].update(self.planet_list)

            for planet in self.planet_list:
                # draw planet at transformed position
                sx, sy = self.world_to_screen(planet.x_coord, planet.y_coord)
                r = max(1, int(planet.size * self.zoom))
                self.circle_list.append(pygame.draw.circle(self.screen, "white", (int(sx), int(sy)), r))
            self.mouse_hover()
            # draw side menu when active
            if self.menu_active:
                menu_x = WINDOW_WIDTH - 320
                menu_y = 20
                menu_w = 300
                menu_h = 40 * len(self.menu_fields) + 20
                menu_rect = pygame.Rect(menu_x, menu_y, menu_w, menu_h)
                pygame.draw.rect(self.screen, (20, 20, 20), menu_rect)
                pygame.draw.rect(self.screen, (180, 180, 180), menu_rect, 2)
                # render each field
                for i, field in enumerate(self.menu_fields):
                    y = menu_y + 10 + i * 40
                    label_surf = self.font.render(field["label"] + ":", False, "white")
                    box = pygame.Rect(menu_x + 90, y, 190, 32)
                    # highlight focused
                    if self.focus_index == i:
                        pygame.draw.rect(self.screen, (60, 60, 60), box)
                        pygame.draw.rect(self.screen, (255, 255, 255), box, 2)
                    else:
                        pygame.draw.rect(self.screen, (40, 40, 40), box)
                        pygame.draw.rect(self.screen, (120, 120, 120), box, 2)
                    text_surf = self.font.render(field["text"], False, "white")
                    self.screen.blit(label_surf, (menu_x + 10, y + 6))
                    self.screen.blit(text_surf, (box.x + 6, box.y + 6))
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

        
    def mouse_hover(self):
        pos = pygame.mouse.get_pos()
        for planet, circle in zip(self.planet_list, self.circle_list):
            if circle.collidepoint(pos):
                text_surface = self.font.render(planet.name, False, "white", "black")
                self.screen.blit(text_surface, (pos[0] + 10, pos[1] + 10))
    def _spawn_planet_at(self, pos):
        # spawn using menu field values at screen position `pos` (screen coords)
        try:
            name = self.menu_fields[0]["text"] or "P"
            mass = float(self.menu_fields[1]["text"])
            vx = float(self.menu_fields[2]["text"])
            vy = float(self.menu_fields[3]["text"])
            size = int(float(self.menu_fields[4]["text"]))
            # convert screen position to world coords
            world_x, world_y = self.screen_to_world(pos[0], pos[1])
            new_planet = Planet(name, world_x, world_y, mass, vx, vy, size)
            self.planet_list.append(new_planet)
        except Exception:
            # malformed values: ignore spawn
            return

    def world_to_screen(self, x, y):
        sx = (x - self.cam_x) * self.zoom + WINDOW_WIDTH / 2
        sy = (y - self.cam_y) * self.zoom + WINDOW_HEIGHT / 2
        return sx, sy

    def screen_to_world(self, sx, sy):
        x = (sx - WINDOW_WIDTH / 2) / max(self.zoom, 1e-6) + self.cam_x
        y = (sy - WINDOW_HEIGHT / 2) / max(self.zoom, 1e-6) + self.cam_y
        return x, y


