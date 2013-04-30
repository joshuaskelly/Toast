import pygame

from toast.scene_graph import Scene, Component
from toast.image_sheet import ImageSheet
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.camera import Camera
from toast.math.vector import Vector2D
from toast.math import lerp
from toast.timer import Timer
from toast.animation import Animation
from toast.emitter import Emitter

from examples.demo_game import DemoGame

class DestroyAfter(Component):
    def __init__(self, milliseconds):
        super(DestroyAfter, self).__init__()
        self.__life_timer = Timer(milliseconds)
        
    def update(self, milliseconds=0):
        super(DestroyAfter, self).update(milliseconds)
            
        if self.__life_timer.is_time_up():
            self.__life_timer.reset()
            self.game_object.remove()
            
class Particle(Sprite):
    def __init__(self, lifetime, color):
        default = pygame.Surface((2, 2))
        default.fill((208, 70, 72))
        
        super(Particle, self).__init__(default)
        
        sheet = []
        dark = 20, 12, 28
        steps = 8
        
        for i in range(steps):
            amount = i / float(steps - 1)
            
            r = lerp(color[0], dark[0], amount)
            g = lerp(color[1], dark[1], amount)
            b = lerp(color[2], dark[2], amount)
            
            s = pygame.Surface((2, 2))
            s.fill((r, g, b))
            
            sheet.append(s)
            
        frame_time = lifetime / float(steps - 1)
        puff = [(image, frame_time) for image in sheet]
        
        self.animation = Animation('puff', puff)
        self.add(self.animation)
        self.add(DestroyAfter(lifetime))
        
    @classmethod
    def on_create(cls, emitter, particle):
        particle.transform.position = emitter.parent.transform.position + (16, 16)
        
        
class OrbitBehavior(Component):
    def __init__(self, radius, angular_velocity):
        super(OrbitBehavior, self).__init__()
        self.radius = radius
        self.angular_velocity = angular_velocity
        self.angle = 0
        
    def update(self, milliseconds=0):
        self.angle += self.angular_velocity * milliseconds / 16.66
        offset = Vector2D.from_angle(self.angle) * self.radius
        
        # Rotate about the local 0, 0
        self.game_object.transform.local_position  = offset
        
class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        Camera.current_camera.clear_color = 20, 12, 28
        Camera.current_camera.viewport = 640, 480
        
        dimension = 32, 32
        data = ResourceLoader.load('data//planets.png')
        sheet = ImageSheet(data, dimension)
        
        # Create a sun in the center of the scene
        sun = Sprite(sheet[0], (144, 104))
        self.add(sun)
        
        mercury = Sprite(sheet[3])
        mercury.add(OrbitBehavior(28.0, 3.25))
        mercury.add(Emitter(Particle, (1250, (133, 149, 161)), 160, Particle.on_create))
        sun.add(mercury)
        
        planet = Sprite(sheet[1])
        planet.add(OrbitBehavior(64.0, 0.75))
        planet.add(Emitter(Particle, (5000, (89, 125, 206)), 400, Particle.on_create))
        sun.add(planet)
        
        moon = Sprite(sheet[3])
        moon.add(OrbitBehavior(24.0, 1.875))
        moon.add(Emitter(Particle, (2500, (133, 149, 161)), 200, Particle.on_create))
        planet.add(moon)
        
        planet = Sprite(sheet[2])
        planet.add(OrbitBehavior(132.0, 0.25))
        planet.add(Emitter(Particle, (12000, (109, 170, 44)), 800, Particle.on_create))
        sun.add(planet)
        
        moon = Sprite(sheet[3])
        moon.add(OrbitBehavior(20.0, 4.25))
        moon.add(Emitter(Particle, (1250, (133, 149, 161)), 100, Particle.on_create))
        planet.add(moon)
        
        moon = Sprite(sheet[3])
        moon.add(OrbitBehavior(42.0, 1.75))
        moon.add(Emitter(Particle, (2500, (133, 149, 161)), 200, Particle.on_create))
        planet.add(moon)
        
        planet = Sprite(sheet[4])
        planet.add(OrbitBehavior(232.0, 0.125))
        planet.add(Emitter(Particle, (18000, (208, 70, 72)), 1000, Particle.on_create))
        sun.add(planet)
        
        moon = Sprite(sheet[3])
        moon.add(OrbitBehavior(48.0, 0.75))
        moon.add(Emitter(Particle, (2500, (133, 149, 161)), 200, Particle.on_create))
        planet.add(moon)
        
game = DemoGame((640, 480), NewScene)
game.run()
