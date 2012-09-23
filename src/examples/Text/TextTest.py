import toast
from toast import Scene

class NewScene(Scene):
    def initialize_scene(self):
        self.resolution = (640, 480)
        
        # Read the alphabet string from a file.
        alphaArray = open("Data\\anomaly.dat","r").readline()
        # Define the font dimensions
        fontDimension = (32,32)
        # Create bitmap font object
        font = toast.BitmapFont("Data\\anomaly.png", fontDimension, alphaArray)
        
        # Create the text object
        text = toast.Text(font,"Basic Text")
        # Set the text object's position
        text.position = (0, 88)
        
        self.add(text)

s = NewScene()

s.run()
