from pygame.locals import K_1, K_2, K_3

from toast.scene import Scene
from toast.text_effects import wavy_text, shaky_text, dialog_text
from toast.event_manager import EventManager
from toast.text import Text
from toast.resource_loader import ResourceLoader
from toast.bitmap_font import BitmapFont

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()

        EventManager.subscribe(self, 'onKeyDown')
        
        # Read the alphabet string from a file.
        alphaArray = open('Data\\anomaly.dat','r').readline()
        # Define the font dimensions
        fontDimension = (32,32)
        # Create bitmap font object
        self.font = BitmapFont(ResourceLoader.load('Data\\anomaly.png'), fontDimension, alphaArray)

        # Create the text object
        self.text = Text(self.font,'Wavy Text')
        # Wrap the text object with an effect
        self.effect = wavy_text.WavyText(self.text)
        
        # Set the text object's position
        self.effect.position = (16, 88)
        
        self.add(self.text)
        
    def onKeyDown(self, event):
        if event.key == K_1:
            self.remove(self.effect)
            self.effect = wavy_text.WavyText(Text(self.font,'Wavy Text'))
            self.effect.position = (16, 88)
            self.add(self.effect)
            
        elif event.key == K_2:
            self.remove(self.effect)
            self.text = Text(self.font,'Shaky Text')
            self.effect = shaky_text.ShakyText(self.text)
            self.effect.position = (0, 88)
            self.add(self.effect)
            
        elif event.key == K_3:
            self.remove(self.effect)
            self.text = Text(self.font,'Dialog Text')
            self.effect = dialog_text.DialogText(self.text)
            self.effect.position = (-16, 88)
            self.add(self.effect)
            

game = DemoGame((640, 480), NewScene)
game.run()
