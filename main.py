import numpy as np
import pygame

pygame.init()


backgroundColor = (255,255,255)
red = (255, 0, 0)
blue = (0,0,255)
green = (0,255,0)
grey = (125,125,125)

class OrbitalObject:
    def __init__(self, mass, pos):
        self.pos = np.array(pos, dtype=np.float64) # TODO: Perhaps do away with this or make some way to set it
        self.velocity = np.array([0,0], dtype=np.float64) # TODO: Initialize this in a smart way
        self.mass = mass
        self.orbit_type = 'stable-regular' # stable/unstable-regular/elliptical
        
    def distance(self, other_object):
        return np.linalg.norm(self.pos - other_object.pos)

    def get_angle(self, other_object, deg=None):
        relative_x = self.pos[0] - other_object.pos[0]
        relative_y = self.pos[1] - other_object.pos[1]
        ang = np.arctan2(relative_y, relative_x)

        if not deg:
            return ang

        return np.degrees(ang)

    def get_gravity(self, other_object):
        """
        Just returns the force between the two objects
        bascially f1-f2 - how much this object is attracted by the other, lmao
        returns a vector
        """
        f = -1 * (self.mass * other_object.mass)/self.distance(other_object)**2 # Minus 1 cuz towards other object
        # angle = self.get_angle(other_object)

        angle = self.get_angle(other_object)

        f_x = np.cos(angle) * f
        f_y = np.sin(angle) * f

        return np.array([f_x, f_y])

    def accelerate(self, force):
        self.velocity += force/self.mass

    def update_pos(self):
        self.pos += self.velocity

# TODO: Consider whether this one is actually necessary, since 'some' are actually without parents (like the sun)
class OrbitalChild(OrbitalObject):
    """
    'All people are children', only some are parents
    An orbital object with stuff to get attracted by something
    """

    def __init__(self, mass, pos, parent=None):
        super().__init__(mass, pos)
        self.parent = parent

        if self.parent is not None:
            self.get_starting_velocity()
        else:
            self.velocity *= [0,0]

    def update(self):
        """
        All necessary steps for a single update to the system
        """

        self.velocity += self.get_gravity(self.parent)

    def update_pos(self):
        if self.parent is not None:
            self.pos += self.velocity + self.parent.velocity
        else:
            self.pos += self.velocity

   # TODO: MOVE this to be only for children, lone orbitals never need to get a starting velocity
    def get_starting_velocity(self):
        if self.orbit_type == 'stable-regular':
            total_speed = np.sqrt((self.mass*self.parent.mass)/ self.distance(self.parent)) # Absolute velocity required for stable orbit
            angle = self.get_angle(self.parent)
            self.velocity += [np.sin(angle)*total_speed, np.cos(angle)*total_speed]


class OrbitalParent(OrbitalChild):
    """
    Self-contained system meant for orbital simulation. Has one 'main' orbital object, affected by one outside force
    Only the main object affected by outside forces
    """
    
    def __init__(self, mass, pos, children=None, parent=None):
        super().__init__(mass, pos)
        self.children = children # Children are connected to their parents, not the other way around - For simplicity
        self.parent = parent

    # For Now, assume no parent has a parent
    def update(self):
        if self.parent is not None:
            self.velocity += self.get_gravity(self.parent)

        for child in self.children:
            child.update()


# TODO: ADD SOME KIND OF FUNCTION SETCHILDREN, WHICH'LL GO THROUGH EACH OF THE GIVEN CHILDREN AND SET THEIR PARENT AS THE ONE CALLING SET-CHILDREN

sun_pos = [1000, 1000]
sun_mass = 1000
sun = OrbitalParent(mass=sun_mass, pos=sun_pos)

moon_pos, moon_mass = [1550, 1000], 500
moon = OrbitalChild(mass=moon_mass, pos=moon_pos)

earth_pos, earth_mass = [1500, 1000], 5
earth = OrbitalParent(mass=earth_mass, pos=earth_pos)

sun.children = [earth]
earth.children = [moon]
earth.parent = sun
moon.parent = earth

earth.get_starting_velocity()
moon.get_starting_velocity()

# TODO: FIX THE WHOLE GET STARTING VELOCITY THINGY
# OVERALL MAKE A TREE LIKE STRUCTURE FOR THIS, IT IS RIDICULOUS
# TODO: Make an auto-renderer that goes through a single parent like a tree-like-structure to render every item under that

# sun = OrbitalObject(1000, [1000,1000])
# earth = OrbitalObject(1, [1500,1000])


display = pygame.display.set_mode((2000, 2000))
clock = pygame.time.Clock()
frame_rate = 40

# total_speed = np.sqrt(sun.mass/earth.distance(sun))
# angle = earth.get_angle(sun)
# earth.velocity[0] = np.sin(angle) * total_speed
# earth.velocity[1] = np.cos(angle) * total_speed
font = pygame.font.SysFont('Sans-serif', 50)

# print(earth)

while True:
    earth.update_pos()
    moon.update_pos()
    sun.update_pos()

    sun.update()
    earth_to_sun_force = earth.get_gravity(sun)
    moon_to_earth_force = moon.get_gravity(earth)
    #
    # force = earth.get_gravity(sun)
    # earth.accelerate(force)
    # earth.update_pos()
    # angle = earth.get_angle(sun, deg=True)

    clock.tick(frame_rate)
    pygame.display.flip()  # Why this?
    display.fill(backgroundColor)  # Fill with background color - Do before other stuff
    pygame.draw.circle(display, green, earth.pos, radius=20)
    pygame.draw.circle(display, grey, sun.pos, radius=20)
    pygame.draw.circle(display, grey, moon.pos, radius=20)

    pygame.draw.line(display, green, start_pos=earth.pos, end_pos=earth.pos+earth_to_sun_force*100*earth.mass, width=10)
    pygame.draw.line(display, red, start_pos=earth.pos, end_pos=earth.pos+earth.velocity*100, width=10)

    # position = font.render(str(angle), True, (0, 0, 0))
    # position1 = font.render('x' + str(np.cos(angle)), True, (0, 0, 0))
    # position2 = font.render('y' + str(np.sin(angle)), True, (0, 0, 0))
    # position3 = font.render('force' + str(force), True, (0, 0, 0))
    norm = font.render('norm' + str(np.linalg.norm(earth.velocity)), True, (0,0,0))

    # display.blit(position, (50, 1000))
    # display.blit(position1, (50, 1050))
    # display.blit(position2, (50, 1100))
    # display.blit(position3, (50, 1150))
    display.blit(norm, (50, 1200))

