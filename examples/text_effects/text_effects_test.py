from pygame.locals import K_1, K_2, K_3

import toast.camera

from toast.scene_graph import Scene
from toast.text_effects import wavy_text, shaky_text, dialog_text
from toast.event_manager import EventManager
from toast.text import Text
from toast.resource_loader import ResourceLoader
from toast.bitmap_font import BitmapFont

from examples.demo_game import DemoGame


class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()

        toast.camera.Camera.current_camera.clear_color = 0, 0, 0

        EventManager.subscribe(self, 'onKeyDown')
        
        # Read the alphabet string from a file.
        alphaArray = open('data/anomaly.dat', 'r').readline()
        # Define the font dimensions
        fontDimension = (32,32)
        # Create bitmap font object
        self.font = BitmapFont(ResourceLoader.load('data/anomaly.png'), fontDimension, alphaArray)

        # Create the text object
        self.text = Text(self.font,'Wavy Text')
        # Wrap the text object with an effect
        self.effect = wavy_text.WavyText(self.text)
        
        # Set the text object's position
        self.effect.position = (16, 88)
        
        self.add(self.text)
        
    def onKeyDown(self, event):
        if event.key == K_1:
            self.text.remove()
            self.text = Text(self.font, 'Wavy Text')
            self.effect = wavy_text.WavyText(self.text)
            self.effect.position = (16, 88)
            self.add(self.text)

        elif event.key == K_2:
            self.text.remove()
            self.text = Text(self.font,'Shaky Text')
            self.effect = shaky_text.ShakyText(self.text)
            self.effect.position = (0, 88)
            self.add(self.text)

        elif event.key == K_3:
            self.text.remove()
            self.text = Text(self.font,'Dialog Text')
            self.effect = dialog_text.DialogText(self.text)
            self.effect.position = (-16, 88)
            self.add(self.text)


game = DemoGame((640, 480), NewScene)
game.run()
